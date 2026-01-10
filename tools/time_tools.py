from datetime import datetime

from langchain.tools import tool


@tool('get_current_time', return_direct=False, description="Get the current system time.")
def get_current_time() -> str:
    """Get the current system time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")