from datetime import datetime

from django.utils import timezone

from organizer.models import Video, VideoListSnapshot, VideoListSnapshotItem


def create_video(
    youtube_id: str = "video-00001",
    *,
    title: str = "Example video",
    channel_title: str = "Example channel",
    thumbnail_url: str = "https://img.youtube.com/vi/video-00001/default.jpg",
) -> Video:
    """Create a video for model and API tests."""
    return Video.objects.create(
        youtube_id=youtube_id,
        title=title,
        channel_title=channel_title,
        thumbnail_url=thumbnail_url,
    )


def create_video_list_snapshot(
    kind: str = VideoListSnapshot.Kind.MANUAL,
    *,
    name: str = "Example snapshot",
    source_snapshot: VideoListSnapshot | None = None,
    retrieved_at: datetime | None = None,
) -> VideoListSnapshot:
    """Create a video list snapshot for tests."""
    return VideoListSnapshot.objects.create(
        kind=kind,
        name=name,
        source_snapshot=source_snapshot,
        retrieved_at=retrieved_at or timezone.now(),
    )


def create_video_list_snapshot_item(
    snapshot: VideoListSnapshot,
    video: Video,
    *,
    position: int = 0,
    availability: str = VideoListSnapshotItem.Availability.AVAILABLE,
) -> VideoListSnapshotItem:
    """Create one ordered item inside a video list snapshot."""
    return VideoListSnapshotItem.objects.create(
        snapshot=snapshot,
        video=video,
        position=position,
        availability=availability,
        captured_title=video.title,
        captured_channel_title=video.channel_title,
        captured_thumbnail_url=video.thumbnail_url,
    )
