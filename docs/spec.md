# YouTube Liked Videos Organizer — Backend Specification

## 1. Project Overview

This repository contains the backend service for the YouTube Liked Videos Organizer.

The backend is responsible for connecting to YouTube, storing the user's Liked Videos state, calculating reorder plans, executing synchronization operations, preserving progress, and verifying the final order.

It exposes an API consumed by a separate React frontend.

## 2. Project Goals

The backend should support the following capabilities:

- Authenticate the user with Google and YouTube.
- Retrieve all videos from the user's YouTube Liked Videos list.
- Save snapshots of the original order.
- Save a user-defined target order.
- Support replacement of unavailable videos.
- Compare the original and target orders.
- Identify the smallest section that must be rebuilt.
- Generate a synchronization plan.
- Remove and restore likes in the required order.
- Stop safely when daily quota is insufficient.
- Save execution progress.
- Resume an interrupted synchronization.
- Record failures and allow recovery.
- Retrieve the final YouTube state.
- Verify that the final order matches the target order.

## 3. Scope

The backend only reorganizes videos associated with the user's YouTube Liked Videos list.

It does not provide:

- Video downloading.
- Recommendation features.
- Subscription management.
- Comment management.
- Watch history management.
- General-purpose playlist management.
- Multi-user account management.
- Public user registration.
- Public cloud deployment requirements.

The initial application is intended for one user running the system locally.

## 4. Core Functional Areas

### 4.1 YouTube Authentication

The backend should manage the Google OAuth flow required to access the user's YouTube account.

Authentication credentials and tokens must remain on the backend and must not be exposed to the frontend.

### 4.2 Liked Videos Retrieval

The backend should retrieve the user's complete Liked Videos list and preserve its order.

The saved data should include available metadata where possible, such as:

- YouTube video ID.
- Title.
- Channel title.
- Thumbnail.
- Availability status.
- Position in the list.
- Retrieval timestamp.

Unavailable or deleted entries should be preserved when they can be identified.

### 4.3 Snapshot Management

The backend should save distinct versions of the list, including:

- Original YouTube snapshots.
- User-modified target snapshots.
- Final verification snapshots.

Snapshots should remain available for comparison and recovery.

### 4.4 Reorder Planning

The backend should compare the original and target orders and determine the minimum section that must be rebuilt.

It should produce a persistent plan containing the required operations and their intended order.

The backend owns this logic. The frontend only displays the result.

### 4.5 Replacement Handling

The backend should allow an unavailable video entry to be replaced by another YouTube video selected by the user.

The replacement should take the unavailable video's intended place in the target order.

The feature should also support ordinary reordering that is unrelated to unavailable videos.

### 4.6 Synchronization Execution

The backend should execute the generated plan against YouTube.

Execution must be:

- Incremental.
- Recoverable.
- Persisted.
- Observable by the frontend.
- Safe to resume after application restart.
- Able to stop before exceeding the configured operation or quota limit.

### 4.7 Progress and Recovery

The backend should track:

- Plan status.
- Individual operation status.
- Completed operation count.
- Pending operation count.
- Failed operations.
- Current execution position.
- Pause reason.
- Quota-related stop state.
- Last update time.

The backend should resume from saved state instead of rebuilding the plan from scratch.

### 4.8 Verification

After synchronization, the backend should retrieve the actual Liked Videos order again and compare it with the target order.

The result should clearly indicate:

- Whether the final order matches.
- Where mismatches exist.
- Whether another repair operation is required.

## 5. Backend Responsibilities

The backend is responsible for:

- Google OAuth and credential management.
- YouTube Data API integration.
- Database persistence.
- Snapshot storage.
- Target-order validation.
- Reorder-plan generation.
- Quota-aware execution.
- Checkpoint and recovery behavior.
- Error recording.
- Final-state verification.
- Providing API data to the frontend.
- Enforcing business rules.

The backend is not responsible for:

- Rendering the main graphical interface.
- Drag-and-drop behavior.
- Frontend navigation.
- Client-side visual state.

## 6. Data Persistence Requirements

The backend should use a relational database to persist:

- Video metadata.
- Snapshots.
- Ordered snapshot items.
- Replacement relationships.
- Reorder plans.
- Individual synchronization operations.
- Execution progress.
- Error information.
- Authentication-related metadata where appropriate.

SQLite is sufficient for the initial local single-user version.

The design should not prevent a later migration to PostgreSQL, but PostgreSQL support is not required initially.

## 7. Initial Technology Stack

### Core Framework

- Django
- Django REST Framework

### Configuration

- django-environ

### YouTube and Google Authentication

- google-api-python-client
- google-auth
- google-auth-oauthlib
- google-auth-httplib2

### Frontend Integration

- django-cors-headers

This may be used during development when the frontend and backend run on different local origins.

### Filtering

- django-filter

This should be added when API-side filtering becomes useful.

### API Documentation

- drf-spectacular

This should provide an OpenAPI schema and interactive API documentation once the API structure becomes stable enough.

### Testing

- pytest
- pytest-django
- pytest-cov

Optional test-data support:

- factory-boy

### Code Quality

- Ruff
- pre-commit

## 8. Background Execution

The initial version should avoid unnecessary infrastructure.

Celery and Redis are not required for the first implementation.

The backend should first support safe, incremental execution with persistent checkpoints.

A dedicated background-task system may be introduced later if the simpler execution model becomes insufficient.

Potential future packages include:

- Celery
- Redis
- django-celery-results
- django-celery-beat

These are explicitly deferred.

## 9. Security Requirements

The backend should:

- Keep OAuth credentials and tokens outside source control.
- Load secrets from environment variables.
- Avoid exposing tokens to the frontend.
- Bind local development services appropriately.
- Validate all target-order and replacement input.
- Require explicit confirmation before synchronization begins.
- Avoid logging secrets.
- Preserve enough state to recover from partial execution.

## 10. Initial Development Priorities

The first backend milestone should focus on:

1. Establishing the Django project.
2. Configuring environment-based settings.
3. Creating the initial persistence layer.
4. Implementing YouTube authentication.
5. Retrieving and saving a Liked Videos snapshot.
6. Providing the saved data to the frontend.
7. Accepting and storing a target order.
8. Implementing reorder comparison and plan generation.
9. Adding incremental execution and saved progress.
10. Adding final verification.

Detailed API endpoint design, database schemas, service interfaces, and execution algorithms are intentionally excluded from this specification.

## 11. Non-Goals for the Initial Version

The initial version does not need:

- Multi-user support.
- Public authentication.
- PostgreSQL.
- Celery.
- Redis.
- Docker orchestration.
- Kubernetes.
- Cloud deployment.
- WebSocket communication.
- General playlist support.
- Automatic discovery of replacement videos.
- Recommendation systems.

## 12. Repository Boundary

This repository contains backend-related code and configuration only.

React components, browser routing, drag-and-drop behavior, visual design, frontend tests, and frontend build configuration belong to the separate frontend repository.
