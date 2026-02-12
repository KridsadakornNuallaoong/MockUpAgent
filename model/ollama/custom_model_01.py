from langchain_core.language_models.model_profile import ModelProfile
from langchain_ollama import ChatOllama
from ollama import Client

ollama_key = "8ea28e74ae344b2e8dd9ae5976da722e.rUz5UDYujAQL-uBrsv-9Uiv2"

# TODO: Configure custom model parameters
# llm = ChatOllama(
#     model="Qwen3",
#     temperature=0.1,
#     num_predict=2048,
#     disable_streaming=False,
#     # num_gpu=1,
#     # num_thread=8,
# )

model="Qwen3"
# model="Qwen3"
# model="nemotron-3-nano"
# model="kimi-k2.5:cloud"

profile_config = ModelProfile(
    max_input_tokens=32768,
    max_output_tokens=32768,
    reasoning_output=True,
    image_inputs=True,
    image_url_inputs=True,
    tool_calling=True,
    tool_choice=True,
)

llm = ChatOllama(
    model=model,
    temperature=0.3,
    num_predict=32768,
    disable_streaming=False,
    base_url="http://localhost:11434",
    # num_gpu=1,
    profile=profile_config,
    reasoning=True,
)

# Alternative configuration for a different server
# llm = ChatOllama(
#     model="nemotron-3-nano",
#     temperature=0.1, 
#     num_predict=32768,
#     disable_streaming=False,
#     base_url="http://atlas:admin1234@atlas-jetson:11434",
#     num_gpu=1,
#     num_thread=20,
#     profile=profile_config,
#     reasoning=True,
# )