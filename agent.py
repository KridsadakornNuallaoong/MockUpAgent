import os
from datetime import datetime
from typing import Union

from langchain.agents import AgentState, create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.messages import (AIMessage, AIMessageChunk, AnyMessage,
                                     ToolMessage)
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

from model.custom_model_01 import llm
from research_agent.prompts import (RESEARCH_WORKFLOW_INSTRUCTIONS,
                                    RESEARCHER_INSTRUCTIONS,
                                    SUBAGENT_DELEGATION_INSTRUCTIONS)
from research_agent.tools import tavily_search, think_tool
from tools.general_tools import (add_two_numbers, divide_two_numbers,
                                 multiply_two_numbers, subtract_two_numbers)
from tools.secure_tools import (base64_decode, base64_encode, dir_list,
                                hash_string)
from tools.time_tools import get_current_time
from utils.stream.context_decoder import (decode_message_chunk,
                                          stream_context_decoder)

# TODO: Load system prompt from file
prompt_path = "./prompts"

system_prompt_path = os.path.join(prompt_path, "system.txt")
with open(system_prompt_path, "r") as f:
    system_prompt_content = f.read()

system_prompt_content += "\n\n"
system_prompt_content += RESEARCH_WORKFLOW_INSTRUCTIONS
system_prompt_content += "\n\n"
system_prompt_content += "=" * 80
system_prompt_content += "\n\n"
system_prompt_content += SUBAGENT_DELEGATION_INSTRUCTIONS.format(
    max_concurrent_research_units=3,
    max_researcher_iterations=3,
)
system_prompt_content += "\n\n"
system_prompt_content += RESEARCHER_INSTRUCTIONS.format(date=datetime.now().strftime("%Y-%m-%d"))

# TODO: Create agent state for maintaining context
class CustomAgentState(AgentState):
    user_id: str = "default_user"
    
# TODO: Create agent without middleware and checkpointer for faster response during testing
current_agent = "ResearchAgent"
agent = create_agent(
    model=llm,
    tools=[
        get_current_time, 
        base64_encode, 
        base64_decode, 
        hash_string, 
        add_two_numbers, 
        subtract_two_numbers, 
        multiply_two_numbers, 
        divide_two_numbers,
        dir_list,
        tavily_search,
        think_tool,
    ],
    state_schema=CustomAgentState,
    store=InMemoryStore(),
    checkpointer=InMemorySaver(),
    system_prompt=system_prompt_content,
    name="ResearchAgent",
)

os.system('cls' if os.name == 'nt' else 'clear')

# TODO: RunnableConfig for threading
config: RunnableConfig = {
    "configurable": {
        "thread_id": "1",
    }
}

time = ""
message_chunk = ""
path_output = "./output"

def output_to_file(time: str, messages_chunk: str) -> None:
    os.makedirs(path_output, exist_ok=True)
    with open(f"{path_output}/output_{time}.md", "a", encoding="utf-8") as f:
        f.write(str(messages_chunk))

def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.content:
        messages_chunk = token.content
        print(messages_chunk, end='', flush=True)
        output_to_file(time, messages_chunk)
    if token.additional_kwargs:
        messages_chunk = token.additional_kwargs.get('reasoning_content', '')
        print(messages_chunk, end='', flush=True)
        output_to_file(time, messages_chunk)

def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"\nTool calls: {message.tool_calls}")
        print(f"Reason explain: {message.additional_kwargs.get('reasoning_content', '')}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content}\n")

current_agent = "ResearchAgent"
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
                    _render_message_chunk(token)  
            if stream_mode == "updates":
                for source, update in data.items():
                    if source in ("model", "tools"):  # `source` captures node name
                        _render_completed_message(update["messages"][-1])  
            
        print("\n\n")
    
    except KeyboardInterrupt:
        print("\nExiting the chat.")
        break