from __future__ import annotations

import asyncio
import json

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import CallToolResult, ResourceLink, TextContent
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from .runtime import ExportCoordinator, ServiceSettings


settings = ServiceSettings.from_env()
coordinator = ExportCoordinator(settings)
mcp = FastMCP(
    "Shared URL to Markdown",
    instructions=(
        "Export only exact public ChatGPT or Claude share URLs. Return a short-lived "
        "Markdown download rather than placing the full transcript in model context."
    ),
    stateless_http=True,
    json_response=True,
    host="0.0.0.0",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=list(settings.allowed_hosts),
        allowed_origins=list(settings.allowed_origins),
    ),
)


@mcp.tool()
async def export_shared_chat(url: str, ctx: Context) -> CallToolResult:
    """Export one public ChatGPT or Claude shared conversation to Markdown."""

    client_key = str(ctx.client_id or "anonymous")
    record = await asyncio.to_thread(coordinator.export, url, client_key)
    result = record.result(settings.public_base_url)
    summary = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
    return CallToolResult(
        content=[
            TextContent(type="text", text=summary),
            ResourceLink(
                type="resource_link",
                uri=result["download_url"],
                name=record.filename,
                description=(
                    f"{result['completeness']} Markdown export of {result['title']}; "
                    f"expires at {result['expires_at']}"
                ),
                mimeType="text/markdown",
                size=len(record.content),
            ),
        ],
        structuredContent=result,
    )


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


@mcp.custom_route("/downloads/{token}", methods=["GET"])
async def download(request: Request) -> Response:
    record = coordinator.store.get(request.path_params["token"])
    if record is None:
        return JSONResponse({"error": "Export not found or expired"}, status_code=404)
    return Response(
        record.content,
        media_type="text/markdown; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{record.filename}"',
            "Cache-Control": "private, max-age=0, no-store",
            "X-Content-Type-Options": "nosniff",
        },
    )


app = CORSMiddleware(
    mcp.streamable_http_app(),
    allow_origins=list(settings.allowed_origins),
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],
)
