"""
mcp_client.py - connects to mcp_server.py the way any MCP client does: it starts the server as a
subprocess, then lists or calls its tools over stdin/stdout. Used by the app's 🔌 MCP tab.
"""
import asyncio
import sys

from mcp import Client, StdioServerParameters

import config

SERVER = StdioServerParameters(command=sys.executable, args=[str(config.ROOT / "mcp_server.py")], cwd=config.ROOT)
TIMEOUT_SECONDS = 300   # GraphRAG answers take about 20-30 s on a laptop CPU


async def _connect(action):
    async with Client(SERVER, read_timeout_seconds=TIMEOUT_SECONDS) as client:
        return await action(client)


def list_tools():
    """Returns (server name, list of tools)."""
    async def action(client):
        return client.server_info.name, (await client.list_tools()).tools
    return asyncio.run(_connect(action))


def call_tool(name, arguments):
    """Returns the CallToolResult (content, structured_content, is_error)."""
    return asyncio.run(_connect(lambda client: client.call_tool(name, arguments)))
