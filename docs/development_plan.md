# Development Plan

This plan breaks the project into small backend milestones and explicit
frontend integration checkpoints. The goal is to avoid building too much backend
surface before the React frontend has verified the API shape and workflow.

## Guiding Principles

- Build one usable workflow at a time.
- Keep backend logic authoritative for data validation, planning, execution, and
  verification.
- Let the frontend validate API ergonomics early, especially list browsing,
  reordering, replacement, progress display, and error recovery.
- Prefer local single-user simplicity until the core workflow proves stable.
- Every backend milestone should end with tests, lint checks, and a clear manual
  verification path.

## Phase 1: Backend Foundation

Goal: create a clean Django backend that can start, test, lint, and expose a
minimal API.

Backend work:

- Install runtime packages:
  - Django
  - Django REST Framework
  - django-environ
  - django-cors-headers
- Install test packages:
  - pytest
  - pytest-django
  - pytest-cov
- Create the Django project and first app.
- Configure environment-based settings.
- Configure SQLite for local development.
- Configure DRF and CORS.
- Add a health check endpoint.
- Configure pytest.
- Run Ruff and tests.

Expected result:

- Backend runs locally.
- `/api/health/` or equivalent returns a simple success response.
- Test suite passes.
- Pre-commit can run successfully.

Frontend checkpoint:

- No full frontend work yet.
- Optionally create a tiny fetch test from the frontend repo to confirm CORS and
  base API URL assumptions.

Proceed to Phase 2 when:

- Django starts cleanly.
- Tests and lint pass.
- The frontend can reach the health endpoint if tested.

## Phase 2: Snapshot Persistence

Goal: implement the first durable data model for ordered video snapshots without
connecting to YouTube yet.

Backend work:

- Design and implement models for:
  - Video
  - Snapshot
  - SnapshotItem
- Preserve ordered list positions.
- Represent available, unavailable, deleted, or unknown video states.
- Store retrieval timestamps.
- Add migrations.
- Add model and service tests for saving and reading ordered snapshots.
- Add a small seed or fixture path for local manual testing.

Expected result:

- The backend can persist an ordered list of liked-video-like records.
- Snapshot ordering is deterministic.
- Unavailable entries can exist in the data model.

Frontend checkpoint:

- No major frontend implementation yet.
- Review the model shape from the frontend perspective:
  - Is the video item shape enough to render a YouTube-like list?
  - Is availability status clear enough for UI states?
  - Is ordering represented in a way that is easy to consume?

Proceed to Phase 3 when:

- Snapshot model tests pass.
- The data shape looks usable for the frontend list UI.

## Phase 3: Read-Only Snapshot API

Goal: expose saved snapshots through API endpoints so the frontend can render
real backend data.

Backend work:

- Add serializers for snapshots and snapshot items.
- Add endpoints for:
  - Listing snapshots
  - Reading one snapshot
  - Reading ordered items for one snapshot
- Add API tests.
- Add pagination only if the first real payloads require it.
- Keep filters minimal until the frontend needs them.

Expected result:

- The frontend can fetch saved snapshots and ordered items.
- API responses are stable enough for early UI work.

Frontend checkpoint 1: read-only browser

At this point, pause backend feature work and switch to the frontend.

Frontend work:

- Create the frontend project if it does not exist yet.
- Configure the backend API base URL.
- Build a read-only snapshot list page.
- Build a read-only snapshot detail page.
- Render ordered videos with title, channel, thumbnail, position, and
  availability state.
- Handle loading, empty, and error states.

Integration questions to answer:

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

Backend work:

- Add target snapshot creation from an original snapshot.
- Add endpoint to submit a target order.
- Validate target order input:
  - Known snapshot source
  - No accidental duplicate entries
  - No missing entries unless explicitly supported
  - Stable handling for unavailable entries
- Add service tests and API tests.

Expected result:

- A user can create a target snapshot based on an existing original snapshot.
- The backend rejects invalid target orders with actionable errors.

Frontend checkpoint 2: reorder UI

Pause backend feature work again and switch to the frontend.

Frontend work:

- Add a target-order editing screen.
- Implement drag-and-drop or another ordering UI.
- Submit target order to the backend.
- Display backend validation errors.
- Refresh and render the saved target order.

Integration questions to answer:

- Is the target-order payload too large or awkward?
- Are validation errors precise enough for UI display?
- Does the frontend need optimistic updates or draft state separate from saved
  state?
- Does reordering remain usable with realistic list sizes?

Proceed to Phase 5 when:

- The frontend can edit and save target order.
- Backend validation is understandable in the UI.

## Phase 5: Replacement Handling

Goal: support replacing unavailable entries with user-selected videos while
still allowing ordinary reordering.

Backend work:

- Add replacement representation to the data model.
- Add endpoint to register or update a replacement.
- Validate replacement input.
- Ensure replacement entries can participate in target snapshots.
- Add tests for unavailable-video replacement scenarios.

Expected result:

- The target order can place a replacement video where an unavailable entry used
  to be.
- Replacement state is explicit and recoverable.

Frontend checkpoint 3: replacement flow

Pause backend feature work and switch to the frontend.

Frontend work:

- Add UI states for unavailable entries.
- Add a replacement selection form.
- Submit replacement choices.
- Render replacement relationships clearly.
- Confirm replacement behavior still works with reordering.

Integration questions to answer:

- Does the replacement API support the intended user flow?
- Does the UI need a video lookup endpoint now, or can the user paste a YouTube
  URL/video ID first?
- Are replacement records understandable when viewing old snapshots later?

Proceed to Phase 6 when:

