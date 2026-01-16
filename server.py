import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain.messages import (AIMessageChunk, AnyMessage, HumanMessage,
                                SystemMessage, ToolMessage)

from agent_model import AgentModel
from model.ollama.custom_model_01 import llm
from tools.time_tools import get_current_time


async def streaming_generator(agent_model: AgentModel, user_input: str = "", config: dict = {}):
    async for stream_mode, data in agent_model._get_agent().astream(
                {"messages": user_input},
                config=config,
                stream_mode=["messages", "updates"],
                tool_choice="auto",
                # debug=True,
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
                        if token.content:
                            messages_chunk = token.content
                            print(messages_chunk, end='', flush=True)
                            yield f'data: {messages_chunk}\n\n'
                        if token.additional_kwargs:
                            messages_chunk = token.additional_kwargs.get('reasoning_content', '')
                            print(messages_chunk, end='', flush=True)
                            yield f'data: {messages_chunk}\n\n'

app = FastAPI()
agent_model = AgentModel(model=llm, tools=[get_current_time], system_prompt_content="You are a helpful assistant. always checking your tools.")

@app.post("/chat")
async def chat(payload: dict):
    user_input = payload.get("message", "")
    config = {
        "configurable": {
            "thread_id": "1",
        }
    }
    agent_model.set_config(config)
    
    return StreamingResponse(
        # streaming_generator(agent_model, user_input=user_input, config=config),
        agent_model.stream_server_render(messages=user_input, path_output="./output"),
        media_type="text/event-stream"
    )
    


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)