from django.urls import path

from organizer.views import health_check

app_name = "organizer"

urlpatterns = [
    path("health/", health_check, name="health"),
]
