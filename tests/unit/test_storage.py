import json
from pathlib import Path

from src.agent.storage import ThreatStorage


def test_storage_saves_and_loads_alert(tmp_path):
    storage_path = tmp_path / "threats.json"
    storage = ThreatStorage(path=str(storage_path))

    alert = {
        "message_id": "msg-123",
        "sender": "attacker@example.com",
        "subject": "Urgent account update",
        "snippet": "Your account requires immediate attention.",
        "detected_at": "2026-06-07T12:00:00Z",
        "reason": "Model flagged this message as phishing.",
        "status": "flagged",
    }

    assert storage.save_alert(alert) is True
    assert storage.has_processed("msg-123")
    assert len(storage.get_alerts()) == 1

    assert storage.save_alert(alert) is False
    assert len(storage.get_alerts()) == 1

    stored = json.loads(storage_path.read_text(encoding="utf-8"))
    assert stored["processed_ids"] == ["msg-123"]
