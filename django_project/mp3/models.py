import uuid

from accounts.models import User
from django.conf import settings
from django.db import models


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

    timestamps = models.BooleanField(editable=False)

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