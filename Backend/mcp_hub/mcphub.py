import os
from contextlib import AsyncExitStack
from dataclasses import dataclass
from typing import Any

from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.stdio import stdio_client

from mcp import ClientSession, StdioServerParameters


@dataclass
class McpServerConfig:
    name: str
    command: str
    args: list[str]
    env: dict[str, str] | None = None


class McpHub:
    """Manages connections to multiple MCP servers."""

    def __init__(self):
        self.connections: dict[str, ClientSession] = {}
        self._exit_stack = AsyncExitStack()

    async def connect(self, config: McpServerConfig) -> ClientSession:
        """Connect to an MCP server via stdio."""
        print(f"Connecting to MCP server: {config}...")
        if config.name in self.connections:
            return self.connections[config.name]

        env = os.environ.copy()
        if config.env:
            env.update(config.env)

        server_params = StdioServerParameters(
            command=config.command,
            args=config.args,
            env=env,
        )

        transport = await self._exit_stack.enter_async_context(stdio_client(server_params))
        read, write = transport
        
        session = await self._exit_stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        
        self.connections[config.name] = session
        return session

    async def list_tools_langchain(self, server_name: str) -> list[Any]:
        """List tools available on a connected server."""
        if server_name not in self.connections:
            raise ValueError(f"Server {server_name} not connected")
        session = self.connections[server_name]
        # result = await self.connections[server_name].list_tools()
        tools = await load_mcp_tools(session)
        return tools
    
    async def close(self):
        """Close all connections."""
        try:
            await self._exit_stack.aclose()
        except RuntimeError as e:
            # Ignore "Attempted to exit cancel scope..." errors during shutdown
            # This can happen when anyio/starlette lifespan tasks interact
            if "cancel scope" not in str(e):
                raise
        except Exception:
            # Best effort cleanup
            pass
        finally:
            self.connections.clear()