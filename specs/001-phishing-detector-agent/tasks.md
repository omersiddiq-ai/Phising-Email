# Tasks: Phishing Detector Agent

**Input**: Design documents from `/specs/001-phishing-detector-agent/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the Python project structure, dependency manifest, and repository hygiene before implementation begins.

- [ ] T001 Create `src/agent/`, `src/portal/templates/`, `src/portal/static/`, `data/`, `tests/unit/`, and `tests/integration/` directories
- [ ] T002 Create `requirements.txt` with `openai`, `google-auth`, `google-auth-oauthlib`, `google-api-python-client`, `Flask`, `pytest`, and `python-dotenv`
- [ ] T003 [P] Create `.gitignore` in the repository root to exclude `__pycache__/`, `.venv/`, `token.json`, and other local artifacts
- [ ] T004 [P] Add package initialization files `src/agent/__init__.py` and `src/portal/__init__.py`
- [ ] T005 [P] Create `data/threats.json` with initial content `{"alerts": []}`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement the core service components that all user stories depend on.

- [ ] T006 Create `src/agent/gmail_client.py` to load `credentials.json` and `token.json`, authorize Gmail API read-only access, and fetch new inbox messages
- [ ] T007 Create `src/agent/phishing_classifier.py` to authenticate with `OPENAI_API_KEY`, call the OpenAI Agents SDK, and classify email content as safe or phishing
- [ ] T008 Create `src/agent/storage.py` to persist phishing alerts to `data/threats.json`, load existing alerts, and deduplicate entries by `message_id`
- [ ] T009 Create `src/portal/app.py` with Flask routes for `/`, `/api/alerts`, `/api/alerts/recent`, and `POST /api/alerts`
- [ ] T010 Create `src/portal/templates/index.html` with a portal layout for the running alert list and pop-up notification container
- [ ] T011 Create `src/portal/static/app.js` to fetch portal alert data, poll for new alerts, and trigger browser pop-ups
- [ ] T012 [P] Create `src/portal/static/styles.css` with styling for the alert list and notification pop-up
- [ ] T013 [P] Create `.env.example` at the repository root documenting `OPENAI_API_KEY` and Gmail credential expectations

**Checkpoint**: Foundation ready; user story implementation can begin.

---

## Phase 3: User Story 1 - Detect phishing emails in Gmail (Priority: P1) 🎯 MVP

**Goal**: Connect to Gmail, classify incoming emails with the OpenAI Agents SDK, and only log confirmed phishing messages.

**Independent Test**: Run the agent, send a phishing-style email to the monitored Gmail inbox, and verify a portal entry is created while safe emails are ignored.

- [ ] T014 [US1] Implement Gmail OAuth and inbox monitoring in `src/agent/gmail_client.py`
- [ ] T015 [US1] Implement the OpenAI classification workflow in `src/agent/phishing_classifier.py`
- [ ] T016 [US1] Implement `src/agent/runner.py` to poll Gmail, classify each message, and route phishing detections to storage and the portal API
- [ ] T017 [US1] Implement internal portal alert ingestion via `POST /api/alerts` in `src/portal/app.py`
- [ ] T018 [US1] Implement safe email ignore behavior and deduplication in `src/agent/storage.py`
- [ ] T019 [US1] Validate that safe emails do not generate portal entries or alerts

**Checkpoint**: User Story 1 should detect phishing messages and record them to the portal backend.

---

## Phase 4: User Story 2 - Maintain a running portal list of detected threats (Priority: P2)

**Goal**: Display all detected phishing alerts in a browser-accessible portal list that persists across sessions.

**Independent Test**: Trigger multiple phishing detections and verify the portal list accumulates entries with sender, subject, detection time, and reason.

- [ ] T020 [US2] Implement `GET /api/alerts` in `src/portal/app.py` to return all stored phishing alerts
- [ ] T021 [US2] Implement JSON storage read and list rendering in `src/portal/app.py` using `src/agent/storage.py`
- [ ] T022 [US2] Implement portal list rendering in `src/portal/templates/index.html` to show sender, subject, timestamp, and reason
- [ ] T023 [US2] Implement client-side list refresh in `src/portal/static/app.js` to load the running alert list from `/api/alerts`
- [ ] T024 [US2] Ensure `data/threats.json` persists alerts and the portal reloads them after restart

**Checkpoint**: User Story 2 should provide a durable portal history of all detected phishing threats.

---

## Phase 5: User Story 3 - Show immediate alert details for each detected phishing email (Priority: P3)

**Goal**: Immediately notify the browser with sender details and subject when a new phishing alert is detected.

**Independent Test**: Verify a browser pop-up appears with sender and subject immediately after a new phishing alert is stored.

- [ ] T025 [US3] Implement `GET /api/alerts/recent?since=` in `src/portal/app.py` to return alerts added since an ISO 8601 timestamp
- [ ] T026 [US3] Implement client polling for new alerts in `src/portal/static/app.js`
- [ ] T027 [US3] Implement browser pop-up notification behavior in `src/portal/static/app.js`
- [ ] T028 [US3] Implement alert rendering in `src/portal/templates/index.html` with dedicated sender and subject fields
- [ ] T029 [US3] Implement duplicate notification suppression in `src/portal/static/app.js` so the same alert does not repeat unnecessarily

**Checkpoint**: User Story 3 should immediately surface new phishing alerts in the portal UI.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Clean up documentation, finalize portal behavior, and ensure the feature is deployable.

- [ ] T030 [P] Update `specs/001-phishing-detector-agent/quickstart.md` with exact commands for running the portal and agent locally
- [ ] T031 [P] Add runtime environment documentation in `.env.example`
- [ ] T032 [P] Add `README.md` or repository-level instructions for Gmail OAuth setup and `OPENAI_API_KEY` configuration
- [ ] T033 [P] Add a basic integration test file `tests/integration/test_portal_api.py` for `/api/alerts` and `/api/alerts/recent`
- [ ] T034 [P] Add a basic unit test file `tests/unit/test_storage.py` for `data/threats.json` persistence and deduplication

---

## Dependencies & Execution Order

- **Phase 1: Setup** must finish before Phase 2 begins.
- **Phase 2: Foundational** must finish before all user story work begins.
- **Phase 3, Phase 4, and Phase 5** each depend on the foundational phase, but development on these stories can proceed in parallel once the foundation is ready.
- **Phase 6: Polish** depends on completing the primary user stories.

## Parallel Opportunities

- `T003`, `T004`, and `T005` in Phase 1 can be executed in parallel once the directory structure exists.
- `T012` and `T013` in Phase 2 can be completed in parallel with other foundational file creation tasks.
- `T020` and `T022` in Phase 4 can be implemented in parallel if the portal API and UI are developed separately.
- `T026` and `T027` in Phase 5 can be implemented in parallel because they are separate frontend behaviors.
- `T030` through `T034` in Phase 6 are cross-cutting polish tasks that can proceed in parallel.

## Implementation Strategy

1. Complete Phase 1 and Phase 2 to establish the project scaffold and shared services.
2. Implement User Story 1 first as the MVP behavior: Gmail monitoring, classification, and threat storage.
3. Then implement User Story 2 to expose the persisted running list in the portal.
4. Finally implement User Story 3 to add immediate alert pop-ups for newly detected phishing emails.
5. Finish with Phase 6 polish, documentation, and optional tests.
