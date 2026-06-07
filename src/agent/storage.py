import json
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ThreatStorage:
    def __init__(self, path: str = "data/threats.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        if not self.path.exists():
            self._save({"alerts": [], "processed_ids": []})

    def _load(self) -> Dict[str, Any]:
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, FileNotFoundError):
            logger.warning("Reinitializing storage file at %s", self.path)
            data = {"alerts": [], "processed_ids": []}
            self._save(data)
        if "alerts" not in data:
            data["alerts"] = []
        if "processed_ids" not in data:
            data["processed_ids"] = []
        return data

    def _save(self, data: Dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

    def get_alerts(self) -> List[Dict[str, Any]]:
        data = self._load()
        return data.get("alerts", [])

    def get_processed_ids(self) -> List[str]:
        data = self._load()
        return data.get("processed_ids", [])

    def has_processed(self, message_id: str) -> bool:
        return message_id in set(self.get_processed_ids())

    def mark_processed(self, message_id: str) -> None:
        data = self._load()
        processed = set(data.get("processed_ids", []))
        if message_id not in processed:
            processed.add(message_id)
            data["processed_ids"] = list(processed)
            self._save(data)

    def save_alert(self, alert: Dict[str, Any]) -> bool:
        message_id = alert.get("message_id")
        if not message_id:
            raise ValueError("Alert payload must include message_id")

        data = self._load()
        processed = set(data.get("processed_ids", []))
        existing_ids = {item.get("message_id") for item in data.get("alerts", [])}

        if message_id in processed or message_id in existing_ids:
            logger.debug("Skipping duplicate alert for message_id %s", message_id)
            self.mark_processed(message_id)
            return False

        alert_record = {
            "id": alert.get("id") or message_id,
            "sender": alert.get("sender", "Unknown sender"),
            "subject": alert.get("subject", "No subject"),
            "snippet": alert.get("snippet", ""),
            "message_id": message_id,
            "detected_at": alert.get("detected_at"),
            "reason": alert.get("reason", "phishing suspected"),
            "status": alert.get("status", "flagged"),
        }
        data["alerts"].append(alert_record)
        processed.add(message_id)
        data["processed_ids"] = list(processed)
        self._save(data)
        logger.info("Saved phishing alert for message_id %s", message_id)
        return True
