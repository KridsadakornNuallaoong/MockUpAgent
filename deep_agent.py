from datetime import datetime

from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain_core.messages import (AIMessage, AIMessageChunk, AnyMessage,
                                     ToolMessage)
from langchain_core.runnables import RunnableConfig

from model.ollama.custom_model_01 import llm
from research_agent.prompts import (RESEARCH_WORKFLOW_INSTRUCTIONS,
                                    RESEARCHER_INSTRUCTIONS,
                                    SUBAGENT_DELEGATION_INSTRUCTIONS)
from research_agent.tools import tavily_search, think_tool
from tools.secure_tools import base64_decode, base64_encode
from tools.time_tools import get_current_time
from utils.stream.context_decoder import (_render_completed_message,
                                          _render_message_chunk)

tools = [
    get_current_time,
    tavily_search,
    think_tool,
    base64_encode,
    base64_decode,
]

if load_dotenv(".env") is None:
    print("Failed to load .env file")


# Limits
max_concurrent_research_units = 3
max_researcher_iterations = 3

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
research_sub_agent = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. The sub-agent is responsible for conducting in-depth research on specific topics as assigned by the main agent. It should utilize available tools to gather accurate and up-to-date information.",
    "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=get_current_time.run("")),
    "tools": tools,
    "model": llm,
}


research_instructions = f"""\
You are an expert researcher. Your job is to conduct \
thorough research, and then write a polished report. \
today is : {get_current_time.run("")}
"""

# TODO: Create agent state for maintaining context
agent = create_deep_agent(
    model=llm,
    # tools=tools,
    system_prompt=research_instructions,
)

# TODO: RunnableConfig for threading
config: RunnableConfig = {
    "configurable": {
        "thread_id": "1",
    }
}

path_output = "./output"

# TODO: Implement graceful exit
while True:
    try:
        user_input = input("Enter your message: ")
        messages = [("user", user_input)]

        if user_input.lower() in ["exit", "quit", "bye", "!c"]:
            raise KeyboardInterrupt
        
        time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        user_message_log = f"[{time}] User: {user_input}\n"
        full_message = ""

        for stream_mode, data in agent.stream(
            {"messages": messages},
            config=config,
            stream_mode=["messages", "updates"],
            tool_choice="auto",
            # debug=True,
            subgraph=True
        ):
            if stream_mode == "messages":
                token, metadata = data
                if tags := metadata.get("model", []):  
                    this_agent = tags[0]  
                    if this_agent != current_agent:  
                        print(f"🤖 {this_agent}: ")  
                        current_agent = this_agent  
                if isinstance(token, AIMessageChunk):
                    _render_message_chunk(token, time, path_output)  
            if stream_mode == "updates":
                for source, update in data.items():
                    if source in ("model", "tools"):
                        _render_completed_message(update["messages"][-1])  
        print("\n")
    
    except KeyboardInterrupt:
        print("\nExiting the chat.")
        break