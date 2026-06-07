from datetime import datetime, timezone

from src.portal.app import create_app


def test_portal_alert_endpoints(tmp_path):
    storage_path = tmp_path / "threats.json"
    app = create_app(storage_path=str(storage_path))
    client = app.test_client()

    response = client.get("/api/alerts")
    assert response.status_code == 200
    assert response.json == {"alerts": []}

    payload = {
        "message_id": "msg-999",
        "sender": "phisher@example.com",
        "subject": "Account verification required",
        "snippet": "Please verify your account immediately.",
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "reason": "Phishing classification returned PHISHING.",
        "status": "flagged",
    }

    response = client.post("/api/alerts", json=payload)
    assert response.status_code == 201
    assert response.json["status"] == "created"

    response = client.get("/api/alerts")
    assert response.status_code == 200
    assert len(response.json["alerts"]) == 1
    assert response.json["alerts"][0]["message_id"] == "msg-999"

    old_time = datetime(2000, 1, 1, tzinfo=timezone.utc).isoformat()
    response = client.get("/api/alerts/recent", query_string={"since": old_time})
    assert response.status_code == 200
    assert len(response.json["alerts"]) == 1

    response = client.get("/api/alerts/recent")
    assert response.status_code == 400
