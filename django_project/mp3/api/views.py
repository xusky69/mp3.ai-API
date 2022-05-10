import torchaudio
from django.conf import settings
from mp3.api.common import (analyze_sentiment, initialize_model_processor_S2T,
                            initialize_model_tokenizer_SENT, load_audio_file,
                            transcript_file)
from mp3.api.permissions import IsAuthorOrReadOnly
from mp3.api.serializers import RecordingSerializer
from mp3.models import Recording
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

(s2t_model, s2t_processor) = initialize_model_processor_S2T(model_name=settings.S2T_MODEL,
                                                            processor_name=settings.S2T_PROCESSOR)


(sent_model, sent_tokenizer) = initialize_model_tokenizer_SENT(model_name=settings.SENT_MODEL,
                                                               tokenizer_name=settings.SENT_TKNZR)


class RecordingViewSet(viewsets.ModelViewSet):
    serializer_class = RecordingSerializer
    lookup_field = "uuid"
    queryset = Recording.objects.all().order_by("-creation_date")
    permission_classes = [IsAuthorOrReadOnly] + [IsAuthenticated]
    filterset_fields = ('user__username')

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

        instance = serializer.instance
        audio_path = str(instance.audio_file.path)

        print(audio_path)

        data, sampling_rate = load_audio_file(audio_path)

        data = data.reshape([-1])

        transcript = transcript_file(data=data,
                                     sampling_rate=sampling_rate,
                                     model=s2t_model,
                                     processor=s2t_processor)

        instance.transcript = transcript[0]
        sentence = transcript[0]

        sentiment = analyze_sentiment(sentence=sentence,
                                      model=sent_model,
                                      tokenizer=sent_tokenizer)

        instance.sentiment_negative = sentiment[0]
        instance.sentiment_neutral = sentiment[1]
        instance.sentiment_positive = sentiment[2]

        instance.save()
