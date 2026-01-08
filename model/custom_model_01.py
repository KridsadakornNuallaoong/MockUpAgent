from langchain_ollama import ChatOllama

# TODO: Configure custom model parameters
llm = ChatOllama(
    model="Qwen3",
    # cache="./cache/ollama",
    temperature=0.1,
    num_predict=2048,
    disable_streaming=False,
    # num_gpu=1,
    # num_thread=8,
)