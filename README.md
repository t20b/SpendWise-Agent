# SpendWise-Agent

SpendWise-Agent is a FastAPI-based MVP for tracking personal spending and providing practical spending guidance.

## MVP Scope

- Single-user personal spending tracker
- SQLite persistence
- Manual transaction entry
- Natural-language transaction parsing
- CSV transaction import
- Default category set for spending analysis
- Monthly income, savings goal, total budget, and category budget management
- Agent-style explanations and saving recommendations

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Open the API docs at <http://127.0.0.1:8000/docs>.

## Testing

```bash
pytest
```
