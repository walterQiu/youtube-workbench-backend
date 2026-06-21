# Development Plan

This plan breaks the project into small reviewable increments. Each numbered
substep should be implemented, tested, and reviewed before moving to the next
substep. Avoid bundling multiple substeps into one coding pass unless the user
explicitly asks for it.

## Review Rules

- Implement one substep at a time.
- Before each substep, state which files are expected to change.
- After each substep, run the smallest useful verification commands.
- Do not advance to the next substep until the current result is reviewable.
- Pause backend work at frontend checkpoints and validate the API shape from the
  React app before continuing.

## Phase 1: Backend Foundation

Goal: create a clean Django backend that can start, test, lint, and expose a
minimal API.

Status: mostly complete.

### Phase 1.1: Python Tooling

Work:

- Add Ruff.
- Add pre-commit.
- Configure commit-time Ruff checks.

Review boundary:

- `pyproject.toml`
- `.pre-commit-config.yaml`

### Phase 1.2: Django Dependencies

Work:

- Add Django.
- Add Django REST Framework.
- Add django-environ.
- Add django-cors-headers.
- Add pytest, pytest-django, and pytest-cov.

Review boundary:

- `pyproject.toml`
- `uv.lock`

### Phase 1.3: Django Project Skeleton

Work:

- Create the Django project.
- Create the first Django app.
- Keep generated files understandable and lint-clean.

Review boundary:

- `manage.py`
- `config/`
- `organizer/`

### Phase 1.4: Local Settings

Work:

- Configure environment-based settings.
- Configure `dotenv/.env`.
- Configure SQLite.
- Configure DRF.
- Configure CORS.

Review boundary:

- `config/settings.py`
- `dotenv/.env.example`

### Phase 1.5: Health Endpoint

Work:

- Add a minimal health endpoint.
- Add a minimal API test.

Review boundary:

- `config/urls.py`
- `organizer/urls.py`
- `organizer/views.py`
- `organizer/tests/test_health.py`

### Phase 1.6: Foundation Verification

Work:

- Run Django system checks.
- Run tests.
- Run Ruff.
- Run pre-commit.
- Confirm the health endpoint manually if useful.

Verification:

- `uv run python manage.py check`
- `uv run pytest`
- `uv run ruff check .`
- `uv run pre-commit run --all-files`

Proceed to Phase 2 when:

- Django starts cleanly.
- Tests and lint pass.
- The health endpoint returns `{"status": "ok"}`.

## Phase 2: Snapshot Persistence

Goal: implement the first durable data model for ordered video snapshots without
connecting to YouTube yet.

### Phase 2.1: Model Shape Proposal

Work:

- Propose the model fields before writing model code.
- Decide how to represent video availability.
- Decide how to represent snapshot kinds.
- Decide which uniqueness constraints are needed.
- Decide which fields can be blank or null for unavailable videos.

Expected output:

- A short written model proposal.
- No code changes unless the user asks to record the proposal in docs.

Review boundary:

- User confirms the model shape.

### Phase 2.2: Add Core Model Classes

Work:

- Add `Video`.
- Add `Snapshot`.
- Add `SnapshotItem`.
- Add enum-style `TextChoices` where useful.
- Add `Meta.ordering` and constraints.
- Add helpful `__str__` methods.

Expected files:

- `organizer/models.py`

Verification:

- `uv run ruff check organizer/models.py`
- `uv run python manage.py check`

Review boundary:

- Review model code before migrations are created.

### Phase 2.3: Create Initial Organizer Migration

Work:

- Run `makemigrations`.
- Inspect the generated migration.
- Apply the migration locally.

Expected files:

- `organizer/migrations/0001_initial.py`

Verification:

- `uv run python manage.py makemigrations --check`
- `uv run python manage.py migrate`

Review boundary:

- Review the migration separately from model code.

### Phase 2.4: Model Factory Helpers for Tests

Work:

- Add small test helper functions for creating videos, snapshots, and ordered
  snapshot items.
- Keep helpers local to tests for now.
- Do not add factory-boy yet unless the helpers become noisy.

Expected files:

- `organizer/tests/`

Verification:

- `uv run ruff check organizer/tests`
- `uv run pytest`

Review boundary:

- Review test setup style before adding behavior tests.

