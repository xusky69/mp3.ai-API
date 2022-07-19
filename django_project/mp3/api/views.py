import json

from django.conf import settings
from mp3.api.permissions import IsAuthorOrReadOnly
from mp3.api.serializers import RecordingSerializer
from mp3.common import (analyze_sentiment, get_word_freq,
                        initialize_model_tokenizer_SENT, initialize_model_vosk,
                        split_words, transcript_file_vosk)
from mp3.models import Recording
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

if settings.ENABLE_SENT:
    (sent_model, sent_tokenizer) = initialize_model_tokenizer_SENT(model_name=settings.SENT_MODEL,
                                                                   tokenizer_name=settings.SENT_TKNZR)

if settings.ENABLE_VOSK:
    model = initialize_model_vosk(model_path=settings.VOSK_MODEL)


class RecordingViewSet(viewsets.ModelViewSet):
    serializer_class = RecordingSerializer
    lookup_field = "uuid"
    queryset = Recording.objects.all().order_by("-creation_date")
    permission_classes = [IsAuthorOrReadOnly] + [IsAuthenticated]
    filterset_fields = ('user__username',)
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Recording.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
        instance = serializer.instance
        word_list = list(set(split_words(words=instance.words)))

        if settings.ENABLE_VOSK:

            audio_path = str(instance.audio_file.path)

            result = transcript_file_vosk(path=audio_path, model=model)

            sentence = result['text']

            instance.transcript = sentence

            instance.word_freqs = get_word_freq(
                word_list=word_list, sentence=sentence)

        if settings.ENABLE_VOSK and instance.get_timestamps:

            timestamps = list(
                filter(lambda item: item['word'] in word_list, result['result']))

            instance.timestamps = timestamps

        if settings.ENABLE_SENT and settings.ENABLE_VOSK:

            sentiment = analyze_sentiment(sentence=sentence,
                                          model=sent_model,
                                          tokenizer=sent_tokenizer)

            instance.sentiment_negative = sentiment[0]
            instance.sentiment_neutral = sentiment[1]
            instance.sentiment_positive = sentiment[2]

        instance.save()
