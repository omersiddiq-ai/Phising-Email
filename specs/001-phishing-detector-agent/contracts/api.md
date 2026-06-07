# API Contract: Phishing Detector Agent Portal

## Purpose
Define the web portal interface used by browser clients and the internal agent for storing and retrieving phishing alerts.

## Portal routes

### GET /
- Description: Returns the portal HTML page.
- Response: HTML page that loads the client-side list and alert behavior.

### GET /api/alerts
- Description: Returns the full list of detected phishing alerts.
- Response: `200 OK`
- Body:
  ```json
  {
    "alerts": [
      {
        "id": "string",
        "sender": "string",
        "subject": "string",
        "snippet": "string",
        "message_id": "string",
        "detected_at": "2026-06-07T12:34:56Z",
        "reason": "string",
        "status": "flagged"
      }
    ]
  }
  ```

### GET /api/alerts/recent?since={timestamp}
- Description: Returns alerts detected since the specified ISO 8601 timestamp.
- Query parameters:
  - `since` (string, required): ISO 8601 timestamp.
- Response: `200 OK`
- Body: same format as `GET /api/alerts`, filtered to new alerts.

### POST /api/alerts
- Description: Internal endpoint used by the agent to record a newly detected phishing alert.
- Body:
  ```json
  {
    "id": "string",
    "sender": "string",
    "subject": "string",
    "snippet": "string",
    "message_id": "string",
    "detected_at": "2026-06-07T12:34:56Z",
    "reason": "string",
    "status": "flagged"
  }
  ```
- Response: `201 Created` on success.

## Data contract

### Phishing Alert Object
- `id`: unique alert identifier.
- `sender`: sender email address or display name.
- `subject`: email subject.
- `snippet`: short excerpt of message content or classification reason.
- `message_id`: Gmail message identifier used for deduplication.
- `detected_at`: detection timestamp in ISO 8601 format.
- `reason`: classification rationale or label.
- `status`: current alert status.

## Client behavior

- The portal should poll `GET /api/alerts/recent?since=` or use a refresh mechanism to show newly flagged emails soon after detection.
- When the client sees a new alert, it should display a pop-up notification with `sender` and `subject`.
- The portal list should remain a running list of all alerts.
