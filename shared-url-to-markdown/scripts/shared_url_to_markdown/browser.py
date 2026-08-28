from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

from .models import Conversation, Message
from .providers import ProviderParseError, merge_dom_messages, normalize_claude, parse_chatgpt_html
from .urls import SharedUrl


class BrowserExtractionError(RuntimeError):
    pass


def extract_browser(shared: SharedUrl, timeout: float, headed: bool) -> Conversation:
    local_browsers = Path(__file__).resolve().parents[2] / ".venv" / "playwright-browsers"
    if local_browsers.is_dir():
        os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(local_browsers))
    try:
        from markdownify import markdownify
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise BrowserExtractionError(
            "Browser dependencies are missing. Run scripts/bootstrap.py after approving downloads."
        ) from exc

    timeout_ms = max(1, int(timeout * 1000))
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=not headed)
            context = browser.new_context(
                accept_downloads=False,
                java_script_enabled=True,
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1440, "height": 1000},
            )
            context.set_default_timeout(timeout_ms)
            page = context.new_page()
            page.on("popup", lambda popup: popup.close())
            try:
                page.goto(shared.normalized, wait_until="domcontentloaded", timeout=timeout_ms)
                _wait_for_challenge(page, timeout)
                structured_error = ""

                if shared.provider == "chatgpt":
                    try:
                        return parse_chatgpt_html(page.content(), shared)
                    except ProviderParseError:
                        pass
                else:
                    structured, structured_error = _claude_snapshot_from_page(page, shared)
                    if structured is not None:
                        try:
                            return normalize_claude(
                                structured, shared, extraction_method="claude-browser-snapshot-api"
                            )
                        except ProviderParseError:
                            pass

                try:
                    return _extract_dom(page, shared, markdownify)
                except ValueError as exc:
                    if shared.provider == "claude" and structured_error:
                        raise BrowserExtractionError(
                            f"Claude snapshot request failed ({structured_error}); DOM fallback failed ({exc})"
                        ) from exc
                    raise
            finally:
                context.close()
                browser.close()
    except PlaywrightError as exc:
        raise BrowserExtractionError(f"Browser extraction failed: {exc}") from exc


def _wait_for_challenge(page, timeout: float) -> None:
    deadline = time.monotonic() + min(timeout, 45.0)
    while time.monotonic() < deadline:
        title = page.title().lower()
        if "just a moment" not in title and "checking your browser" not in title:
            return
        page.wait_for_timeout(500)


def _claude_snapshot_from_page(page, shared: SharedUrl) -> tuple[dict[str, Any] | None, str]:
    result = page.evaluate(
        """async ({id}) => {
          try {
            const response = await fetch(
              `/api/chat_snapshots/${id}?rendering_mode=messages&render_all_tools=true`,
              {credentials: 'same-origin', headers: {'Content-Type': 'application/json'}}
            );
            const contentType = response.headers.get('content-type') || '';
            const text = await response.text();
            return {ok: response.ok, contentType, text};
          } catch (error) {
            return {ok: false, contentType: '', text: String(error)};
          }
        }""",
        {"id": shared.share_id},
    )
    if not isinstance(result, dict):
        return None, "browser returned no response metadata"
    if not result.get("ok") or "json" not in result.get("contentType", ""):
        prefix = str(result.get("text", ""))[:80].replace("\n", " ")
        return None, f"content-type={result.get('contentType')!r}, response={prefix!r}"
    try:
        payload = json.loads(result.get("text", ""))
    except json.JSONDecodeError:
        return None, "snapshot response was not valid JSON"
    if not isinstance(payload, dict):
        return None, "snapshot response was not an object"
    return payload, ""


