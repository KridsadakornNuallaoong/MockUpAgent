
# context decoder
import os

from langchain_core.messages import (AIMessage, AIMessageChunk, AnyMessage,
                                     ToolMessage)

from utils.logger.logger import logger


def output_to_file(time: str, messages_chunk: str, path_output: str) -> None:
    os.makedirs(path_output, exist_ok=True)
    with open(f"{path_output}/output_{time}.md", "a", encoding="utf-8") as f:
        f.write(str(messages_chunk))

def _render_message_chunk(token: AIMessageChunk, time: str, path_output: str, verbose: bool = True):
    if token.content:
        messages_chunk = token.content
        if verbose:
            print(messages_chunk, end='', flush=True)
        output_to_file(time, messages_chunk, path_output)

    if token.additional_kwargs:
        messages_chunk = token.additional_kwargs.get('reasoning_content', '')
        if verbose:
            print(messages_chunk, end='', flush=True)
        output_to_file(time, messages_chunk, path_output)

def _render_completed_message(message: AnyMessage, verbose: bool = True) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        if verbose:
            print(f"\nTool calls: {message.tool_calls}")
            print(f"Reason explain: {message.additional_kwargs.get('reasoning_content', '')}")
        logger.info(f"AI Message completed with tool calls: {message}")
    if isinstance(message, ToolMessage):
        if verbose:
            print(f"Tool response: {message.content}\n")
        logger.info(f"Tool Message completed with content: {message}")

def _render_server_message_chunk(token: AIMessageChunk, time: str, path_output: str, verbose: bool = True):
    if token.content:
        messages_chunk = token.content
        if verbose:
            print(messages_chunk, end='', flush=True)
        output_to_file(time, messages_chunk, path_output)
        yield f'data: {messages_chunk}\n\n'

    if token.additional_kwargs:
        messages_chunk = token.additional_kwargs.get('reasoning_content', '')
        if verbose:
            print(messages_chunk, end='', flush=True)
        output_to_file(time, messages_chunk, path_output)
        yield f'data: {messages_chunk}\n\n'

def _render_server_completed_message(message: AnyMessage, verbose: bool = True):
    if isinstance(message, AIMessage) and message.tool_calls:
        if verbose:
            print(f"\nTool calls: {message.tool_calls}")
            print(f"Reason explain: {message.additional_kwargs.get('reasoning_content', '')}")
            yield f'data: \nTool calls: {message.tool_calls}\n\n'
            logger.info(f"AI Message completed with tool calls: {message}")
    if isinstance(message, ToolMessage):
        if verbose:
            print(f"Tool response: {message.content}\n")
            logger.info(f"Tool Message completed with content: {message}")