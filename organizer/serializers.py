from typing import ClassVar

from rest_framework import serializers

from organizer.models import Video, VideoListSnapshot, VideoListSnapshotItem


class VideoSerializer(serializers.ModelSerializer):
    """Read-only representation of a known YouTube video."""

    class Meta:
        model = Video
        fields: ClassVar = [
            "id",
            "youtube_id",
            "title",
            "channel_title",
            "thumbnail_url",
        ]
        read_only_fields = fields


class VideoListSnapshotSerializer(serializers.ModelSerializer):
    """Read-only representation of a video list snapshot."""

    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = VideoListSnapshot
        fields: ClassVar = [
            "id",
            "kind",
            "name",
            "source_snapshot",
            "retrieved_at",
            "created_at",
            "updated_at",
            "item_count",
        ]
        read_only_fields = fields


class VideoListSnapshotItemSerializer(serializers.ModelSerializer):
    """Read-only representation of one ordered snapshot item."""

    video = VideoSerializer(read_only=True)

    class Meta:
        model = VideoListSnapshotItem
        fields: ClassVar = [
            "id",
            "position",
            "availability",
            "video",
            "captured_title",
            "captured_channel_title",
            "captured_thumbnail_url",
        ]
        read_only_fields = fields
