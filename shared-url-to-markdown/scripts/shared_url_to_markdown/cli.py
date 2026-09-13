from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .browser import BrowserExtractionError, extract_browser
from .fetch import MAX_RETRIEVAL_BYTES, RetrievalError, extract_http, extract_snapshot_bytes
from .render import default_output_path, render_markdown, write_markdown
from .urls import UrlValidationError, parse_shared_url


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export a public ChatGPT or Claude shared conversation to Markdown."
    )
    parser.add_argument("url", help="Public chatgpt.com/share or claude.ai/share URL")
    parser.add_argument("-o", "--output", type=Path, help="Output Markdown path")
    parser.add_argument(
        "--snapshot",
        type=Path,
        help="Complete provider snapshot JSON file, or - for standard input",
    )
    parser.add_argument(
        "--mode", choices=("auto", "http", "browser"), default="auto",
        help="Extraction method (default: auto)",
    )
    parser.add_argument("--headed", action="store_true", help="Show Chromium for diagnostics")
    parser.add_argument("--timeout", type=float, default=60.0, help="Per-stage timeout in seconds")
    parser.add_argument("--force", action="store_true", help="Replace an explicit existing output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.timeout <= 0:
        print("error: --timeout must be greater than zero", file=sys.stderr)
        return 2
    if args.snapshot is not None and (args.mode != "auto" or args.headed):
        print("error: --snapshot cannot be combined with --mode or --headed", file=sys.stderr)
        return 2
    try:
        shared = parse_shared_url(args.url)
        if args.snapshot is not None:
            content = _read_snapshot(args.snapshot)
            conversation = extract_snapshot_bytes(shared, content)
        else:
            conversation = _extract(shared, args.mode, args.timeout, args.headed)
        output = args.output
        if output is not None and output.suffix.lower() != ".md":
            output = output.with_suffix(output.suffix + ".md" if output.suffix else ".md")
        if output is None:
            output = default_output_path(conversation, Path.cwd())
        write_markdown(output, render_markdown(conversation), force=args.force)
        resolved = output.expanduser().resolve()
        print(f"Exported {len(conversation.messages)} messages to {resolved}")
        print(f"Completeness: {conversation.completeness}")
        for warning in conversation.warnings:
            print(f"Warning: {warning}", file=sys.stderr)
        return 0
    except (UrlValidationError, RetrievalError, BrowserExtractionError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _read_snapshot(path: Path) -> bytes:
    if str(path) == "-":
        content = sys.stdin.buffer.read(MAX_RETRIEVAL_BYTES + 1)
    else:
        with path.expanduser().open("rb") as handle:
            content = handle.read(MAX_RETRIEVAL_BYTES + 1)
    if len(content) > MAX_RETRIEVAL_BYTES:
        raise RetrievalError(
            f"Snapshot exceeds the {MAX_RETRIEVAL_BYTES // (1024 * 1024)} MiB limit"
        )
    return content


def _extract(shared, mode: str, timeout: float, headed: bool):
    if mode == "http":
        return extract_http(shared, timeout)
    if mode == "browser":
        return extract_browser(shared, timeout, headed)

    http_error: Exception | None = None
    try:
        return extract_http(shared, timeout)
    except (RetrievalError, ValueError) as exc:
        http_error = exc
    try:
        return extract_browser(shared, timeout, headed)
    except BrowserExtractionError as browser_error:
        raise BrowserExtractionError(
            f"HTTP extraction failed ({http_error}); browser fallback failed ({browser_error})"
        ) from browser_error
