from langchain_core.language_models.model_profile import ModelProfile
from langchain_ollama import ChatOllama

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
# model="nemotron-3-nano"

profile_config = ModelProfile(
    max_input_tokens=32768,
    max_output_tokens=32768,
    reasoning_output=True,
)

llm = ChatOllama(
    model=model,
    temperature=0.5,
    num_predict=32768,
    disable_streaming=False,
    base_url="http://localhost:11434",
    # num_gpu=1,
    # num_thread=20,
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