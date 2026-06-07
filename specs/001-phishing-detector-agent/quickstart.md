# Quickstart: Phishing Detector Agent

## Prerequisites

- Python 3.11 or later installed.
- `OPENAI_API_KEY` set in the environment.
- `credentials.json` containing Gmail OAuth client credentials in the repository root.
- `token.json` generated after the first Gmail OAuth consent flow.
- `requirements.txt` with the required Python dependencies.

## Setup

1. Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\Activate.ps1 # Windows PowerShell
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Verify environment variables:

```bash
export OPENAI_API_KEY="your_api_key"   # macOS/Linux
setx OPENAI_API_KEY "your_api_key"      # Windows
```

4. Confirm that `credentials.json` and `token.json` are present in the repository root.

## Run the portal

Start the web portal service:

```bash
python src/portal/app.py
```

Open the browser to the portal URL shown in the console, typically `http://localhost:5000`.

## Run the Gmail phishing agent

Launch the email monitoring agent so it can poll Gmail and classify new messages:

```bash
python src/agent/runner.py
```

## Expected outcome

- The portal opens in a browser and shows a list of detected phishing threats.
- When a phishing email is identified, the portal stores it in `data/threats.json`.
- The next browser refresh or live update shows the new phishing alert.
- A browser pop-up or on-screen notification appears with sender details and the email subject for each newly detected phishing email.

## Validation scenarios

- Send a known phishing-style message to the monitored Gmail inbox.
- Confirm the portal list gains a new entry with sender, subject, and detection time.
- Confirm no portal entry appears for safe emails.
