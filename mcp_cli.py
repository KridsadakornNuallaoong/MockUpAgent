import asyncio
import json

from langchain.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

# load json from registry file
registry_file = "registry.json"
with open(registry_file, "r") as f:
    registry = json.load(f)

@tool("load_tools", description="Load tools from MCP servers.")
async def load_tools() -> list:
    client = MultiServerMCPClient(
        registry['registry']
    )

    tools = await client.get_tools()
     
    return tools

if __name__ == "__main__":
    tools = asyncio.run(load_tools.arun(""))
    print(f"Loaded {len(tools)} tools from MCP servers.")
    print(tools)