from rest_framework import serializers
from mp3.models import Recording


class RecordingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    audio_file = serializers.FileField(allow_empty_file=False, write_only=True, use_url=False)
    
    class Meta:
        model = Recording
        exclude = ['id', ]