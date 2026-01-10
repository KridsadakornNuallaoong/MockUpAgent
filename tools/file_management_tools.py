import os

from langchain.tools import tool


# 1.Text to file tool
@tool("text_to_file", return_direct=False)
def text_to_file(file_path: str, content: str) -> str:
    """Saves the given text content to a file at the specified path.

    Args:
        file_path: The path where the file will be saved.
        content: The text content to save in the file.

    Returns:
        A confirmation message indicating the file has been saved.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File saved successfully at {file_path}"
    except Exception as e:
        return f"Error saving file at {file_path}: {str(e)}"
    
# 2.File to text tool, define file type before reading
@tool("file_to_text", return_direct=False)
def file_to_text(file_path: str) -> str:
    """Reads the content of a file at the specified path and returns it as text.

    Args:
        file_path: The path of the file to read.
    Returns:
        The text content of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file at {file_path}: {str(e)}" 