### Phase 2.5: Snapshot Ordering Tests

Work:

- Test that snapshot items are read in position order.
- Test that unavailable videos can be persisted.
- Test that snapshot metadata is saved.

Expected files:

- `organizer/tests/test_models.py`

Verification:

- `uv run pytest organizer/tests/test_models.py`
- `uv run ruff check organizer/tests/test_models.py`

Review boundary:

- Review basic persistence behavior before adding constraint tests.

### Phase 2.6: Constraint Tests

Work:

- Test that one snapshot cannot have duplicate positions.
- Test that one snapshot cannot contain the same video twice unless the model
  proposal explicitly allows it.
- Test any source-snapshot relationship constraints if added.

Expected files:

- `organizer/tests/test_models.py`

Verification:

- `uv run pytest organizer/tests/test_models.py`
- `uv run ruff check organizer/tests/test_models.py`

Review boundary:

- Review database guarantees before adding services or APIs.

### Phase 2.7: Optional Seed Command or Fixture

Work:

- Add a tiny local-only way to create sample snapshot data if manual API/UI
  testing needs it.
- Prefer a management command over committing database files.

Expected files:

- `organizer/management/commands/`

Verification:

- `uv run python manage.py <command-name>`
- `uv run pytest`
- `uv run ruff check organizer`

Review boundary:

- This substep can be skipped until the read-only API exists.

Proceed to Phase 3 when:

- Snapshot model tests pass.
- Ordering behavior is deterministic.
- Unavailable entries can be represented.
- The data shape looks usable for the frontend list UI.

Frontend checkpoint:

- No major frontend implementation yet.
- Review the model shape from the frontend perspective:
  - Is the video item shape enough to render a YouTube-like list?
  - Is availability status clear enough for UI states?
  - Is ordering represented in a way that is easy to consume?

## Phase 3: Read-Only Snapshot API

Goal: expose saved snapshots through API endpoints so the frontend can render
real backend data.

### Phase 3.1: API Shape Proposal

Work:

- Propose endpoint paths.
- Propose response payloads.
- Decide whether snapshot items are embedded or separate.
- Decide whether pagination is needed immediately.

Review boundary:

- User confirms API shape before serializers/views are written.

### Phase 3.2: Serializers

Work:

- Add serializers for `Video`, `Snapshot`, and `SnapshotItem`.
- Keep fields stable and frontend-friendly.

Expected files:

- `organizer/serializers.py`

Verification:

- `uv run ruff check organizer/serializers.py`
- `uv run pytest`

### Phase 3.3: Read-Only Views and URLs

Work:

- Add snapshot list endpoint.
- Add snapshot detail endpoint.
- Add ordered snapshot items endpoint if not embedded.

Expected files:

- `organizer/views.py`
- `organizer/urls.py`

Verification:

- `uv run python manage.py check`
- `uv run ruff check organizer`

### Phase 3.4: API Tests

Work:

- Test snapshot list response.
- Test snapshot detail response.
- Test ordered items response.
- Test empty states.

Expected files:

- `organizer/tests/test_snapshot_api.py`

Verification:

- `uv run pytest organizer/tests/test_snapshot_api.py`
- `uv run ruff check organizer/tests/test_snapshot_api.py`

### Phase 3.5: Frontend Checkpoint 1 - Read-Only Browser

Pause backend feature work and switch to the frontend.

Frontend work:

- Create the frontend project if it does not exist yet.
- Configure the backend API base URL.
- Build a read-only snapshot list page.
- Build a read-only snapshot detail page.
- Render ordered videos with title, channel, thumbnail, position, and
  availability state.
- Handle loading, empty, and error states.

Integration questions:

- Are endpoint names and response shapes convenient?
- Does the frontend need different thumbnail fields or metadata?
- Does the list need pagination, search, or filtering earlier than expected?
- Are unavailable entries clear enough for users?

Proceed to Phase 4 when:

- The frontend can browse backend snapshots comfortably.
- Any painful API shape issues from read-only rendering are fixed.

## Phase 4: Target Order Drafting

Goal: support creating and updating a user-defined target order from an original
snapshot.

### Phase 4.1: Target Order API Proposal

Work:

- Propose endpoint paths and request payloads.
- Decide whether target snapshots are created explicitly or on first save.
- Decide how to report validation errors.

