# Research: Phishing Detector Agent

## Decision: Python + OpenAI Agents SDK + Gmail API + JSON storage

**Decision**: Build the phishing detector using Python, the OpenAI Agents SDK for phishing classification, the Gmail API for read-only inbox access, and a lightweight Flask-based web portal. Persist detected phishing records in a local JSON file.

**Rationale**:
- Python provides wide support for Google APIs and OpenAI integrations.
- The OpenAI Agents SDK can manage prompt-driven classification while keeping the system centered on the requested LLM-based intelligence.
- Gmail API read-only access satisfies the safety requirement for inbox monitoring without modifying messages.
- JSON file storage is simple, easy to inspect, and aligns with the requested straightforward storage strategy.
- Flask is a lightweight portal framework that supports simple HTML/JS front ends and can display alerts without introducing heavy UI frameworks.

**Alternatives considered**:
- FastAPI instead of Flask: FastAPI offers built-in schema validation and async support, but Flask is simpler for a small portal and easier to bootstrap for standard HTML/JS pages.
- SQLite or PostgreSQL instead of JSON file: a database is more scalable, but JSON storage is sufficient for a proof-of-concept and matches the user’s request for straightforward storage.
- Gmail push notifications / Pub/Sub instead of polling: push notifications reduce latency, but they require additional webhook infrastructure. A polling loop with short intervals is simpler for initial implementation.
- Local classification rules instead of OpenAI: local rules can be faster, but the user explicitly requested LLM-based phishing classification.

## Key implementation assumptions

- The email monitor will run continuously or on a scheduled loop, reading new Gmail messages as they arrive.
- The Gmail OAuth credentials are stored in `credentials.json` and exchanged for a refreshable token in `token.json`.
- The portal and agent can be co-hosted in the same Python service or launched as separate Python processes, with the storage file shared between them.
- Alerts can be surfaced in the browser using a simple polling or near-real-time push mechanism from the portal.
