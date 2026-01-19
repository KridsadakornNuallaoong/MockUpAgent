# Python Server Project Setup with uv and venv

## Prerequisites
- Python 3.13
- `uv` package manager installed

## Setup Steps

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install compile and get requirements.txt
```bash
uv pip compile pyproject.toml -o requirements.txt
```

### 4. Install Dependencies
```bash
uv pip install -r requirements.txt
```

### 5. Or add dependencies:
```bash
uv pip install flask  # or your server framework
```

### 6. Run Server
```bash
python main.py
```

## Project Structure
```
project/
├── venv/
├── main.py
├── requirements.txt
└── README.md
└── ...
```

## Tips
- Keep `requirements.txt` updated: `uv pip freeze > requirements.txt`
- Always activate venv before running commands
- Add `venv/` to `.gitignore`