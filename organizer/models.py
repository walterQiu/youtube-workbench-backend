from typing import ClassVar

from django.db import models


class Video(models.Model):
    """A YouTube video known to the local organizer database."""

    # YouTube video IDs are currently 11 characters, but keep extra room.
    youtube_id = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=500, blank=True)
    channel_title = models.CharField(max_length=255, blank=True)
    thumbnail_url = models.URLField(max_length=2048, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ClassVar = ["youtube_id"]

    def __str__(self) -> str:
        """Return a readable video label."""
        if self.title:
            return f"{self.title} ({self.youtube_id})"
        return self.youtube_id


class VideoListSnapshot(models.Model):
    """A captured or user-defined state of an ordered video list."""

    class Kind(models.TextChoices):
        """Supported snapshot purposes."""

        ORIGINAL = "original", "Original"
        TARGET = "target", "Target"
        VERIFICATION = "verification", "Verification"
        MANUAL = "manual", "Manual"

    kind = models.CharField(max_length=32, choices=Kind.choices)
    name = models.CharField(max_length=255, blank=True)
    # Links derived snapshots, such as target or verification, back to a source.
    source_snapshot = models.ForeignKey(
        "self",
        related_name="derived_snapshots",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    retrieved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the external video list state was retrieved.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ClassVar = ["-created_at", "-id"]

    def __str__(self) -> str:
        """Return a readable snapshot label."""
        label = self.name or self.get_kind_display()
        return f"{label} snapshot #{self.pk}"


class VideoListSnapshotItem(models.Model):
    """One ordered video entry inside a video list snapshot."""

    class Availability(models.TextChoices):
        """Video availability observed for this snapshot item."""

        AVAILABLE = "available", "Available"
        UNAVAILABLE = "unavailable", "Unavailable"
        DELETED = "deleted", "Deleted"
        PRIVATE = "private", "Private"
        UNKNOWN = "unknown", "Unknown"

    snapshot = models.ForeignKey(
        VideoListSnapshot,
        related_name="items",
        on_delete=models.CASCADE,
    )
    video = models.ForeignKey(
        Video,
        related_name="list_snapshot_items",
        on_delete=models.PROTECT,
    )
    # Zero-based position matching the order observed or defined in the snapshot.
    position = models.PositiveIntegerField()
    availability = models.CharField(
        max_length=32,
        choices=Availability.choices,
        default=Availability.UNKNOWN,
    )
    captured_title = models.CharField(
        max_length=500,
        blank=True,
        help_text="Title observed when this snapshot item was captured.",
    )
    captured_channel_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Channel title observed when this snapshot item was captured.",
    )
    captured_thumbnail_url = models.URLField(
        max_length=2048,
        blank=True,
        help_text="Thumbnail URL observed when this snapshot item was captured.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ClassVar = ["snapshot", "position"]
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["snapshot", "position"],
                name="unique_position_per_video_list_snapshot",
            ),
            models.UniqueConstraint(
                fields=["snapshot", "video"],
                name="unique_video_per_video_list_snapshot",
            ),
        ]

    def __str__(self) -> str:
        """Return a readable snapshot item label."""
        return f"{self.snapshot_id}:{self.position} {self.video}"
