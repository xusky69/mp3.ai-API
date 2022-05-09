from django.urls import include, path
from rest_framework.routers import DefaultRouter
from mp3.api.views import RecordingViewSet

router = DefaultRouter()
router.register(prefix=r"recordings",
                viewset=RecordingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]