import os
from datetime import datetime
from typing import Literal
from xml.parsers.expat import model

from deepagents import create_deep_agent
from deepagents.middleware.patch_tool_calls import PatchToolCallsMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from dotenv import load_dotenv
from langchain.agents import AgentState
from langchain.tools import tool
from langchain_core.runnables import RunnableConfig
from tavily import TavilyClient

from model.custom_model_01 import llm, llm_Q
from research_agent.prompts import (RESEARCH_WORKFLOW_INSTRUCTIONS,
                                    RESEARCHER_INSTRUCTIONS,
                                    SUBAGENT_DELEGATION_INSTRUCTIONS)
from research_agent.tools import tavily_search, think_tool
from tools.time_tools import get_current_time

tavily_client = TavilyClient(api_key="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")

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

# Limits
max_concurrent_research_units = 3
max_researcher_iterations = 3

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Combine orchestrator instructions (RESEARCHER_INSTRUCTIONS only for sub-agents)
INSTRUCTIONS = (
    RESEARCH_WORKFLOW_INSTRUCTIONS
    + "\n\n"
    + "=" * 80
    + "\n\n"
    + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
        max_concurrent_research_units=max_concurrent_research_units,
        max_researcher_iterations=max_researcher_iterations,
    )
)

# # Create research sub-agent
# research_sub_agent = {
#     "name": "research-agent",
#     "description": "Delegate research to the sub-agent researcher. The sub-agent is responsible for conducting in-depth research on specific topics as assigned by the main agent. It should utilize available tools to gather accurate and up-to-date information.",
#     "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
#     "tools": tools,
# }


research_instructions = """\
You are an expert researcher. Your job is to conduct \
thorough research, and then write a polished report. \
"""

# TODO: Create agent state for maintaining context
agent = create_deep_agent(
    model=llm,
    tools=[
        get_current_time,
        tavily_search,
        think_tool,
        internet_search,
    ],
    system_prompt=research_instructions,
    # middleware=[
    #     PatchToolCallsMiddleware()
    # ]
)

message = {
    'message': [
        {
            'role': 'user',
            'content': """Conduct comprehensive research on the topic of 'The impact of artificial intelligence on modern healthcare systems'. Provide a detailed report summarizing key findings, advancements, challenges, and future prospects in this field. Use credible sources and include relevant statistics or case studies to support your analysis.""",
        }
    ]
}

# TODO: RunnableConfig for threading
config: RunnableConfig = {
    "configurable": {
        "thread_id": "1",
    }
}

# TODO: Implement graceful exit
try:

    for chunk in agent.stream(
        message,
        config=config,
        stream_mode=["messages"],
        debug=True,
    ):
        # for step, data in chunk.items():
        #     print(f"step: {step}")
        #     print(f"content: {data['messages'][-1].content_blocks}\n")

        # example output: ('messages', (AIMessageChunk(content='The current date and time is 2024-06-15 12:34:56.', tool_call_chunks=[]),))
        content = chunk[1][0].content
        print(content, end='', flush=True)
        # write to file report output.md
        # os.makedirs("research_reports", exist_ok=True)
        # with open("research_reports/output.md", "a", encoding="utf-8") as f:
        #     f.write(content)

    print("\n\n")
    print("Research finished. You can start a new research or type 'exit' to quit.")

except KeyboardInterrupt:
    print("\nExiting the chat.")