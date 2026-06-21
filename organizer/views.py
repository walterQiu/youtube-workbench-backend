from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from organizer.models import VideoListSnapshot, VideoListSnapshotItem
from organizer.serializers import (
    VideoListSnapshotItemSerializer,
    VideoListSnapshotSerializer,
)


@api_view(["GET"])
def health_check(_request: Request) -> Response:
    """Return a minimal API health response."""
    return Response({"status": "ok"})


@api_view(["GET"])
def snapshot_list(_request: Request) -> Response:
    """Return all video list snapshots."""
    snapshots = VideoListSnapshot.objects.annotate(item_count=Count("items"))
    serializer = VideoListSnapshotSerializer(snapshots, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def snapshot_detail(_request: Request, snapshot_id: int) -> Response:
    """Return one video list snapshot."""
    snapshot = get_object_or_404(
        VideoListSnapshot.objects.annotate(item_count=Count("items")),
        pk=snapshot_id,
    )
    serializer = VideoListSnapshotSerializer(snapshot)
    return Response(serializer.data)


@api_view(["GET"])
def snapshot_item_list(_request: Request, snapshot_id: int) -> Response:
    """Return ordered items for one video list snapshot."""
    snapshot = get_object_or_404(VideoListSnapshot, pk=snapshot_id)
    items = (
        VideoListSnapshotItem.objects.select_related("video")
        .filter(snapshot=snapshot)
        .order_by("position")
    )
    serializer = VideoListSnapshotItemSerializer(items, many=True)
    return Response(serializer.data)
