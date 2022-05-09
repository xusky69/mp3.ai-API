from mp3.api.permissions import IsAuthorOrReadOnly
from mp3.api.serializers import RecordingSerializer
from mp3.models import Recording
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class RecordingViewSet(viewsets.ModelViewSet):
    serializer_class = RecordingSerializer
    lookup_field = "uuid"
    queryset = Recording.objects.all().order_by("-creation_date")
    # permission_classes = [IsAuthorOrReadOnly] + [IsAuthenticated]
    filterset_fields = ('user__username')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

