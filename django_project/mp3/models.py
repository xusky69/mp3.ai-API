import uuid
from statistics import mode
from accounts.models import User
from django.db import models


class Recording(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=32)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    transcript = models.TextField(blank=True, default='')

    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "MP3 Recording"
        verbose_name_plural = "MP3 Recordings"
    
    def __str__(self):
        return f"{self.user}_{self.name}_{self.uuid}"