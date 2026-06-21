from datetime import datetime

import pytest
from django.db import IntegrityError
from django.utils import timezone

from organizer.models import VideoListSnapshot, VideoListSnapshotItem
from organizer.tests.factories import (
    create_video,
    create_video_list_snapshot,
    create_video_list_snapshot_item,
)

pytestmark = pytest.mark.django_db


def test_snapshot_items_are_ordered_by_position() -> None:
    """Snapshot items are returned in their stored list order."""
    snapshot = create_video_list_snapshot()
    first_video = create_video("video-first", title="First video")
    second_video = create_video("video-second", title="Second video")
    third_video = create_video("video-third", title="Third video")

    create_video_list_snapshot_item(snapshot, third_video, position=2)
    create_video_list_snapshot_item(snapshot, first_video, position=0)
    create_video_list_snapshot_item(snapshot, second_video, position=1)

    ordered_items = list(snapshot.items.all())

    assert [item.video for item in ordered_items] == [
        first_video,
        second_video,
        third_video,
    ]
    assert [item.position for item in ordered_items] == [0, 1, 2]


def test_unavailable_snapshot_item_can_be_saved() -> None:
    """Unavailable entries can stay in a snapshot with incomplete metadata."""
    snapshot = create_video_list_snapshot()
    unavailable_video = create_video(
        "unavailable-01",
        title="",
        channel_title="",
        thumbnail_url="",
    )

    item = create_video_list_snapshot_item(
        snapshot,
        unavailable_video,
        availability=VideoListSnapshotItem.Availability.UNAVAILABLE,
    )

    item.refresh_from_db()

    assert item.availability == VideoListSnapshotItem.Availability.UNAVAILABLE
    assert item.captured_title == ""
    assert item.captured_channel_title == ""
    assert item.captured_thumbnail_url == ""


def test_snapshot_metadata_can_be_saved() -> None:
    """Snapshot records keep their purpose, label, source, and retrieval time."""
    retrieved_at = timezone.make_aware(datetime(2026, 6, 20, 9, 30))
    source_snapshot = create_video_list_snapshot(
        kind=VideoListSnapshot.Kind.ORIGINAL,
        name="Original liked videos",
        retrieved_at=retrieved_at,
    )

    target_snapshot = create_video_list_snapshot(
        kind=VideoListSnapshot.Kind.TARGET,
        name="Edited liked videos",
        source_snapshot=source_snapshot,
        retrieved_at=retrieved_at,
    )

    target_snapshot.refresh_from_db()

    assert target_snapshot.kind == VideoListSnapshot.Kind.TARGET
    assert target_snapshot.name == "Edited liked videos"
    assert target_snapshot.source_snapshot == source_snapshot
    assert target_snapshot.retrieved_at == retrieved_at


def test_snapshot_cannot_have_duplicate_positions() -> None:
    """One snapshot cannot contain two items at the same position."""
    snapshot = create_video_list_snapshot()
    first_video = create_video("duplicate-position-01")
    second_video = create_video("duplicate-position-02")
    create_video_list_snapshot_item(snapshot, first_video, position=0)

    with pytest.raises(IntegrityError):
        create_video_list_snapshot_item(snapshot, second_video, position=0)


def test_snapshot_cannot_have_duplicate_videos() -> None:
    """One snapshot cannot contain the same video more than once."""
    snapshot = create_video_list_snapshot()
    video = create_video("duplicate-video-01")
    create_video_list_snapshot_item(snapshot, video, position=0)

    with pytest.raises(IntegrityError):
        create_video_list_snapshot_item(snapshot, video, position=1)