### Phase 4.2: Target Snapshot Service

Work:

- Add service logic for creating a target snapshot from an original snapshot.
- Keep behavior independent from HTTP.

### Phase 4.3: Target Order Validation

Work:

- Validate known source snapshot.
- Validate duplicate entries.
- Validate missing entries.
- Preserve unavailable entry handling.

### Phase 4.4: Target Order API

Work:

- Add endpoint to create/update target order.
- Add API tests.

### Phase 4.5: Frontend Checkpoint 2 - Reorder UI

Pause backend feature work and switch to the frontend.

Frontend work:

- Add a target-order editing screen.
- Implement drag-and-drop or another ordering UI.
- Submit target order to the backend.
- Display backend validation errors.
- Refresh and render the saved target order.

Proceed to Phase 5 when:

- The frontend can edit and save target order.
- Backend validation is understandable in the UI.

## Phase 5: Replacement Handling

Goal: support replacing unavailable entries with user-selected videos while
still allowing ordinary reordering.

### Phase 5.1: Replacement Data Proposal

Work:

- Decide whether replacements live on `SnapshotItem`, a separate model, or both.
- Decide whether the first version accepts pasted YouTube video IDs only.

### Phase 5.2: Replacement Model Changes

Work:

- Add replacement persistence.
- Add migration.
- Add constraint tests.

### Phase 5.3: Replacement Service

Work:

- Add replacement validation.
- Ensure replacement entries participate in target snapshots.

### Phase 5.4: Replacement API

Work:

- Add endpoint to register or update a replacement.
- Add API tests.

### Phase 5.5: Frontend Checkpoint 3 - Replacement Flow

Pause backend feature work and switch to the frontend.

Frontend work:

- Add UI states for unavailable entries.
- Add a replacement selection form.
- Submit replacement choices.
- Render replacement relationships clearly.
- Confirm replacement behavior still works with reordering.

Proceed to Phase 6 when:

- The frontend can handle unavailable entries and replacements end to end.
- The backend data shape does not need major changes for replacements.

## Phase 6: Reorder Plan Generation

Goal: compare original and target orders and persist a synchronization plan
without touching YouTube yet.

### Phase 6.1: Planning Algorithm Proposal

Work:

- Define how to find the smallest section that must be rebuilt.
- Define operation types.
- Define edge cases.

### Phase 6.2: Plan Models

Work:

- Add `ReorderPlan`.
- Add `SyncOperation`.
- Add status fields and constraints.
- Add migration.

### Phase 6.3: Pure Planning Function

Work:

- Implement comparison logic without database writes.
- Add unit tests for edge cases.

### Phase 6.4: Plan Persistence Service

Work:

- Convert planning result into persisted plan and operations.
- Add service tests.

### Phase 6.5: Plan Preview API

Work:

- Add endpoint to create and inspect a plan.
- Add API tests.

### Phase 6.6: Frontend Checkpoint 4 - Plan Preview

Pause backend feature work and switch to the frontend.

Frontend work:

- Add a plan preview screen.
- Display affected section, operation count, and planned operation order.
- Require explicit user confirmation before execution.
- Display warnings for unavailable videos, replacements, or large operation
  counts.

Proceed to Phase 7 when:

- The frontend can preview a plan and ask for confirmation.
- The backend plan representation is sufficient for user review.

## Phase 7: YouTube OAuth

Goal: connect the local backend to the user's Google/YouTube account securely.

### Phase 7.1: OAuth Configuration Proposal

Work:

- Define required environment variables.
- Decide where local token files or token records live.
- Decide frontend redirect behavior.

### Phase 7.2: Google Auth Dependencies

Work:

- Add Google API/auth packages.
- Re-enable or adjust pre-commit hooks if needed.

### Phase 7.3: OAuth Start and Callback

Work:

- Add OAuth start endpoint.
- Add OAuth callback endpoint.
- Store backend-only credentials.

### Phase 7.4: Auth Status API

Work:

- Add endpoint for connected/disconnected state.
- Add tests around state and error handling.

### Phase 7.5: Frontend Checkpoint 5 - Auth Flow

Pause backend feature work and switch to the frontend.

Frontend work:

