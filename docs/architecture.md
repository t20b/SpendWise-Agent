# SpendWise Agent Architecture

The MVP uses a FastAPI API layer, SQLAlchemy services, SQLite persistence, and a rule-backed agent facade.

## Responsibilities

- API routes validate HTTP input and shape HTTP responses.
- Services own deterministic calculations, persistence, CSV import, category assignment, and budget analysis.
- The agent parses natural-language spending input and explains service-generated spending insights.
- Prompt files document the intended behavior for future LLM integration.

## Data Privacy Notes

Spending data is sensitive. Avoid logging raw transaction descriptions in production, pass only necessary summaries to future LLM calls, and keep calculations in deterministic service code.
