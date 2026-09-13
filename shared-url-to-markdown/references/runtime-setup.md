# Runtime setup

The default package includes the skill and Python exporter. It requires no hosted MCP endpoint, server, tunnel, or separate export service. Retrieving a public conversation still requires internet access through the host; converting an existing snapshot works offline.

## Packages

Packaging and service commands below require the repository checkout. Installed standalone archives contain the exporter, but exclude the service and package builder.

Build the standalone skills and self-contained plugin:

```bash
python scripts/package_skill.py
```

This creates `shared-url-to-markdown-plugin.zip`, containing the skill and scripts with no MCP configuration, plus an OpenAI standalone ZIP with `SKILL.md` at its root and a Claude standalone ZIP containing a top-level skill folder. Use the plugin for ChatGPT web. A standalone ZIP is not a ChatGPT web plugin.

The default build is self-contained. Only users who separately choose to operate the optional service should supply an endpoint:

```bash
python scripts/package_skill.py --mcp-url https://exports.example.com/mcp
```

The explicit `--mcp-url` option adds remote MCP configuration to the plugin. Omit it for the self-contained package. Both variants contain OpenAI and Claude plugin manifests and the bundled exporter. Python itself is supplied by the host; HTTP and snapshot conversion use only its standard library. The browser fallback additionally needs Playwright and Chromium, which the bootstrap script can install in a capable host. Service code and service dependencies are excluded from the packages.

## Installation by environment

- **Codex CLI:** install or copy the standalone skill into a discovered skills directory, or install the generated plugin. Invoke it as `$shared-url-to-markdown`.
- **ChatGPT desktop:** use a standalone skill where supported, or install the generated plugin. Invoke the skill with `@` or describe the export request directly.
- **ChatGPT web:** extract the default plugin archive and follow OpenAI's marketplace and plugin installation workflow. This package contains a skill and scripts only; skip MCP setup. Use a session with Python execution and file delivery. HTTP retrieval also needs network access to the provider. Do not use the standalone ZIP as the web installation procedure.
- **Claude Code:** copy the skill to a discovered Claude skills directory or install the plugin. Invoke it explicitly with `/shared-url-to-markdown` when automatic matching does not trigger.
- **Claude Cowork and Claude web:** use the Claude archive in a host that supports skill installation. Direct retrieval requires Python network access; supplied snapshots can be converted offline.

Skill availability and synchronization depend on the product, plan, workspace permissions, code-execution setting, and admin controls. Installing a personal skill on one vendor does not install it on the other.

Resolve the exporter path relative to the installed skill directory. Run `python scripts/export_shared_chat.py "SHARED_URL"` in that host. Return the resulting Markdown through the host's file-download mechanism. A local filesystem path alone is insufficient delivery from a hosted session.

ChatGPT's cloud browser and code/shell network access are separate capabilities. Web search availability does not establish either, and installing a skill grants neither. See [ChatGPT Work cloud security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security). If Python cannot retrieve the source, use a complete snapshot saved by a capable host tool or supplied as a file. If neither is available, explain the specific limitation and request a snapshot or offer the local command. Do not require the user to deploy a service.

