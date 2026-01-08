import base64
import hashlib

from langchain.tools import tool


@tool('base64_encode', return_direct=False)
def base64_encode(raw_str: str) -> str:
    """Encodes a string to base64 and returns the encoded string"""
    encoded_bytes = base64.b64encode(raw_str.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

@tool('base64_decode', return_direct=False)
def base64_decode(encoded_str: str) -> str:
    """Decodes a base64 encoded string and returns the decoded string"""
    decoded_bytes = base64.b64decode(encoded_str)
    return decoded_bytes.decode('utf-8')

@tool('hash_string', return_direct=False)
def hash_string(raw_str: str) -> str:
    """Hashes a string using SHA256 and returns the hexadecimal digest"""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(raw_str.encode('utf-8'))
    return sha256_hash.hexdigest()

@tool('dir_list', return_direct=False)
def dir_list(path: str) -> str:
    """Lists files and directories in the given path"""
    import os
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except Exception as e:
        return str(e)