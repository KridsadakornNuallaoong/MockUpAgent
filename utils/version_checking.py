import accelerate
import fastapi
import gradio
import huggingface_hub
import langchain
import langchain_huggingface
import markdownify
import mcp
import ollama
import qdrant_client
import tavily
import torch
import transformers
import uvicorn


def check_versions():
    modules = {
        'langchain': langchain,
        'langchain_huggingface': langchain_huggingface,
        'transformers': transformers,
        'torch': torch,
        'accelerate': accelerate,
        'gradio': gradio,
        'uvicorn': uvicorn,
        'fastapi': fastapi,
        'huggingface_hub': huggingface_hub,
        'mcp': mcp,
        'ollama': ollama,
        'qdrant_client': qdrant_client,
        'markdownify': markdownify,
        'tavily': tavily,
    }
    
    for name, module in modules.items():
        version = getattr(module, '__version__', 'unknown')
        print(f"{name}: {version}")

if __name__ == "__main__":
    check_versions()
