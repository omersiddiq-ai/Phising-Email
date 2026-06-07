import logging
import os
import sys
import time
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

from src.agent.gmail_client import GmailClient
from src.agent.phishing_classifier import PhishingClassifier
from src.agent.storage import ThreatStorage

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DEFAULT_PORTAL_URL = os.getenv("PORTAL_URL", "http://127.0.0.1:5000")
DEFAULT_POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "30"))


def build_alert(message: dict, classification: dict) -> dict:
    detected_at = datetime.now(timezone.utc).isoformat()
    return {
        "id": message.get("message_id"),
        "sender": message.get("sender", "Unknown sender"),
        "subject": message.get("subject", "No subject"),
        "snippet": message.get("body", ""),
        "message_id": message.get("message_id"),
        "detected_at": detected_at,
        "reason": classification.get("reason", "phishing suspected"),
        "status": "flagged",
    }


def post_alert_to_portal(portal_url: str, alert: dict) -> None:
    if not portal_url:
        return

    try:
        response = requests.post(f"{portal_url.rstrip('/')}/api/alerts", json=alert, timeout=5)
        if response.status_code not in (200, 201):
            logger.warning("Portal returned %s when posting alert: %s", response.status_code, response.text)
    except requests.RequestException as exc:
        logger.warning("Could not post alert to portal at %s: %s", portal_url, exc)


def main() -> None:
    logger.info("Starting phishing detector agent")
    gmail_client = GmailClient()
    classifier = PhishingClassifier()
    storage = ThreatStorage()
    portal_url = os.getenv("PORTAL_URL", DEFAULT_PORTAL_URL)
    poll_interval = int(os.getenv("POLL_INTERVAL", DEFAULT_POLL_INTERVAL))

    while True:
        try:
            messages = gmail_client.get_unread_messages()
            if not messages:
                logger.debug("No unread messages found")
            for message in messages:
                message_id = message.get("message_id")
                if not message_id:
                    logger.warning("Skipping message with missing ID: %s", message)
                    continue
                if storage.has_processed(message_id):
                    logger.debug("Skipping already processed message %s", message_id)
                    continue

                classification = classifier.classify(message)
                is_phishing = classification.get("is_phishing", False)

                if is_phishing:
                    alert = build_alert(message, classification)
                    saved = storage.save_alert(alert)
                    if saved:
                        post_alert_to_portal(portal_url, alert)
                        logger.info("Flagged phishing message %s", message_id)
                    else:
                        logger.debug("Duplicate phishing message ignored: %s", message_id)
                else:
                    logger.info("Message marked safe: %s", message_id)
                    storage.mark_processed(message_id)

        except Exception as exc:
            logger.exception("Unexpected error in agent loop: %s", exc)

        logger.debug("Sleeping for %s seconds before polling again", poll_interval)
        time.sleep(poll_interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Agent shutdown requested")
        sys.exit(0)
