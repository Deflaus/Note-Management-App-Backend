from django.urls import path
from rest_framework.routers import DefaultRouter

from api.openapi import schema_view
from api.views.auth import AuthViewSet
from api.views.note import NoteViewSet

router = DefaultRouter()
router.register("auth", AuthViewSet, basename="auth")
router.register("note", NoteViewSet, basename="note")

urlpatterns = router.urls
urlpatterns += [
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
]
