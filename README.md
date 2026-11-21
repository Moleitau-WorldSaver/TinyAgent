# TinyAgent

TinyAgent is a small synchronous agent loop for experimenting with structured model tool calls. It uses an OpenAI-compatible chat completions endpoint and Python's standard library.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install -e .
copy config.example.toml .tinyagent.toml   # Windows
cp config.example.toml .tinyagent.toml     # macOS/Linux
```

Edit `.tinyagent.toml` with a local API key and model. The file is ignored by Git. You can also set `TINYAGENT_API_KEY`, `TINYAGENT_BASE_URL`, `TINYAGENT_MODEL`, and `TINYAGENT_TIMEOUT_SECONDS`.

## Run

```bash
python -m tinyagent.cli "Say hello"
tinyagent "Use the echo tool when appropriate"
```

The included `echo` tool demonstrates the full path. The model receives the user message and registered tool schemas, the loop validates and executes structured calls, appends each tool result to the conversation, and continues until the model returns text or 50 decision rounds are reached.

## Test

```bash
python -m unittest discover -s tests -v
```

Tests use a fake model and deterministic tools, so they never need a real API key or network access. Unknown tools, invalid arguments, tool failures, direct text responses, multi-step calls, configuration errors, and the round limit are covered.

## Scope

This first version deliberately leaves streaming, parallel tool calls, persistence, RAG, web UI, retries, permissions, and multi-agent orchestration for later issues.


