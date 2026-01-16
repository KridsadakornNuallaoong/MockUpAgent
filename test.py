import asyncio
import json
import os
from datetime import datetime

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.config import RunnableConfig

from agent_model import AgentModel
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
    registry_file = "registry.json"
    with open(registry_file, "r") as f:
        registry = json.load(f)


    mcp_client = MultiServerMCPClient(
        registry['mcpServers']
    )

    tools = await mcp_client.get_tools()
    print("tools from MCP: ", tools)
    # print("Adding MCP tools...")
    # agent_model.add_tools(tools)
    # print("now agentic tools: ", agent_model.list_tools())
    # messages = "Show me your tools now"
    # await agent_model.astream(messages, path_output="./output")
    # printt("Test completed with MCP Tools")

if __name__ == "__main__":
    asyncio.run(main())