def _extract_dom(page, shared: SharedUrl, markdownify) -> Conversation:
    # First force the virtualized list to settle at its oldest mounted window.
    stable = 0
    previous = None
    for _ in range(12):
        state = page.evaluate(_DOM_SCRIPT, "top")
        signature = (state.get("scrollHeight"), state.get("first"))
        stable = stable + 1 if signature == previous and state.get("atTop") else 0
        previous = signature
        if stable >= 2:
            break
        page.wait_for_timeout(400)

    mounted: list[dict[str, str]] = []
    bottom_stable = 0
    previous_bottom = None
    for _ in range(2000):
        state = page.evaluate(_DOM_SCRIPT, "scan")
        items = state.get("items")
        if isinstance(items, list):
            mounted.extend(item for item in items if isinstance(item, dict))

        bottom_signature = (state.get("scrollHeight"), state.get("last"))
        if state.get("atBottom") and bottom_signature == previous_bottom:
            bottom_stable += 1
        else:
            bottom_stable = 0
        if bottom_stable >= 2:
            break
        previous_bottom = bottom_signature
        page.evaluate(_DOM_SCRIPT, "advance")
        page.wait_for_timeout(250)
    else:
        raise BrowserExtractionError("Virtualized traversal exceeded its safety limit")

    deduplicated = merge_dom_messages(mounted)
    messages: list[Message] = []
    for index, item in enumerate(deduplicated):
        html = item.get("html", "")
        markdown = markdownify(html, heading_style="ATX", bullets="-").strip()
        if not markdown:
            markdown = item.get("text", "").strip()
        if not markdown:
            continue
        message_id = item.get("id") or hashlib.sha256(
            f"{item.get('role')}\x1f{item.get('text')}".encode("utf-8")
        ).hexdigest()
        messages.append(Message(message_id or f"message-{index}", item["role"], markdown))

    title = (page.title() or "").strip()
    if not title or title.lower() in {"chatgpt", "claude"}:
        title = f"{shared.provider.title()} Shared Conversation"
    conversation = Conversation(
        provider=shared.provider,
        share_id=shared.share_id,
        title=title,
        source_url=shared.normalized,
        messages=messages,
        extraction_method=f"{shared.provider}-virtualized-dom",
        completeness="best-effort",
        warnings=[
            "The provider's structured snapshot was unavailable. All traversed virtualized "
            "message windows were exported, but completeness could not be independently verified."
        ],
    )
    conversation.validate()
    return conversation


_DOM_SCRIPT = r"""(action) => {
  const selector = [
    '[data-message-author-role]',
    '[data-testid="user-message"]',
    '[data-testid="assistant-message"]',
    '[data-testid*="user-message"]',
    '[data-testid*="assistant-message"]',
    '.font-user-message',
    '.font-claude-response'
  ].join(',');
  const all = Array.from(document.querySelectorAll(selector));
  const nodes = all.filter((node) => !all.some((other) => other !== node && other.contains(node)));
  const roots = [];
  for (const node of nodes) {
    let current = node.parentElement;
    while (current && current !== document.body) {
      const style = getComputedStyle(current);
      if (/(auto|scroll)/.test(style.overflowY) && current.scrollHeight > current.clientHeight + 4) {
        roots.push(current);
      }
      current = current.parentElement;
    }
  }
  const root = roots.sort((a, b) => (b.scrollHeight - b.clientHeight) - (a.scrollHeight - a.clientHeight))[0]
    || document.scrollingElement || document.documentElement;
  if (action === 'top') root.scrollTop = 0;
  if (action === 'advance') root.scrollTop = Math.min(root.scrollHeight, root.scrollTop + Math.max(80, root.clientHeight * 0.75));

  function roleFor(node) {
    const direct = (node.getAttribute('data-message-author-role') || '').toLowerCase();
    if (direct === 'user' || direct === 'assistant') return direct;
    const marker = `${node.getAttribute('data-testid') || ''} ${node.className || ''}`.toLowerCase();
    if (marker.includes('user') || marker.includes('human')) return 'user';
    if (marker.includes('assistant') || marker.includes('claude')) return 'assistant';
    return '';
  }
  const items = nodes.map((node, index) => {
    const role = roleFor(node);
    const content = node.querySelector('.markdown, .whitespace-pre-wrap, [class*="font-claude"], [class*="prose"]') || node;
    return {
      id: node.getAttribute('data-message-id') || node.getAttribute('data-testid') || node.id || '',
      role,
      html: content.innerHTML || '',
      text: (content.innerText || content.textContent || '').trim(),
      index: String(index)
    };
  }).filter((item) => item.role && item.text);
  const top = Number(root.scrollTop || 0);
  const clientHeight = Number(root.clientHeight || innerHeight || 0);
  const scrollHeight = Number(root.scrollHeight || document.documentElement.scrollHeight || 0);
  return {
    items,
    first: items[0]?.id || items[0]?.text.slice(0, 80) || '',
    last: items.at(-1)?.id || items.at(-1)?.text.slice(0, 80) || '',
    scrollTop: top,
    clientHeight,
    scrollHeight,
    atTop: top <= 2,
    atBottom: top + clientHeight >= scrollHeight - 3
  };
}"""
