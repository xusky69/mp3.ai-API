from rest_framework import serializers
from mp3.models import Recording


class RecordingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Recording
        exclude = ['id']
        # read_only_fields = ['audio_file']
