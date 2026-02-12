import langchain_core
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_huggingface import (ChatHuggingFace, HuggingFaceEndpoint,
                                   HuggingFacePipeline)
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_name = "Qwen/Qwen3-0.6B"
cache_path = "./cache"

# TODO: load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# TODO: create the pipeline and the llm
pipe = pipeline(
    "text-generation",
    model=model_name,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.1,
    do_sample=True,
)

# TODO: create the HuggingFacePipeline and ChatHuggingFace llm
hf = HuggingFacePipeline(pipeline=pipe)
# n_pipe = HuggingFacePipeline.from_model_id(
#     model_id=model_name,
#     task="text-generation",
#     pipeline_kwargs=dict(
#         max_new_tokens=512,
#         do_sample=False,
#         repetition_penalty=1.03,
#     ),
# )

llm = ChatHuggingFace(
    llm=hf,
    model_name=model_name,
    temperature=0.1,
    max_output_tokens=512,
    streaming=True,
)