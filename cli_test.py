# http://localhost:8000/chat

# call api
import json

import requests

url = "http://localhost:8000/chat"
payload = {
    "message": "What time is it now?"
}

# async receive streaming response
response = requests.post(url, json=payload, stream=True)
def stream(response):
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith("data: "):
                yield decoded_line[6:]

for message in stream(response):
    print(message, end='', flush=True)