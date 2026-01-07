import os

from langchain.agents import create_agent

from model.custom_model_01 import llm
from tools.general_tools import (add_two_numbers, divide_two_numbers,
                                 multiply_two_numbers, subtract_two_numbers)
from tools.secure_tools import base64_decode, base64_encode, hash_string
from tools.time_tools import get_current_time

# TODO: Load system prompt from file
prompt_path = "./prompts"

system_prompt_path = os.path.join(prompt_path, "system.txt")
with open(system_prompt_path, "r") as f:
    system_prompt_content = f.read()

# TODO: Create agent without middleware and checkpointer for faster response during testing
agent = create_agent(
    model=llm,
    tools=[
        get_current_time, 
        base64_encode, 
        base64_decode, 
        hash_string, 
        add_two_numbers, 
        subtract_two_numbers, 
        multiply_two_numbers, 
        divide_two_numbers
    ],
)

# agent = create_agent(
#     model=llm,
#     checkpointer=InMemorySaver(),
#     middleware=[
#         ModelCallLimitMiddleware(
#             thread_limit=10,
#             run_limit=10,
#         )
#     ],
#     debug=True,
#     tools=[
#         get_current_time, 
#         base64_encode, 
#         base64_decode, 
#         hash_string, 
#         add_two_numbers, 
#         subtract_two_numbers, 
#         multiply_two_numbers, 
#         divide_two_numbers
#     ],
# )

# TODO: Add system prompt to agent initialization 
prompt = [
    ("system", system_prompt_content),
]

# TODO: Implement graceful exit
while True:
    try:
        user_input = input("User: ")
        messages = prompt + [("user", user_input)]

        if user_input.lower() in ["exit", "quit", "bye", "!c"]:
            raise KeyboardInterrupt

        for chunk in agent.stream(
            {"messages": messages},
            {'tool_choice': 'auto'},
            stream_mode=["messages"],
        ):
            # for step, data in chunk.items():
            #     print(f"step: {step}")
            #     print(f"content: {data['messages'][-1].content_blocks}\n")

            # example output: ('messages', (AIMessageChunk(content='The current date and time is 2024-06-15 12:34:56.', tool_call_chunks=[]),))
            print(chunk[1][0].content, end='', flush=True)
        print("\n\n")
    
    except KeyboardInterrupt:
        print("\nExiting the chat.")
        break