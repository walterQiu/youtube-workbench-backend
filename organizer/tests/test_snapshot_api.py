import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from organizer.models import VideoListSnapshot, VideoListSnapshotItem
from organizer.tests.factories import (
    create_video,
    create_video_list_snapshot,
    create_video_list_snapshot_item,
)

pytestmark = pytest.mark.django_db

SNAPSHOT_LIST_ITEM_COUNT = 2
MISSING_SNAPSHOT_ID = 999


def test_snapshot_list_returns_empty_list() -> None:
    """The snapshot list endpoint returns an empty list when no snapshots exist."""
    client = APIClient()

    response = client.get(reverse("organizer:snapshot-list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_snapshot_list_returns_snapshots_with_item_counts() -> None:
    """The snapshot list endpoint includes snapshot metadata and item counts."""
    client = APIClient()
    snapshot = create_video_list_snapshot(
        kind=VideoListSnapshot.Kind.ORIGINAL,
        name="Original liked videos",
    )
    first_video = create_video("snapshot-list-01")
    second_video = create_video("snapshot-list-02")
    create_video_list_snapshot_item(snapshot, first_video, position=0)
    create_video_list_snapshot_item(snapshot, second_video, position=1)

    response = client.get(reverse("organizer:snapshot-list"))

    payload = response.json()
    snapshot_payload = payload[0]

    assert response.status_code == status.HTTP_200_OK
    assert [item["id"] for item in payload] == [snapshot.id]
    assert snapshot_payload["kind"] == VideoListSnapshot.Kind.ORIGINAL
    assert snapshot_payload["name"] == "Original liked videos"
    assert snapshot_payload["source_snapshot"] is None
    assert snapshot_payload["item_count"] == SNAPSHOT_LIST_ITEM_COUNT
    assert isinstance(snapshot_payload["retrieved_at"], str)
    assert isinstance(snapshot_payload["created_at"], str)
    assert isinstance(snapshot_payload["updated_at"], str)


def test_snapshot_detail_returns_one_snapshot() -> None:
    """The snapshot detail endpoint returns one snapshot by primary key."""
    client = APIClient()
    source_snapshot = create_video_list_snapshot(
        kind=VideoListSnapshot.Kind.ORIGINAL,
        name="Original liked videos",
    )
    target_snapshot = create_video_list_snapshot(
        kind=VideoListSnapshot.Kind.TARGET,
        name="Edited liked videos",
        source_snapshot=source_snapshot,
    )

    response = client.get(
        reverse(
            "organizer:snapshot-detail", kwargs={"snapshot_id": target_snapshot.id}
        ),
    )

    payload = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert payload["id"] == target_snapshot.id
    assert payload["kind"] == VideoListSnapshot.Kind.TARGET
    assert payload["name"] == "Edited liked videos"
    assert payload["source_snapshot"] == source_snapshot.id
    assert payload["item_count"] == 0


def test_snapshot_items_returns_ordered_items_with_video_data() -> None:
    """The snapshot item endpoint returns ordered items and nested video metadata."""
    client = APIClient()
    snapshot = create_video_list_snapshot()
    first_video = create_video(
        "snapshot-items-01",
        title="First video",
        channel_title="First channel",
        thumbnail_url="https://img.youtube.com/vi/snapshot-items-01/default.jpg",
    )
    unavailable_video = create_video(
        "snapshot-items-02",
        title="",
        channel_title="",
        thumbnail_url="",
    )
    create_video_list_snapshot_item(
        snapshot,
        unavailable_video,
        position=1,
        availability=VideoListSnapshotItem.Availability.UNAVAILABLE,
    )
    create_video_list_snapshot_item(snapshot, first_video, position=0)

    response = client.get(
        reverse("organizer:snapshot-item-list", kwargs={"snapshot_id": snapshot.id}),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": snapshot.items.get(position=0).id,
            "position": 0,
            "availability": VideoListSnapshotItem.Availability.AVAILABLE,
            "video": {
                "id": first_video.id,
                "youtube_id": "snapshot-items-01",
                "title": "First video",
                "channel_title": "First channel",
                "thumbnail_url": (
                    "https://img.youtube.com/vi/snapshot-items-01/default.jpg"
                ),
            },
            "captured_title": "First video",
            "captured_channel_title": "First channel",
            "captured_thumbnail_url": (
                "https://img.youtube.com/vi/snapshot-items-01/default.jpg"
            ),
        },
        {
            "id": snapshot.items.get(position=1).id,
            "position": 1,
            "availability": VideoListSnapshotItem.Availability.UNAVAILABLE,
            "video": {
                "id": unavailable_video.id,
                "youtube_id": "snapshot-items-02",
                "title": "",
                "channel_title": "",
                "thumbnail_url": "",
            },
            "captured_title": "",
            "captured_channel_title": "",
            "captured_thumbnail_url": "",
        },
    ]


def test_snapshot_detail_returns_not_found_for_missing_snapshot() -> None:
    """The snapshot detail endpoint returns 404 for unknown snapshots."""
    client = APIClient()

    response = client.get(
        reverse(
            "organizer:snapshot-detail", kwargs={"snapshot_id": MISSING_SNAPSHOT_ID}
        ),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_snapshot_items_returns_not_found_for_missing_snapshot() -> None:
    """The snapshot item endpoint returns 404 for unknown snapshots."""
    client = APIClient()

    response = client.get(
        reverse(
            "organizer:snapshot-item-list",
            kwargs={"snapshot_id": MISSING_SNAPSHOT_ID},
        ),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
