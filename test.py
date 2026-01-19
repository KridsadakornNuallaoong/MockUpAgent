import asyncio
import json
import os
import subprocess
from contextlib import AsyncExitStack
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from langchain.tools import BaseTool, tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import (Connection, StdioConnection,
                                             create_session)
from langchain_mcp_adapters.tools import _list_all_tools, load_mcp_tools
from langgraph.config import RunnableConfig
from mcp.client.stdio import stdio_client

from agent_model import AgentModel
from mcp import ClientSession, StdioServerParameters
from mcp_hub.mcphub import McpHub, McpServerConfig
from model.ollama.custom_model_01 import llm
from tools.time_tools import get_current_time


def printt(title: str, symbol: str = "—", size: int = -1):
    if title.startswith("\n"):
        title = title[1:]

    if title.endswith("\n"):
        title = title[:-1]

    terminal_length = os.get_terminal_size().columns

    bar = symbol * (size if size != -1 else ((terminal_length - len(title) - 5) // 2))

    print("\n", bar, f" {title} ", bar, "\n")

def mcp_manager(args: list[str], *, timeout_s: float = 60) -> str:
    process = subprocess.Popen(
        ["docker", "mcp"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        stdout, stderr = process.communicate(timeout=timeout_s)
        # if stdout:
        #     print("MCP Manager Output:\n", stdout)
        if stderr:
            print("MCP Manager Errors:\n", stderr)
    except subprocess.TimeoutExpired:
        process.kill()
        print("MCP Manager timed out.")
        
    if process.returncode != 0:
        msg = stderr.strip() or stdout.strip() or f"exit={process.returncode}"
        raise RuntimeError(f"MCP Manager failed: {msg}")
        
    return stdout

import asyncio
import os
from contextlib import AsyncExitStack
from dataclasses import dataclass
from typing import Any

from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.stdio import stdio_client

from mcp import ClientSession, StdioServerParameters


async def main():
    # printt("Starting Agent Model Test with out tools")
    # agent_model = AgentModel(model=llm, tools=[], system_prompt_content="You are a helpful assistant. always checking your tools.")
    # messages = "please tell me current time."
    # print("now agentic tools: ", agent_model.list_tools())
    # config: RunnableConfig = {
    #     "configurable": {
    #         "thread_id": "1",
    #     }
    # }
    # agent_model.set_config(config)
    # await agent_model.astream(messages, path_output="./output")
    # printt("Test completed without tools")

    # printt("Adding Time Tool")
    # agent_model.add_tool(get_current_time)
    # print("now agentic tools: ", agent_model.list_tools())
    # messages = "please tell me current time."
    # await agent_model.astream(messages, path_output="./output")
    # printt("Test completed with Time Tool")

    # tools = [get_current_time]
    # print("normally adding tools: ", tools)

    # printt("Adding MCP Tools")
    # registry_file = "registry.json"
    # with open(registry_file, "r") as f:
    #     registry = json.load(f)


    # mcp_client = MultiServerMCPClient(
    #     registry['mcpServers']
    # )

    # tools = await mcp_client.get_tools()
    # print("tools from MCP: ", tools)
    # print("Adding MCP tools...")
    # agent_model.add_tools(tools)
    # print("now agentic tools: ", agent_model.list_tools())
    # messages = "Show me your tools now"
    # await agent_model.astream(messages, path_output="./output")

    # printt("Test completed with MCP Tools")
    # printt("Adding Docker MCP Tools")

    # print("Starting MCP client...")
    # Config = McpServerConfig(
    #     transport="stdio",
    #     name="docker_mcp",
    #     command="docker",
    #     args=["run", "--rm", "-i", "mcp/playwright"],
    #     # args=[mcp gateway run --servers="fetch, playwright"],
    #     # args=["mcp", "gateway", "run", "--servers=playwright"],
    # )
    # mcp_hub = McpHub()
    # try:
    #     session: ClientSession = await mcp_hub.connect(Config)
    #     print("Loading tools from Docker MCP...")
    #     tools = await load_mcp_tools(session)
    #     print("tools from Docker MCP: ", tools)
    #     agent_model = AgentModel(model=llm, tools=tools, system_prompt_content="You are a helpful assistant. always checking your tools.")
    #     print("now agentic tools: ", agent_model.list_tools())
    #     messages = "please show me your tools."
    #     await agent_model.astream(messages, path_output="./output")
    #     printt("Test completed with Docker MCP Tools")
    # finally:
    #     await mcp_hub.close()
    mcp_config = McpServerConfig(
        name="docker_mcp",
        command="docker",
        args=["mcp", "gateway", "run", "--servers=fetch,playwright,time"],
    )
    mcp_hub = McpHub()
    session: ClientSession = await mcp_hub.connect(mcp_config)

    # print("tools: ", )
    tools = await load_mcp_tools(session)
    print("tools from Docker MCP: ", tools)
    agent = AgentModel(model=llm, tools=tools, system_prompt_content="You are a helpful assistant. always checking your tools.")
    print("now agentic tools: ", agent.list_tools())
    messages = "please use tools fetch to get https://www.example.com and tell me the title of the page."
    try:
        await agent.astream(messages, path_output="./output")
    except Exception as e:
        print(f"Error during agent execution: {e}")
    await mcp_hub.close()

if __name__ == "__main__":
    asyncio.run(main())