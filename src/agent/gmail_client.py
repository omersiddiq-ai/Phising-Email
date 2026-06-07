import base64
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
logger = logging.getLogger(__name__)


class GmailClient:
    def __init__(self, credentials_path: Optional[str] = None, token_path: Optional[str] = None):
        self.credentials_path = Path(credentials_path or "credentials.json")
        self.token_path = Path(token_path or "token.json")
        self.creds = None
        self.service = self._build_service()

    def _build_service(self):
        self.creds = self._load_credentials()
        return build("gmail", "v1", credentials=self.creds)

    def _load_credentials(self) -> Credentials:
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"Gmail credentials file not found at {self.credentials_path}. "
                "Place your OAuth client credentials in credentials.json."
            )

        creds = None
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                self._save_token(creds)
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)
                self._save_token(creds)

        return creds

    def _save_token(self, creds: Credentials) -> None:
        self.token_path.write_text(creds.to_json())
        logger.info("Saved refreshed Gmail OAuth token to %s", self.token_path)

    def get_unread_messages(self) -> List[Dict[str, Any]]:
        try:
            response = (
                self.service.users()
                .messages()
                .list(userId="me", q="is:unread", maxResults=50)
                .execute()
            )
        except HttpError as exc:
            logger.error("Failed to list unread Gmail messages: %s", exc)
            return []

        messages = response.get("messages", [])
        results = []
        for message in messages:
            details = self._get_message_details(message["id"])
            if details:
                results.append(details)
        return results

    def _get_message_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )
        except HttpError as exc:
            logger.error("Failed to fetch Gmail message %s: %s", message_id, exc)
            return None

        headers = self._parse_headers(message.get("payload", {}).get("headers", []))
        sender = headers.get("From", "Unknown sender")
        subject = headers.get("Subject", "No subject")
        received_at = headers.get("Date", "")
        body = self._extract_text(message.get("payload", {}))
        snippet = message.get("snippet", "")
        content = body or snippet

        return {
            "message_id": message_id,
            "thread_id": message.get("threadId", ""),
            "sender": sender,
            "subject": subject,
            "received_at": received_at,
            "body": content,
        }

    def _parse_headers(self, headers: List[Dict[str, str]]) -> Dict[str, str]:
        header_map = {}
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name and value:
                header_map[name] = value
        return header_map

    def _extract_text(self, payload: Dict[str, Any]) -> str:
        if not payload:
            return ""

        mime_type = payload.get("mimeType", "")
        if mime_type == "text/plain" and payload.get("body", {}).get("data"):
            return self._decode_body(payload["body"]["data"])

        text = ""
        for part in payload.get("parts", []) or []:
            text += self._extract_text(part)

        return text

    def _decode_body(self, data: str) -> str:
        data = data.replace("-", "+").replace("_", "/")
        padding = len(data) % 4
        if padding:
            data += "=" * (4 - padding)
        try:
            decoded = base64.b64decode(data)
            return decoded.decode("utf-8", errors="replace")
        except Exception as exc:
            logger.warning("Could not decode Gmail message body: %s", exc)
            return ""
