# API Specification

Base URL for local development:

```text
http://127.0.0.1:8000/api/
```

All current API responses are JSON.

## Health Check

Check whether the backend API is reachable.

```http
GET /api/health/
```

### Response

```json
{
  "status": "ok"
}
```

### Status Codes

- `200 OK`: backend is reachable.

## List Snapshots

Return all saved video list snapshots.

```http
GET /api/snapshots/
```

### Request

No request body.

### Response

```json
[
  {
    "id": 1,
    "kind": "manual",
    "name": "[seed] Manual liked videos snapshot",
    "source_snapshot": null,
    "retrieved_at": null,
    "created_at": "2026-06-21T12:21:26.150328+08:00",
    "updated_at": "2026-06-21T12:21:26.150345+08:00",
    "item_count": 4
  }
]
```

### Response Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | number | Snapshot primary key. |
| `kind` | string | Snapshot purpose. Current values: `original`, `target`, `verification`, `manual`. |
| `name` | string | Human-readable snapshot name. May be empty. |
| `source_snapshot` | number or null | Source snapshot ID when this snapshot was derived from another snapshot. |
| `retrieved_at` | string or null | Time the list state was retrieved from an external source, when applicable. |
| `created_at` | string | Time this snapshot record was created. |
| `updated_at` | string | Time this snapshot record was last updated. |
| `item_count` | number | Number of items in the snapshot. |

### Status Codes

- `200 OK`: request succeeded.

## Get Snapshot

Return metadata for one saved video list snapshot.

```http
GET /api/snapshots/{snapshot_id}/
```

### Path Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `snapshot_id` | number | Snapshot primary key. |

### Request

No request body.

### Response

```json
{
  "id": 1,
  "kind": "manual",
  "name": "[seed] Manual liked videos snapshot",
  "source_snapshot": null,
  "retrieved_at": null,
  "created_at": "2026-06-21T12:21:26.150328+08:00",
  "updated_at": "2026-06-21T12:21:26.150345+08:00",
  "item_count": 4
}
```

### Response Fields

Same as `GET /api/snapshots/`.

### Status Codes

- `200 OK`: request succeeded.
- `404 Not Found`: snapshot does not exist.

## List Snapshot Items

Return ordered video items for one snapshot.

```http
GET /api/snapshots/{snapshot_id}/items/
```

### Path Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `snapshot_id` | number | Snapshot primary key. |

### Request

No request body.

### Response

```json
[
  {
    "id": 1,
    "position": 0,
    "availability": "available",
    "video": {
      "id": 1,
      "youtube_id": "seedvid0001",
      "title": "Sample introduction",
      "channel_title": "Workbench Samples",
      "thumbnail_url": "https://img.youtube.com/vi/seedvid0001/default.jpg"
    },
    "captured_title": "Sample introduction",
    "captured_channel_title": "Workbench Samples",
    "captured_thumbnail_url": "https://img.youtube.com/vi/seedvid0001/default.jpg"
  },
  {
    "id": 3,
    "position": 2,
    "availability": "unavailable",
    "video": {
      "id": 3,
      "youtube_id": "unavail0001",
      "title": "",
      "channel_title": "",
      "thumbnail_url": ""
    },
    "captured_title": "",
    "captured_channel_title": "",
    "captured_thumbnail_url": ""
  }
]
```

### Response Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | number | Snapshot item primary key. |
| `position` | number | Zero-based position inside the snapshot. |
| `availability` | string | Availability observed for this snapshot item. Current values: `available`, `unavailable`, `deleted`, `private`, `unknown`. |
| `video` | object | Current local video record metadata. |
| `captured_title` | string | Title observed when this snapshot item was captured. May be empty. |
| `captured_channel_title` | string | Channel title observed when this snapshot item was captured. May be empty. |
| `captured_thumbnail_url` | string | Thumbnail URL observed when this snapshot item was captured. May be empty. |

### `video` Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | number | Video primary key. |
| `youtube_id` | string | YouTube video ID. |
| `title` | string | Current local title for this video. May be empty. |
| `channel_title` | string | Current local channel title for this video. May be empty. |
| `thumbnail_url` | string | Current local thumbnail URL for this video. May be empty. |

### Status Codes

- `200 OK`: request succeeded.
- `404 Not Found`: snapshot does not exist.

## Notes For Frontend

- API field names currently use `snake_case`.
- Snapshot item order is determined by `position`; responses are already sorted by position.
- `video` metadata represents the current local video record.
- `captured_*` metadata represents the value stored on that specific snapshot item.
- Empty strings are expected for metadata that is unavailable.
- `retrieved_at` can be `null` for locally created snapshots such as `manual` or `target`.
