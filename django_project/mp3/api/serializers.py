from rest_framework import serializers
from mp3.models import Recording


class RecordingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    audio_file = serializers.FileField(allow_empty_file=False, write_only=True, use_url=False)
    timestamps = serializers.JSONField(read_only=True)
    word_freqs = serializers.JSONField(read_only=True)

    class Meta:
        model = Recording
        exclude = ['id', ]