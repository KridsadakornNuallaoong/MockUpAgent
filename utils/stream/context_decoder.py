
# context decoder
import os

from langchain_core.messages import (AIMessage, AIMessageChunk, AnyMessage,
                                     ToolMessage)

from utils.logger.logger import logger


def output_to_file(time: str, messages_chunk: str, path_output: str) -> None:
    os.makedirs(path_output, exist_ok=True)
    with open(f"{path_output}/output_{time}.md", "a", encoding="utf-8") as f:
        f.write(str(messages_chunk))

def _render_message_chunk(token: AIMessageChunk, time: str, path_output: str) -> None:
    if token.content:
        messages_chunk = token.content
        print(messages_chunk, end='', flush=True)
        output_to_file(time, messages_chunk, path_output)
    if token.additional_kwargs:
        messages_chunk = token.additional_kwargs.get('reasoning_content', '')
        print(messages_chunk, end='', flush=True)
        output_to_file(time, messages_chunk, path_output)

def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"\nTool calls: {message.tool_calls}")
        print(f"Reason explain: {message.additional_kwargs.get('reasoning_content', '')}")
        logger.info(f"AI Message completed with tool calls: {message}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content}\n")
        logger.info(f"Tool Message completed with content: {message}")