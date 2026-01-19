from collections.abc import Callable, Sequence
from datetime import datetime
from typing import Any

from langchain.agents import create_agent
from langchain.chat_models.base import BaseChatModel
from langchain.messages import AIMessageChunk
from langchain.tools import BaseTool
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver as Checkpointer
from langgraph.store.memory import InMemoryStore as Store

from utils.stream.context_decoder import (_arender_server_completed_message,
                                          _arender_server_message_chunk,
                                          _render_completed_message,
                                          _render_message_chunk,
                                          _render_server_completed_message,
                                          _render_server_message_chunk)


def now_isoformat():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

class AgentModel:
    def __init__(self, model, tools: BaseTool = [], system_prompt_content: str = "", checkpointer=Checkpointer(), store=Store(), name: str = "AgentModel"):
        self.name = name
        self.model : str | BaseChatModel = model
        self.tools : Sequence[BaseTool | Callable | dict[str, Any]] | None = tools
        self.system_prompt_content = system_prompt_content
        self.ShortTermMemory = checkpointer
        self.LongTermMemory = store
        self.config = RunnableConfig({
                            "configurable": {
                                "thread_id": "1",
                            }
                        })

    def _get_agent(self):
        return create_agent(
                model=self.model,
                tools=self.tools,
                system_prompt=self.system_prompt_content,
                checkpointer=self.ShortTermMemory,
                store=self.LongTermMemory,
                name=self.name,
            )
    
    def add_tool(self, new_tool: Sequence[BaseTool | Callable | dict[str, Any]] | None = []):
        try:
            self.tools.append(new_tool)
        except Exception as e:
            print("Error adding tool: ", e)

    def add_tools(self, new_tools: Sequence[BaseTool | Callable | dict[str, Any]] | None = []):
        try:
            self.tools.extend(new_tools)
        except Exception as e:
            print("Error adding tools: ", e)
    
    def set_tools(self, new_tools: Sequence[BaseTool | Callable | dict[str, Any]] | None = []):
        self.tools = new_tools
    
    def list_tools(self):
        return [tool.name for tool in self.tools]
    
    def set_model(self, new_model : str | BaseChatModel):
        self.model = new_model

    def set_config(self, new_config):
        self.config = new_config

    def run(self, input_text):
        return self._get_agent().invoke(
            {"messages": [("user", input_text)]},
            config=self.config,
        )

    async def astream(self, messages: str, path_output="output_stream", verbose: bool = True, debug: bool = False):
        time = now_isoformat()
        async for stream_mode, data in self._get_agent().astream(
                {"messages": messages},
                config=self.config,
                stream_mode=["messages", "updates"],
                tool_choice="auto",
                debug=debug,
                subgraph=True,
            ):
                if stream_mode == "messages":
                    token, metadata = data
                    if tags := metadata.get("model", []):  
                        this_agent = tags[0]  
                        if this_agent != current_agent:  
                            print(f"🤖 {this_agent}: ")  
                            current_agent = this_agent  
                    if isinstance(token, AIMessageChunk):
                        # print("Rendering message chunk...")
                        _render_message_chunk(token, time, path_output, verbose)
                if stream_mode == "updates":
                    for source, update in data.items():
                        if source in ("model", "tools"):
                            # print("Rendering completed message...")
                            _render_completed_message(update["messages"][-1], verbose)

    def stream_server_render(self, messages: str, path_output="output_stream", verbose: bool = True, debug: bool = False):
        time = now_isoformat()
        for stream_mode, data in self._get_agent().stream(
                {"messages": messages},
                config=self.config,
                stream_mode=["messages", "updates"],
                tool_choice="auto",
                debug=debug,
                subgraph=True,
            ):
                if stream_mode == "messages":
                    token, metadata = data
                    if tags := metadata.get("model", []):  
                        this_agent = tags[0]  
                        if this_agent != current_agent:  
                            print(f"🤖 {this_agent}: ")  
                            current_agent = this_agent  
                    if isinstance(token, AIMessageChunk):
                        # print("Rendering message chunk...")
                        for chunk in _render_server_message_chunk(token, time, path_output, verbose):
                            yield f'{chunk}'
                if stream_mode == "updates":
                    for source, update in data.items():
                        if source in ("model", "tools"):
                            # print("Rendering completed message...")
                            for chunk in _render_server_completed_message(update["messages"][-1], verbose):
                                yield f'{chunk}'
    
    async def astream_server_render(self, messages: str, path_output="output_stream", verbose: bool = True, debug: bool = False):
        time = now_isoformat()
        async for stream_mode, data in self._get_agent().astream(
                {"messages": messages},
                config=self.config,
                stream_mode=["messages", "updates"],
                tool_choice="auto",
                debug=debug,
                subgraph=True,
            ):
                if stream_mode == "messages":
                    token, metadata = data
                    if tags := metadata.get("model", []):  
                        this_agent = tags[0]  
                        if this_agent != current_agent:  
                            print(f"🤖 {this_agent}: ")  
                            current_agent = this_agent  
                    if isinstance(token, AIMessageChunk):
                        # print("Rendering message chunk...")
                        async for chunk in _arender_server_message_chunk(token, time, path_output, verbose):
                            yield f'{chunk}'
                if stream_mode == "updates":
                    for source, update in data.items():
                        if source in ("model", "tools"):
                            # print("Rendering completed message...")
                            async for chunk in _arender_server_completed_message(update["messages"][-1], verbose):
                                yield f'{chunk}'