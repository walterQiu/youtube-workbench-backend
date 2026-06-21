from dataclasses import dataclass

from django.core.management.base import BaseCommand
from django.db import transaction

from organizer.models import Video, VideoListSnapshot, VideoListSnapshotItem

SAMPLE_SNAPSHOT_NAME = "[seed] Manual liked videos snapshot"


@dataclass(frozen=True)
class SampleSnapshotItem:
    """Sample data for one seeded snapshot item."""

    position: int
    youtube_id: str
    title: str
    channel_title: str
    thumbnail_url: str
    availability: str


SAMPLE_ITEMS = (
    SampleSnapshotItem(
        position=0,
        youtube_id="seedvid0001",
        title="Sample introduction",
        channel_title="Workbench Samples",
        thumbnail_url="https://img.youtube.com/vi/seedvid0001/default.jpg",
        availability=VideoListSnapshotItem.Availability.AVAILABLE,
    ),
    SampleSnapshotItem(
        position=1,
        youtube_id="seedvid0002",
        title="Backend planning notes",
        channel_title="Workbench Samples",
        thumbnail_url="https://img.youtube.com/vi/seedvid0002/default.jpg",
        availability=VideoListSnapshotItem.Availability.AVAILABLE,
    ),
    SampleSnapshotItem(
        position=2,
        youtube_id="unavail0001",
        title="",
        channel_title="",
        thumbnail_url="",
        availability=VideoListSnapshotItem.Availability.UNAVAILABLE,
    ),
    SampleSnapshotItem(
        position=3,
        youtube_id="seedvid0003",
        title="Frontend integration pass",
        channel_title="Workbench Samples",
        thumbnail_url="https://img.youtube.com/vi/seedvid0003/default.jpg",
        availability=VideoListSnapshotItem.Availability.AVAILABLE,
    ),
)


class Command(BaseCommand):
    """Seed local snapshot data for manual API and frontend testing."""

    help = "Seed local sample video list snapshot data."

    @transaction.atomic
    def handle(self, *_args: object, **_options: object) -> None:
        """Create or refresh the local seed snapshot."""
        snapshot = (
            VideoListSnapshot.objects.filter(
                kind=VideoListSnapshot.Kind.MANUAL,
                name=SAMPLE_SNAPSHOT_NAME,
            )
            .order_by("id")
            .first()
        )
        if snapshot is None:
            snapshot = VideoListSnapshot.objects.create(
                kind=VideoListSnapshot.Kind.MANUAL,
                name=SAMPLE_SNAPSHOT_NAME,
            )

        VideoListSnapshotItem.objects.filter(snapshot=snapshot).delete()

        for sample_item in SAMPLE_ITEMS:
            video, _created = Video.objects.update_or_create(
                youtube_id=sample_item.youtube_id,
                defaults={
                    "title": sample_item.title,
                    "channel_title": sample_item.channel_title,
                    "thumbnail_url": sample_item.thumbnail_url,
                },
            )
            VideoListSnapshotItem.objects.create(
                snapshot=snapshot,
                video=video,
                position=sample_item.position,
                availability=sample_item.availability,
                captured_title=sample_item.title,
                captured_channel_title=sample_item.channel_title,
                captured_thumbnail_url=sample_item.thumbnail_url,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded snapshot {snapshot.id} with {len(SAMPLE_ITEMS)} items.",
            ),
        )