- Add YouTube connection status.
- Add connect/disconnect or reconnect controls as supported by the backend.
- Handle OAuth redirect/callback UX.
- Display authentication errors.

Proceed to Phase 8 when:

- OAuth works locally.
- The frontend can represent connected and disconnected states.

## Phase 8: YouTube Liked Videos Retrieval

Goal: retrieve the real Liked Videos list from YouTube and save it as an
original snapshot.

### Phase 8.1: Retrieval Contract Proposal

Work:

- Define trigger endpoint behavior.
- Define success and error responses.
- Define how retrieval status is represented.

### Phase 8.2: YouTube Client Wrapper

Work:

- Implement read-only YouTube API wrapper.
- Add mocked tests.

### Phase 8.3: Snapshot Import Service

Work:

- Convert YouTube response pages into `Video`, `Snapshot`, and `SnapshotItem`
  records.
- Preserve order and metadata.

### Phase 8.4: Retrieval API

Work:

- Add endpoint to trigger retrieval.
- Add API tests.

### Phase 8.5: Frontend Checkpoint 6 - Real Snapshot Import

Pause backend feature work and switch to the frontend.

Frontend work:

- Add a fetch/import liked videos action.
- Show retrieval status and errors.
- Navigate to the created snapshot after retrieval.
- Confirm real metadata renders correctly.

Proceed to Phase 9 when:

- Real YouTube snapshots can be imported and browsed.
- API response size and frontend rendering performance are acceptable.

## Phase 9: Incremental Synchronization Execution

Goal: execute persisted plans against YouTube safely, with progress checkpoints
and resumability.

### Phase 9.1: Execution State Proposal

Work:

- Define plan statuses.
- Define operation statuses.
- Define pause reasons and quota stop behavior.

### Phase 9.2: One-Step Execution Service

Work:

- Execute one pending operation.
- Persist after every operation.
- Add mocked YouTube mutation tests.

### Phase 9.3: Execution Control API

Work:

- Add confirm/start endpoint.
- Add progress endpoint.
- Add resume endpoint.
- Add API tests.

### Phase 9.4: Failure and Resume Tests

Work:

- Test interrupted execution.
- Test failed operations.
- Test quota/operation-limit stops.

### Phase 9.5: Frontend Checkpoint 7 - Execution Monitor

Pause backend feature work and switch to the frontend.

Frontend work:

- Add execution confirmation action.
- Add progress display.
- Show completed, pending, failed, and pause reason states.
- Add resume action when backend allows it.
- Display failure details and next available actions.

Proceed to Phase 10 when:

- The frontend can monitor and resume execution using backend state.
- The backend execution state model supports the real UI workflow.

## Phase 10: Final Verification and Repair Planning

Goal: verify the final YouTube order after execution and report mismatches.

### Phase 10.1: Verification Contract Proposal

Work:

- Define mismatch report shape.
- Define when repair planning is allowed.

### Phase 10.2: Final Snapshot Retrieval

Work:

- Retrieve final YouTube state.
- Save a final verification snapshot.

### Phase 10.3: Snapshot Comparison Service

Work:

- Compare final snapshot with target snapshot.
- Report exact mismatch positions.
- Add tests for match and mismatch scenarios.

### Phase 10.4: Verification API

Work:

- Add endpoint to run or inspect verification.
- Add API tests.

### Phase 10.5: Frontend Checkpoint 8 - Verification Result

Pause backend feature work and switch to the frontend.

Frontend work:

- Add verification result screen.
- Show success, mismatch, and repair-needed states.
- Display mismatch positions clearly.
- Offer repair-plan creation if supported.

Proceed when:

- The full core workflow works end to end:
  - Authenticate
  - Import original snapshot
  - Create target order
  - Handle replacements
  - Generate plan
  - Confirm execution
  - Monitor progress
  - Resume if interrupted
  - Verify final order

## Deferred Work

These items should stay out of the initial implementation unless a previous
phase proves they are necessary:

- Multi-user support
- Public registration or public deployment
- PostgreSQL support
- Celery and Redis
- WebSocket or SSE progress updates
- Docker orchestration
- General playlist management
- Recommendation features
- Automatic replacement discovery
- Advanced search/filtering
- OpenAPI documentation polish before endpoint shapes stabilize
