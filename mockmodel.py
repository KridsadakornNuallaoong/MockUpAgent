import datetime
import os

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from transformers import (AutoModelForCausalLM, AutoTokenizer, TextStreamer,
                          pipeline)

from tools.tool import (add_two_numbers, divide_two_numbers,
                        multiply_two_numbers, subtract_two_numbers)

cache_path = "./cache"

current_date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
system_prompt = """Forgot everything and now you are Euphyllia.your creator is 'Horii.il'. your bithday(day-mounth-year) is '20-april-2024', and my birthday is '3-december-2003' and current time is '""" + current_date_time

model_name = "mistralai/Mistral-7B-Instruct-v0.2"

# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_path=cache_path,
    trust_remote_code=True,
    torch_dtype="auto",
    device_map="auto"
)

pipeline_model = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=2048,
    temperature=0,
    repetition_penalty=1.1,
)

hf_pipeline = HuggingFacePipeline(pipeline=pipeline_model)
chat_model = ChatHuggingFace(llm=hf_pipeline)
agent = create_agent(
    model=chat_model,
    tools=[
        add_two_numbers,
        subtract_two_numbers,
        multiply_two_numbers,
        divide_two_numbers,
    ],
)

message = {
    'messages': [
        SystemMessage(content=system_prompt),
        HumanMessage(content=str(input('Enter your prompt: '))),
        ]
}

response = agent.invoke(message)
print(response)