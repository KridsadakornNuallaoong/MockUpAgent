from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.checkpoint.memory import InMemorySaver as Checkpointer
from langgraph.store.memory import InMemoryStore as Store

from agent_model import AgentModel
from mcp_hub.mcphub import McpHub, McpServerConfig
from model.ollama.custom_model_01 import llm


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await mcp_hub.close()

# create FastAPI app and favicon path ./favicon.ico
app = FastAPI(lifespan=lifespan)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    from fastapi.responses import FileResponse
    return FileResponse("./favicon.ico")

tools: list[BaseTool] = []
agent_model = AgentModel(model=llm, tools=tools, system_prompt_content="You are a helpful assistant. always checking your tools available or not.", checkpointer=Checkpointer(), store=Store())
mcp_hub = McpHub()
class DockerMcpServer:
    def __init__(self, servers: list[str] = ["fetch"]):
        self.servers = servers
    
    def get_args(self) -> list[str]:
        return ["mcp", "gateway", "run", f'--servers={",".join(self.servers)}']
    
    def set_servers(self, servers: list[str]):
        self.servers = servers

    def delete_server(self, server: str):
        if server in self.servers:
            self.servers.remove(server)
docker_mcp_server = DockerMcpServer()

@app.get("/")
async def root():
    return {"message": "Welcome to the AgentModel FastAPI server!"}

@app.get("/tools")
async def get_tools():
    
    return {"tools": agent_model.list_tools()}

@app.post("/chat")
async def chat(payload: dict):
    user_input = payload.get("message", "")
    print("Received user input: ", user_input)
    config = {
        "configurable": {
            "thread_id": "1",
        }
    }

    print(docker_mcp_server.get_args())
    print("Loaded MCP tools: ", tools)
    agent_model.add_tools(tools)
    agent_model.set_config(config)
    
    return StreamingResponse(
        content=agent_model.astream_server_render(messages=user_input, path_output="./output"),
        media_type="text/event-stream"
    )
    
@app.post("/mcp_server")
async def mcp_config(payload: dict):
    # receive payload : [str, str, ...str] : name, command, args
    req = payload.get("mcp_server", [])
    # update global docker_mcp_server
    global docker_mcp_server
    docker_mcp_server.set_servers(req)
    await mcp_hub.close()
    session = await mcp_hub.connect(McpServerConfig(
        name="docker_mcp",
        command="docker",
        args=docker_mcp_server.get_args(),
    ))

    global tools
    tools = await load_mcp_tools(session)
    agent_model.set_tools(tools)
    return {"status": "MCP server configuration updated", "servers": docker_mcp_server.servers}

if __name__ == "__main__":
    docker_mcp_server.set_servers(["fetch"])
    uvicorn.run(app, host="127.0.0.1", port=8000)