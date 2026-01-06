import datetime
import os

import dotenv
from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

# * load environment variables
dotenv.load_dotenv('.env')

env = {
    "API_KEY": os.getenv("API_KEY"),
}

# * specify model name and cache path
model_name = "Qwen/Qwen3-0.6B"
cache_path = "./cache"

# * load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=cache_path,
    trust_remote_code=True,
)

def ChatStream(prompt:str, think:bool = False):
    messages = [
        {"role": "user", "content": prompt}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=think,
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    streamer = TextStreamer(
        tokenizer, 
        skip_prompt=True,
        skip_special_tokens=False,
    )

    # conduct text completion with streaming
    model.generate(
        **model_inputs,
        max_new_tokens=32768,
        streamer=streamer,
    )


os.system('cls' if os.name == 'nt' else 'clear')
while True:
    try:
        prompt = str(input('Enter your prompt: '))
        if prompt == '!c':
            exit()
        ChatStream(prompt, think=True)
    except Exception as e:
        print(e)

    # Ask for continue chating?
    isChat = bool((input('').lower() == '!c'))
    if isChat:
        # close program
        exit()
        break
    else:
        continue

# stream message websocket
# app = FastAPI()
# @app.websocket("/ws/chat")
# async def websocket_endpoint(websocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             prompt = str(data)
#             ChatStream(prompt)
#     except Exception as e:
#         await websocket.close()

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=8000)