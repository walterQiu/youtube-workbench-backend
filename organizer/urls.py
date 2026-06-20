from django.urls import path

from organizer.views import (
    health_check,
    snapshot_detail,
    snapshot_item_list,
    snapshot_list,
)

app_name = "organizer"

urlpatterns = [
    path("health/", health_check, name="health"),
    path("snapshots/", snapshot_list, name="snapshot-list"),
    path("snapshots/<int:snapshot_id>/", snapshot_detail, name="snapshot-detail"),
    path(
        "snapshots/<int:snapshot_id>/items/",
        snapshot_item_list,
        name="snapshot-item-list",
    ),
]
