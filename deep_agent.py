import os
from datetime import datetime
from xml.parsers.expat import model

from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain.agents import AgentState
from langchain_core.runnables import RunnableConfig

from model.custom_model_01 import llm
from research_agent.prompts import (RESEARCH_WORKFLOW_INSTRUCTIONS,
                                    RESEARCHER_INSTRUCTIONS,
                                    SUBAGENT_DELEGATION_INSTRUCTIONS)
from research_agent.tools import tavily_search, think_tool

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

# Create research sub-agent
research_sub_agent = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
    "tools": [tavily_search, think_tool],
}

# TODO: Load system prompt from file
prompt_path = "./prompts"

system_prompt_path = os.path.join(prompt_path, "system.txt")
with open(system_prompt_path, "r") as f:
    system_prompt_content = f.read()

# TODO: Create agent state for maintaining context
class CustomAgentState(AgentState):
    user_id: str = "default_user"

agent = create_deep_agent(
    model=llm,
    tools=[tavily_search, think_tool],
    system_prompt=INSTRUCTIONS,
    subagents=[research_sub_agent],
)

message = {
    'message': [
        {
            'role': 'user',
            'content': 'Conduct research on the impact of AI in healthcare and provide a comprehensive report.'
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
        # debug=True,
    ):
        # for step, data in chunk.items():
        #     print(f"step: {step}")
        #     print(f"content: {data['messages'][-1].content_blocks}\n")

        # example output: ('messages', (AIMessageChunk(content='The current date and time is 2024-06-15 12:34:56.', tool_call_chunks=[]),))
        print(chunk[1][0].content, end='', flush=True)
    print("\n\n")
    print("Research finished. You can start a new research or type 'exit' to quit.")

except KeyboardInterrupt:
    print("\nExiting the chat.")