import json

from django.conf import settings
from mp3.api.permissions import IsAuthorOrReadOnly
from mp3.api.serializers import RecordingSerializer
from mp3.models import Recording
from rest_framework import viewsets
from mp3.common import (analyze_sentiment, get_word_freq,
                        initialize_model_VOSK,
                        initialize_model_processor_S2T,
                        initialize_model_tokenizer_SENT, load_audio_file,
                        split_words, transcript_file)


if settings.ENABLE_HFS2T:
    (s2t_model, s2t_processor) = initialize_model_processor_S2T(model_name=settings.S2T_MODEL,
                                                                processor_name=settings.S2T_PROCESSOR)

if settings.ENABLE_SENT:
    (sent_model, sent_tokenizer) = initialize_model_tokenizer_SENT(model_name=settings.SENT_MODEL,
                                                                   tokenizer_name=settings.SENT_TKNZR)

if settings.ENABLE_VOSK:
    model = initialize_model_VOSK(model_path=settings.VOSK_MODEL)


class RecordingViewSet(viewsets.ModelViewSet):
    serializer_class = RecordingSerializer
    lookup_field = "uuid"
    queryset = Recording.objects.all().order_by("-creation_date")
    permission_classes = [IsAuthorOrReadOnly]
    filterset_fields = ('user__username',)
    http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
        instance = serializer.instance
        word_list = list(set(split_words(words=instance.words)))
        instance.words = json.dumps(word_list)
        instance.save()

        if instance.timestamps and settings.ENABLE_VOSK:
            pass

        elif settings.ENABLE_HFS2T:

            audio_path = str(instance.audio_file.path)

            data, sampling_rate = load_audio_file(audio_path)
            data = data.reshape([-1])

            sentence = transcript_file(data=data,
                                       sampling_rate=sampling_rate,
                                       model=s2t_model,
                                       processor=s2t_processor)[0]

            instance.transcript = sentence

            instance.save()

        if settings.ENABLE_SENT and (settings.ENABLE_VOSK or
                                     settings.ENABLE_HFS2T):

            instance.words = json.dumps(get_word_freq(
                word_list=word_list, sentence=sentence))

            sentiment = analyze_sentiment(sentence=sentence,
                                          model=sent_model,
                                          tokenizer=sent_tokenizer)

            instance.sentiment_negative = sentiment[0]
            instance.sentiment_neutral = sentiment[1]
            instance.sentiment_positive = sentiment[2]

            instance.save()