- The frontend can handle unavailable entries and replacements end to end.
- The backend data shape does not need major changes for replacements.

## Phase 6: Reorder Plan Generation

Goal: compare original and target orders and persist a synchronization plan
without touching YouTube yet.

Backend work:

- Implement order comparison logic.
- Identify the smallest section that must be rebuilt.
- Add models for:
  - ReorderPlan
  - SyncOperation
- Generate ordered operations.
- Persist plan status and operation status.
- Add algorithm unit tests with edge cases.
- Add API endpoint to create and inspect a plan.

Expected result:

- The backend can explain what will happen before any destructive YouTube
  operation runs.
- The plan is stable across process restarts.

Frontend checkpoint 4: plan preview

Pause backend feature work and switch to the frontend.

Frontend work:

- Add a plan preview screen.
- Display affected section, operation count, and planned operation order.
- Require explicit user confirmation before execution.
- Display warnings for unavailable videos, replacements, or large operation
  counts.

Integration questions to answer:

- Is the plan explanation understandable?
- Does the frontend need summarized fields instead of raw operations only?
- Is the confirmation flow clear enough before destructive actions?

Proceed to Phase 7 when:

- The frontend can preview a plan and ask for confirmation.
- The backend plan representation is sufficient for user review.

## Phase 7: YouTube OAuth

Goal: connect the local backend to the user's Google/YouTube account securely.

Backend work:

- Add Google OAuth configuration through environment variables.
- Add OAuth start and callback endpoints.
- Store credentials/tokens on the backend only.
- Add an auth status endpoint.
- Avoid logging secrets.
- Add tests around state handling and local credential storage where practical.

Expected result:

- The user can authorize the backend locally.
- The frontend can know whether YouTube is connected without seeing tokens.

Frontend checkpoint 5: auth flow

Pause backend feature work and switch to the frontend.

Frontend work:

- Add YouTube connection status.
- Add connect/disconnect or reconnect controls as supported by the backend.
- Handle OAuth redirect/callback UX.
- Display authentication errors.

Integration questions to answer:

- Is the redirect flow comfortable between frontend and backend origins?
- Does the frontend need polling or a callback landing page?
- Are auth errors actionable?

Proceed to Phase 8 when:

- OAuth works locally.
- The frontend can represent connected and disconnected states.

## Phase 8: YouTube Liked Videos Retrieval

Goal: retrieve the real Liked Videos list from YouTube and save it as an
original snapshot.

Backend work:

- Implement a YouTube API client wrapper.
- Retrieve all liked videos with pagination.
- Preserve YouTube order.
- Save metadata and availability status where possible.
- Add endpoint to trigger retrieval.
- Add error handling for quota, auth expiration, and API failures.
- Add tests with mocked YouTube responses.

Expected result:

- The backend can create real original snapshots from YouTube.
- The frontend read-only snapshot UI works with real data.

Frontend checkpoint 6: real snapshot import

Pause backend feature work and switch to the frontend.

Frontend work:

- Add a fetch/import liked videos action.
- Show retrieval status and errors.
- Navigate to the created snapshot after retrieval.
- Confirm real metadata renders correctly.

Integration questions to answer:

- Are real payload sizes acceptable?
- Are thumbnails reliable?
- Are unavailable/deleted entries represented well enough?
- Does the frontend need background progress for long retrievals?

Proceed to Phase 9 when:

- Real YouTube snapshots can be imported and browsed.
- API response size and frontend rendering performance are acceptable.

## Phase 9: Incremental Synchronization Execution

Goal: execute persisted plans against YouTube safely, with progress checkpoints
and resumability.

Backend work:

- Add execution service for one operation at a time.
- Persist progress after every operation.
- Track completed, pending, failed, and skipped operations.
- Stop before configured operation or quota limits.
- Add pause reasons.
- Add resume behavior from saved state.
- Add tests with mocked YouTube mutation calls.

Expected result:

- Execution is recoverable after app restart or failure.
- The backend can report current progress.
- No execution begins without explicit confirmation.

Frontend checkpoint 7: execution monitor

Pause backend feature work and switch to the frontend.

Frontend work:

- Add execution confirmation action.
- Add progress display.
- Show completed, pending, failed, and pause reason states.
- Add resume action when backend allows it.
- Display failure details and next available actions.

Integration questions to answer:

- Is polling sufficient, or is a later WebSocket/SSE feature justified?
- Are progress fields granular enough?
- Are failure states understandable?

Proceed to Phase 10 when:

- The frontend can monitor and resume execution using backend state.
- The backend execution state model supports the real UI workflow.

## Phase 10: Final Verification and Repair Planning

Goal: verify the final YouTube order after execution and report mismatches.

Backend work:

- Retrieve final Liked Videos state after execution.
- Save a final verification snapshot.
- Compare final snapshot with target snapshot.
- Report exact mismatch positions.
- Indicate whether another repair plan is required.
- Add tests for match and mismatch scenarios.

Expected result:

- The system can prove whether synchronization succeeded.
- Mismatches are explicit and recoverable.

Frontend checkpoint 8: verification result

Pause backend feature work and switch to the frontend.

Frontend work:

- Add verification result screen.
- Show success, mismatch, and repair-needed states.
- Display mismatch positions clearly.
- Offer repair-plan creation if supported.

Integration questions to answer:

- Are mismatch reports easy to understand?
- Does the repair flow need a separate UX?
- Does the user need exportable logs or reports?

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

## Suggested Immediate Next Step

Start with Phase 1. Before running package installation commands, confirm the
exact dependencies and then install them with `uv add`.
