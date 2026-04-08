---
title: Prompt Optimizer RL Environment
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Prompt Optimizer RL Environment

An RL environment where an agent iteratively rewrites system prompts to make a fixed judge LLM produce specific structured outputs. Reward is fully deterministic Python verification.

## How It Works

1. Agent receives a task description and an initial bad prompt
2. Agent rewrites the prompt to steer the judge LLM toward the target output
3. Python verifiers score the judge's response deterministically
4. Agent gets up to 8 steps to maximize the score

## Tasks

| Seed | Task ID | Type | Description |
|------|---------|------|-------------|
| 0 | `json_user_profile` | JSON Keys | Output JSON with `name`, `age`, `city`, `email` |
| 1 | `json_product_listing` | JSON Keys | Output JSON with `product_name`, `price`, `in_stock`, `category` |
| 2 | `code_fibonacci` | Code Tests | Python `fibonacci(n)` passing 4 unit tests |
| 3 | `code_palindrome` | Code Tests | Python `is_palindrome(s)` passing 4 unit tests |
| 4 | `phrase_match_pasta` | Phrase Match | Numbered steps response containing required phrases |
| 5 | `length_range_haiku` | Length Range | Response within exact character limits, no forbidden words |
| 6 | `refusal_medical` | Refusal | Must refuse and include required refusal signals |

## Verifier Types

- **json_keys** — Parses JSON, checks required keys and types
- **code_tests** — Extracts and executes Python code, runs unit tests
- **phrase_match** — Checks for required phrases in response
- **length_range** — Checks character count and forbidden patterns
- **refusal** — Checks for refusal signals and absence of harmful content

## API Endpoints

```
POST /reset   # Start new episode (accepts optional seed 0-6 to select task)
POST /step    # Submit rewritten prompt as action
GET  /health  # Health check
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `API_KEY` | LLM API key (injected by judges) |
| `HF_TOKEN` | Hugging Face token (fallback) |
| `API_BASE_URL` | LLM API base URL (injected by judges) |
| `MODEL_NAME` | Model to use (default: `Qwen/Qwen2.5-72B-Instruct`) |
| `ENV_BASE_URL` | Environment server URL for inference.py |

## Scoring

- Each step returns a reward in `[0, 1]`
- Score per episode = max reward across all steps
- Final score clamped to `(0.01, 0.99)` — strictly between 0 and 1
- Episode succeeds when score ≥ 0.5
