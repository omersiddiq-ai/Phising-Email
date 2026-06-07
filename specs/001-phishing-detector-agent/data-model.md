# Data Model: Phishing Detector Agent

## Entities

### Phishing Alert
Represents a detected phishing email that is surfaced on the portal.

- `id` (string): unique identifier for the alert, e.g. message ID or UUID.
- `sender` (string): sender email address or display name.
- `subject` (string): email subject line.
- `snippet` (string): short excerpt of the email body or reason text.
- `message_id` (string): Gmail message ID used to deduplicate and track the original email.
- `detected_at` (string, ISO 8601): timestamp when phishing was detected.
- `reason` (string): short classification rationale or label, e.g. "phishing suspected".
- `status` (string): portal status label, e.g. `flagged`, `reviewed`.

### Gmail Message Metadata
Represents a minimal view of an incoming Gmail message for classification.

- `message_id` (string): Gmail message identifier.
- `thread_id` (string): Gmail thread identifier.
- `sender` (string): sender address.
- `subject` (string): subject line.
- `received_at` (string, ISO 8601): message arrival time.
- `body_snippet` (string): preview text or extracted content used for classification.

### Storage Record
Represents the persisted form of detected phishing alerts in JSON storage.

- `alerts` (array of Phishing Alert objects)

## Relationships

- A `Phishing Alert` is derived from one `Gmail Message Metadata` record.
- The portal reads from the `Storage Record` JSON file to build the displayed list.

## Validation rules

- `message_id` must be present and unique for each persisted alert.
- `sender` and `subject` should be included in every alert entry; if missing, use fallback values such as `Unknown sender` or `No subject`.
- `detected_at` must be a valid ISO 8601 timestamp.
- Alerts should not be duplicated in storage for the same `message_id`.
- Safe emails must not create storage records or portal entries.
