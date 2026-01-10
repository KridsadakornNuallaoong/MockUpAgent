import langchain_core
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_name = "Qwen/Qwen3-14B"
cache_path = "./cache"

# TODO: load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
)

# TODO: create the pipeline and the llm
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.1,
    do_sample=True
)

# TODO: create the HuggingFacePipeline and ChatHuggingFace llm
n_pipe = HuggingFacePipeline(pipeline=pipe)
llm = ChatHuggingFace(
    pipeline=n_pipe,
    model_name=model_name,
    temperature=0.1,
    max_output_tokens=512,
    streaming=True,
)