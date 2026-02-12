import os
from datetime import datetime
from urllib.request import urlopen

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from deepagents.middleware import MemoryMiddleware, SkillsMiddleware
from deepagents.middleware.skills import _list_skills
from dotenv import load_dotenv
from langchain.chat_models import BaseChatModel, init_chat_model
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
                                          _render_message)

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Current working directory: {PARENT_DIR}")
tools = [
    get_current_time,
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
    # "description": "Delegate research to the sub-agent researcher. The sub-agent is responsible for conducting in-depth research on specific topics as assigned by the main agent. It should utilize available tools to gather accurate and up-to-date information.",
    "description": """
    ALWAYS use this first to research any topic before writing content.
    Searches the web for current information, statistics, and sources.
    When delegating, tell it the topic AND the file path to save results
    (e.g., 'Research renewable energy and save to research/renewable-energy.md').
    """,
    # "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=get_current_time.run("")),
    "system_prompt": """
    You are a research assistant. You have access to web_search and write_file tools.

    ## Your Tools
    - web_search(query, max_results=5, topic="general") - Search the web
    - write_file(file_path, content) - Save your findings

    ## Your Process
    1. Use web_search to find information on the topic
    2. Make 2-3 targeted searches with specific queries
    3. Gather key statistics, quotes, and examples
    4. Save findings to the file path specified in your task

    ## Important
    - The user will tell you WHERE to save the file - use that exact path
    - Always include source URLs in your findings
    - Keep findings concise but informative
    """,
    "tools": [tavily_search],
    "model": "ollama:qwen3",
}


research_instructions = f"""\
You are an expert researcher. Your job is to conduct \
thorough research, and then write a polished report. \
today is : {get_current_time.run("")}
"""

skill_url = "https://raw.githubusercontent.com/langchain-ai/deepagentsjs/refs/heads/main/examples/skills/langgraph-docs/SKILL.md"
with urlopen(skill_url) as response:
    skill_content = response.read().decode('utf-8')

skills_files = {
    "/skills/langgraph-docs/SKILL.md": skill_content
}

listed_skills = _list_skills(
    backend=FilesystemBackend(root_dir="./"),
    source_path="./skills/"
)

print(f"Listed skills from ./skills/blog-post: {listed_skills}")

# TODO: Create agent state for maintaining context
agent = create_deep_agent(
    model=llm,
    tools=tools,
    # backend=FilesystemBackend(root_dir="./"),
    system_prompt=research_instructions,
    subagents=[research_sub_agent],
    memory=["./AGENTS.md"],           # Loaded by MemoryMiddleware
    skills=["./skills/"]
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
            {
                "messages": messages,
                "files": skills_files,
            },
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
                    _render_message(token, time, path_output)
                    # print(token.content, end="", flush=True)
            if stream_mode == "updates":
                for source, update in data.items():
                    if source in ("model", "tools"):
                        # print(f"\n[{source.upper()} UPDATE]: {update}")
                        _render_completed_message(update["messages"][-1])  
        print("\n")
    
    except KeyboardInterrupt:
        print("\nExiting the chat.")
        break