import uuid

from accounts.models import User
from django.conf import settings
from django.db import models

# from mp3.api.common import (initialize_model_processor_S2T,
#                             initialize_model_tokenizer_SENT,
#                             analyze_sentiment,
#                             load_audio_file,
#                             transcript_file)

# (s2t_model, s2t_processor) = initialize_model_processor_S2T(model_name=settings.S2T_MODEL,
#                                                             processor_name=settings.S2T_PROCESSOR)


# (sent_model, sent_tokenizer) = initialize_model_tokenizer_SENT(model_name=settings.SENT_MODEL,
#                                                                tokenizer_name=settings.SENT_TKNZR)

class Recording(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=32)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    audio_file = models.FileField(
        upload_to='audio_files/', blank=True, editable=False)

    sentiment_positive = models.FloatField(
        blank=True, default=0, editable=False)
    sentiment_negative = models.FloatField(
        blank=True, default=0, editable=False)
    sentiment_neutral = models.FloatField(
        blank=True, default=0, editable=False)

    transcript = models.TextField(blank=True, default='', editable=False)

    words = models.TextField(blank=True, default='', editable=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "MP3 Recording"
        verbose_name_plural = "MP3 Recordings"

    def __str__(self):
        return f"{self.user}_{self.name}_{self.uuid}"

    def save(self, *args, **kwargs):

        super(Recording, self).save(*args, **kwargs)

        # audio_path = str(self.audio_file.path)

        # data, sampling_rate = load_audio_file(audio_path)

        # data = data.reshape([-1])

        # transcript = transcript_file(data=data,
        #                              sampling_rate=sampling_rate,
        #                              model=s2t_model,
        #                              processor=s2t_processor)

        # self.transcript = transcript[0]
        # sentence = transcript[0]

        # sentiment = analyze_sentiment(sentence=sentence,
        #                               model=sent_model,
        #                               tokenizer=sent_tokenizer)

        # self.sentiment_negative = sentiment[0]
        # self.sentiment_neutral = sentiment[1]
        # self.sentiment_positive = sentiment[2]
