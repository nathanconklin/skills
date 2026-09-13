from __future__ import annotations

import argparse
import asyncio
from urllib.parse import urlsplit

import httpx

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def inspect(url: str, share_url: str | None = None) -> None:
    async with streamable_http_client(url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = [tool.name for tool in tools.tools]
            if "export_shared_chat" not in names:
                raise RuntimeError(f"export_shared_chat is missing; found: {names}")
            print(f"MCP ready at {url}: {', '.join(names)}")
            if share_url is None:
                return
            result = await session.call_tool("export_shared_chat", {"url": share_url})
            if result.isError:
                raise RuntimeError(f"Export tool failed: {result.content}")
            metadata = result.structuredContent or {}
            download_url = metadata.get("download_url")
            if not isinstance(download_url, str):
                raise RuntimeError("Export did not return a download URL")
            parsed = urlsplit(download_url)
            local_http = parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}
            if (parsed.scheme != "https" and not local_http) or not parsed.hostname:
                raise RuntimeError("Download must use HTTPS, except for localhost testing")
            resource = next((item for item in result.content if item.type == "resource_link"), None)
            if resource is None or str(resource.uri) != download_url:
                raise RuntimeError("Resource link and download metadata disagree")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(download_url)
                response.raise_for_status()
            if not response.content or "text/markdown" not in response.headers.get("content-type", ""):
                raise RuntimeError("Download did not return nonempty Markdown")
            if resource.size is not None and len(response.content) != resource.size:
                raise RuntimeError("Downloaded size does not match the resource metadata")
            print(
                f"Downloaded {len(response.content)} bytes; "
                f"messages={metadata.get('message_count')}; "
                f"completeness={metadata.get('completeness')}"
            )
            for warning in metadata.get("warnings", []):
                print(f"Warning: {warning}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test the hosted MCP endpoint")
    parser.add_argument("url", nargs="?", default="http://127.0.0.1:8000/mcp")
    parser.add_argument("--share-url", help="Also export a public share URL and verify its download")
    args = parser.parse_args()
    asyncio.run(inspect(args.url, args.share_url))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
