#!/usr/bin/env python3
"""Read-only HTTP MCP probe against this project's configured Context7 endpoint."""
import json
import os
from pathlib import Path
import sys
import tomllib
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]


def main():
    config = tomllib.loads((ROOT / ".codex/config.toml").read_text())["mcp_servers"]["context7"]
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    # Optional official API key is read from environment only; never printed or saved.
    token = os.environ.get("CONTEXT7_API_KEY")
    if token:
        headers["Authorization"] = "Bearer " + token

    def request(method, params=None, request_id=None):
        payload = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        if request_id is not None:
            payload["id"] = request_id
        req = urllib.request.Request(config["url"], json.dumps(payload).encode(), headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            if response.headers.get("Mcp-Session-Id"):
                headers["Mcp-Session-Id"] = response.headers["Mcp-Session-Id"]
            body = response.read(512 * 1024 + 1)
        if len(body) > 512 * 1024:
            raise ValueError("oversized MCP response")
        if not body.strip():
            return {}
        content = body.decode()
        if content.lstrip().startswith("{"):
            messages = [json.loads(content)]
        else:
            messages = [json.loads(line[5:].strip()) for line in content.splitlines() if line.startswith("data:")]
        for message in messages:
            if message.get("id") == request_id:
                if message.get("error"):
                    raise ValueError("MCP returned an error")
                return message.get("result", {})
        raise ValueError("missing JSON-RPC response")

    result = request("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                   "clientInfo": {"name": "louipuri-harness-probe", "version": "1.0"}}, 1)
    headers["MCP-Protocol-Version"] = result["protocolVersion"]
    request("notifications/initialized")
    listing = request("tools/list", {}, 2)
    names = {tool["name"] for tool in listing.get("tools", [])}
    if not {"resolve-library-id", "query-docs"}.issubset(names):
        raise ValueError("expected Context7 tools missing")
    # The actual installed harness dependency, not an invented product stack.
    manifest = json.loads((ROOT / "tools/ai/node_modules/playwright/package.json").read_text())
    version = manifest["version"]
    resolution = request("tools/call", {"name": "resolve-library-id", "arguments": {
        "libraryName": "Playwright", "query": f"Playwright {version}: browser launch and close"}}, 3)
    if resolution.get("isError"):
        raise ValueError("library resolution failed")
    text = "\n".join(item.get("text", "") for item in resolution.get("content", []))
    if "/microsoft/playwright" not in text:
        raise ValueError("Playwright official library id not resolved")
    docs = request("tools/call", {"name": "query-docs", "arguments": {
        "libraryId": "/microsoft/playwright", "query": f"Playwright {version}: launch Chromium headless and close browser"}}, 4)
    content = "\n".join(item.get("text", "") for item in docs.get("content", []))
    if docs.get("isError") or not content.strip():
        raise ValueError("documentation query failed")
    print(f"PASS D: initialize, tools/list, resolve-library-id, query-docs; installed Playwright {version}")
    print("Version limit: alpha-specific docs are not guaranteed; verify API against installed code before product use.")
    print("Public documentation excerpt:", content[:450].replace("\n", " "))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        status = f" HTTP {error.code}" if isinstance(error, urllib.error.HTTPError) else ""
        print(f"Context7 probe failed: {type(error).__name__}{status}; check network/authentication. No credentials logged.", file=sys.stderr)
        raise SystemExit(1)
