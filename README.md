# TinyAgent

TinyAgent is a small synchronous agent loop for experimenting with structured model tool calls. It uses an OpenAI-compatible chat completions endpoint and Python's standard library. DeepSeek is supported with thinking mode enabled.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install -e .
copy config.example.toml .tinyagent.toml   # Windows
cp config.example.toml .tinyagent.toml     # macOS/Linux
```

Edit `.tinyagent.toml` with a local API key and model. The file is ignored by Git. The example uses DeepSeek at `https://api.deepseek.com` with `deepseek-chat`. You can also set `TINYAGENT_PROVIDER`, `TINYAGENT_API_KEY`, `TINYAGENT_BASE_URL`, `TINYAGENT_MODEL`, and `TINYAGENT_TIMEOUT_SECONDS`.

## Run

```bash
python -m tinyagent.cli "Say hello"
tinyagent "Use the calculator tool when appropriate"
```

The default catalog includes `bash`, `read`, `edit`, `write`, `calculator`, `search`, `read_docs`, `todo`, and `weather`. The first four are side-effect-free simulations. Search and weather use replaceable offline providers by default. `read_docs` is bounded to `docs/`. Multiple tool calls run concurrently and their results are written back in the model's original order. The `echo` tool remains available in the CLI as a compatibility example.

## Test

```bash
python -m unittest discover -s tests -v
```

Tests use a fake model and deterministic tools, so they never need a real API key or network access. They cover the catalog schemas, mock providers, docs boundary, calculator, parallel calls, unknown tools, invalid arguments, tool failures, direct text responses, multi-step calls, DeepSeek payload and thinking parsing, configuration errors, and the round limit. A real DeepSeek smoke test requires a local key and is not run by the test suite.

## Scope

This version deliberately leaves streaming, persistence, RAG, web UI, retries, permissions, and multi-agent orchestration for later issues. Bash, edit, and write do not perform real side effects.

