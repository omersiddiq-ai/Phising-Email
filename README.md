# Phishing Detector Agent

This repository implements a Python phishing detection agent that monitors a Gmail inbox, classifies new emails using the OpenAI Agents SDK, and logs confirmed phishing threats to a lightweight Flask web portal.

## Setup

1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set your `OPENAI_API_KEY`.

4. Make sure `credentials.json` is present in the repository root. The first run of the agent will create `token.json` automatically during Gmail OAuth consent.

## Run the portal

```powershell
python src/portal/app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Run the agent

```powershell
python src/agent/runner.py
```

The agent will poll Gmail for unread messages, classify each new message, and persist confirmed phishing alerts to `data/threats.json`.

## Testing

```powershell
pytest
```

## Notes

- The agent uses `OPENAI_API_KEY` from the environment.
- Gmail credentials must be stored in `credentials.json`; this project uses read-only Gmail API access.
- Detected phishing threats are stored in `data/threats.json`.
