from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text
from rich.traceback import install
import json
import time
import asyncio
install()

console = Console()

def mock_stream_response(user_input):
    # Simulate a streaming API response
    # split tokens by space for demonstration
    tokens = user_input.split(" ")
    for token in tokens:
        response = f"{token}"
        yield response

if __name__ == "__main__":
    # loop stream message inside message box
    user_input = """
```curl
think think...
```
# Tell me a story about a brave knight who saves a village from a dragon. Make it exciting and full of adventure.
### Make sure to include vivid descriptions and a satisfying conclusion.
- Always include source URLs in your findings
- Keep findings concise but informative
### example table
| Feature | Description | Status |
|---------|-------------|--------|
| Streaming | Real-time token output | ✓ Active |
| Markdown | Rich text formatting | ✓ Active |
| Async | Non-blocking execution | ✓ Active |
    """
    markdown = Markdown(f"**User:** {user_input}\n\n**Assistant:** ")
    async def stream_response():
        response_text = ""
        for token in mock_stream_response(user_input):
            response_text += token + " "
            markdown = Markdown(f"**Assistant:** {response_text}")
            live.update(Panel(markdown, title="Chat Stream", border_style="blue"))
            await asyncio.sleep(0.2)

    # with Live(Panel(markdown, title="Chat Stream", border_style="blue"), console=console, refresh_per_second=4) as live:
    #     asyncio.run(stream_response())
    live = Live(Panel(markdown, title="Chat Stream", border_style="blue"), console=console, refresh_per_second=4)
    live.start()
    asyncio.run(stream_response())
    # live.stop()