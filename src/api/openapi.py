from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Note Management App API",
        default_version="v1",
        description="Test description",
    ),
    public=True,
    permission_classes=[AllowAny],
)
