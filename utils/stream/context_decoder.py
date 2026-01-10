
# context decoder
from langchain_core.messages import (AIMessageChunk, HumanMessageChunk,
                                     SystemMessageChunk, ToolMessageChunk)


# create structured decoder for return
class stream_context_decoder:
    def __init__(self, chunk: tuple = (), title: str = ""):
        self.chunk = chunk
        self.title = title

def decode_message_chunk(chunk: tuple) -> str:
    """Decode a message chunk into a string representation."""
    if isinstance(chunk, AIMessageChunk):
        return stream_context_decoder(chunk=chunk, title="AIMessageChunk")
    elif isinstance(chunk, ToolMessageChunk):
        return stream_context_decoder(chunk=chunk, title="ToolMessageChunk")
    elif isinstance(chunk, HumanMessageChunk):
        return stream_context_decoder(chunk=chunk, title="HumanMessageChunk")
    elif isinstance(chunk, SystemMessageChunk):
        return stream_context_decoder(chunk=chunk, title="SystemMessageChunk")
    else:
        return stream_context_decoder(chunk=chunk, title="UnknownChunk")