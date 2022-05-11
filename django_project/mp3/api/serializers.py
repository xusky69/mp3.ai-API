from rest_framework import serializers
from mp3.models import Recording


class RecordingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    audio_file = serializers.FileField(allow_empty_file=False, write_only=True)
    # words = serializers.CharField(write_only=True)

    class Meta:
        model = Recording
        exclude = ['id', ]