OpenAI documents [standalone skills and plugin availability](https://learn.chatgpt.com/docs/build-skills) and the [connection and plugin testing workflow](https://developers.openai.com/plugins/deploy/connect-chatgpt). These installation instructions were checked on September 13, 2026. Availability does not establish that this exporter's complete workflow has been tested in each environment.

## Deploy the optional connector

This section is for the optional service maintained in the repository. Skip it for the self-contained package.

Run these commands from `shared-url-to-markdown/` in a shell that supports the shown multiline syntax:

```bash
docker build -f service/Dockerfile -t shared-url-to-markdown-service .
docker run --rm -p 8000:8000 \
  -e SHARED_URL_PUBLIC_BASE_URL=https://exports.example.com \
  shared-url-to-markdown-service
```

Terminate TLS at the hosting platform or reverse proxy. The public endpoints are `/mcp`, `/health`, and `/downloads/<random-token>`. Set `SHARED_URL_PUBLIC_BASE_URL` to the externally reachable origin that serves the downloads. Keep the service at the root of that origin. Run one worker/replica; download records are held in process memory.

For a private MCP server, OpenAI also supports Secure MCP Tunnel in developer mode. Register the tunnel and select it when adding the MCP connection using the official connection guide above. A tunnel connection for MCP does not by itself publish this service's ordinary `/downloads/` links. This implementation still requires a reachable download origin; a tunnel alone is not a complete deployment for its current output format.

The deployment is unauthenticated and accepts only public provider share URLs. Use platform-level request limits in addition to the built-in limiter. Requests without a client ID share the anonymous limit; MCP client metadata is not authenticated user identity. Defaults are 10 exports per minute per limiter key, two concurrent browser fallbacks, 25 MiB source/output limits, 90 seconds per retrieval stage or browser-slot wait, and 15-minute download validity. The timeout is not a deadline for the entire export. Configure them with:

- `SHARED_URL_EXPORTS_PER_MINUTE`
- `SHARED_URL_BROWSER_CONCURRENCY`
- `SHARED_URL_MAX_OUTPUT_BYTES`
- `SHARED_URL_TIMEOUT_SECONDS`
- `SHARED_URL_DOWNLOAD_TTL_SECONDS`
- `SHARED_URL_ALLOWED_HOSTS`
- `SHARED_URL_ALLOWED_ORIGINS`
- `SHARED_URL_EXPORT_DIR`

`SHARED_URL_ALLOWED_ORIGINS` defaults to `https://chatgpt.com,https://claude.ai`. Both MCP origin validation and CORS use this same list. An override replaces the defaults; supply all required origins as comma-separated exact values, including ports when present. For example, a local inspector may need `http://localhost:6274`. Paths, trailing slashes, and wildcards are rejected. An empty list permits server-to-server MCP requests without an Origin header while rejecting requests with one. Host validation remains enabled and separate from origin validation.

Use temporary storage for exports. Expired links stop working on access, but file cleanup runs on store access rather than on a timer; a restart loses the in-memory records and can leave old files until the temporary storage is cleared. The Docker command disables HTTP access logging by default.

## Validate the package and ChatGPT web workflow

Run the local suite with Python containing the skill and service dependencies:

```bash
python -m unittest discover -s tests -v
```

The packaging tests extract the default plugin and run the bundled converter with third-party packages disabled and network connections blocked. This verifies self-contained snapshot conversion. The optional service tests are separate from that route.

For a ChatGPT web acceptance test, install the default plugin, open a new conversation with it enabled, and request an export. Download the Markdown and compare the beginning, ending, message order, code blocks, and exposed artifacts with the source. Record the retrieval route, completeness status, and warnings. A local fixture test does not establish end-to-end ChatGPT web compatibility.

For optional service users only, after starting the service, verify MCP initialization and tool discovery:

```bash
python -m service.smoke_mcp https://exports.example.com/mcp
```

To exercise retrieval, export, and the resulting download, supply a public shared conversation that is suitable for testing:

```bash
python -m service.smoke_mcp https://exports.example.com/mcp --share-url "SHARED_URL"
```

Then enable developer mode where your account permits it, add the MCP connection, and confirm that `export_shared_chat` is discovered. Install the plugin containing the skill using the official guide. In a new ChatGPT web conversation with the plugin enabled, request an export of the same share URL. Open the returned download and compare the beginning, ending, message order, code blocks, and any exposed artifacts with the source. Record the reported completeness status and warnings. A successful health check, fixture test, or tool listing alone does not verify this workflow.

If the provider returns a browser challenge or incomplete source, report the failure or `best-effort` status. Do not label an environment verified until an actual export and download have been checked there.

## Hosted snapshot handoff

When a host can save the complete raw response but the code sandbox cannot use the network, retrieve one complete structured response. The exporter currently uses these provider web endpoints, which can change or return browser challenges:

- ChatGPT: `https://chatgpt.com/backend-api/share/<uuid>`
- Claude: `https://claude.ai/api/chat_snapshots/<uuid>?rendering_mode=messages&render_all_tools=true`

Save the raw JSON as `snapshot.json`, then run:

```bash
python scripts/export_shared_chat.py "SHARED_URL" --snapshot snapshot.json
```

This conversion requires only the bundled scripts and Python's standard library. Leave `--mode` at its default and omit `--headed`. If the response is a browser challenge, truncated, summarized, or unavailable as a file/stdin stream, report that limitation and request a complete snapshot or offer the local browser route. Do not reconstruct the conversation from search excerpts or require a hosted service.
