import uuid

import torchaudio
from accounts.models import User
from django.conf import settings
from django.db import models

from mp3.api.common import initialize_model_processor, transcript_file

(model, processor) = initialize_model_processor(model_name=settings.S2T_MODEL,
                                                processor_name=settings.S2T_PROCESSOR)


class Recording(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=32)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    audio_file = models.FileField(upload_to='audio_files/', blank=True)

    transcript = models.TextField(blank=True, default='', editable=False)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "MP3 Recording"
        verbose_name_plural = "MP3 Recordings"

    def __str__(self):
        return f"{self.user}_{self.name}_{self.uuid}"

    def save(self, *args, **kwargs):

        super(Recording, self).save(*args, **kwargs)

        audio_path = str(self.audio_file.path)

        data, sampling_rate = torchaudio.load(audio_path)

        data = data.reshape([-1])

        transcript = transcript_file(data=data,
                                     sampling_rate=sampling_rate,
                                     model=model,
                                     processor=processor)

        self.transcript = transcript[0]
