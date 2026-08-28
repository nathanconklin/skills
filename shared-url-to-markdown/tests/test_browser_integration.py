from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from shared_url_to_markdown.urls import parse_shared_url

try:
    from markdownify import markdownify
    from playwright.sync_api import sync_playwright

    from shared_url_to_markdown.browser import _extract_dom

    BROWSER_AVAILABLE = True
except ImportError:
    BROWSER_AVAILABLE = False


@unittest.skipUnless(BROWSER_AVAILABLE, "Playwright test dependencies are not installed")
class BrowserTraversalTests(unittest.TestCase):
    def test_collects_every_window_from_a_virtualized_scroll_root(self) -> None:
        html = """
        <!doctype html>
        <title>Synthetic Virtual Chat</title>
        <style>
          #root { height: 200px; overflow-y: auto; position: relative; }
          #spacer { height: 2000px; position: relative; }
          #items { position: absolute; left: 0; right: 0; }
          [data-message-author-role] { height: 100px; }
        </style>
        <div id="root"><div id="spacer"><div id="items"></div></div></div>
        <script>
          const data = Array.from({length: 10}, (_, index) => ({
            id: `message-${index}`,
            role: index % 2 ? 'assistant' : 'user',
            text: `Unique message ${index}`
          }));
          function render() {
            const root = document.querySelector('#root');
            const start = Math.min(7, Math.floor(root.scrollTop / 100));
            const items = document.querySelector('#items');
            items.style.top = `${start * 100}px`;
            items.innerHTML = data.slice(start, start + 3).map((item) =>
              `<article data-message-id="${item.id}" data-message-author-role="${item.role}">`
              + `<div class="markdown">${item.text}</div></article>`
            ).join('');
          }
          document.querySelector('#root').addEventListener('scroll', render);
          render();
        </script>
        """
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 800, "height": 600})
            page.set_content(html)
            conversation = _extract_dom(
                page,
                parse_shared_url(
                    "https://chatgpt.com/share/11111111-2222-4333-8444-555555555555"
                ),
                markdownify,
            )
            browser.close()

        self.assertEqual(
            len(conversation.messages),
            10,
            [message.id for message in conversation.messages],
        )
        self.assertEqual(
            [message.markdown for message in conversation.messages],
            [f"Unique message {index}" for index in range(10)],
        )
        self.assertEqual(conversation.completeness, "best-effort")
        self.assertTrue(conversation.warnings)


if __name__ == "__main__":
    unittest.main()
