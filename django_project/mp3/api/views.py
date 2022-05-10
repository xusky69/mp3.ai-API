import torchaudio
from mp3.api.permissions import IsAuthorOrReadOnly
from mp3.api.serializers import RecordingSerializer
from mp3.models import Recording
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# from mp3.api.common import initialize_model_processor, transcript_file

# (model, processor) = initialize_model_processor(model_name=settings.S2T_MODEL,
#                                                 processor_name=settings.S2T_PROCESSOR)

class RecordingViewSet(viewsets.ModelViewSet):
    serializer_class = RecordingSerializer
    lookup_field = "uuid"
    queryset = Recording.objects.all().order_by("-creation_date")
    # permission_classes = [IsAuthorOrReadOnly] + [IsAuthenticated]
    filterset_fields = ('user__username')

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

        # instance = serializer.instance
        # audio_path = str(instance.audio_file.path)

        # data, sampling_rate = torchaudio.load(audio_path)

        # data = data.reshape([-1])

        # transcript = transcript_file(data=data,
        #                 sampling_rate=sampling_rate,
        #                 model=model,
        #                 processor=processor)

        # print(transcript[0])
        # self.request.data['audio_file']
    

