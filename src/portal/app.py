import logging
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request, render_template

from src.agent.storage import ThreatStorage

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def _resolve_storage_path(storage_path: str = None) -> str:
    if storage_path:
        return storage_path
    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "data"
    # Create data directory if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(data_dir / "threats.json")


def _parse_iso_timestamp(timestamp: str) -> datetime:
    if timestamp.endswith("Z"):
        timestamp = timestamp[:-1] + "+00:00"
    return datetime.fromisoformat(timestamp)


def create_app(storage_path: str = None) -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    storage = ThreatStorage(path=_resolve_storage_path(storage_path))

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/alerts")
    def list_alerts():
        return jsonify({"alerts": storage.get_alerts()})

    @app.route("/api/alerts/recent")
    def recent_alerts():
        since = request.args.get("since")
        if not since:
            return jsonify({"error": "Missing required query parameter: since"}), 400
        try:
            cutoff = _parse_iso_timestamp(since)
        except ValueError:
            return jsonify({"error": "Invalid ISO 8601 timestamp for since parameter"}), 400

        recent = [
            alert
            for alert in storage.get_alerts()
            if _parse_iso_timestamp(alert.get("detected_at", "1970-01-01T00:00:00Z")) > cutoff
        ]
        return jsonify({"alerts": recent})

    @app.route("/api/alerts", methods=["POST"])
    def receive_alert():
        payload = request.get_json(force=True, silent=True)
        if not payload:
            return jsonify({"error": "JSON payload required"}), 400

        required = ["message_id", "sender", "subject", "detected_at"]
        for field in required:
            if not payload.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400

        saved = storage.save_alert(payload)
        if saved:
            return jsonify({"status": "created"}), 201
        return jsonify({"status": "duplicate"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    # Use PORT env var from Vercel; fallback to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0" if os.environ.get("VERCEL") else "127.0.0.1"
    app.run(host=host, port=port)
