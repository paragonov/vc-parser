from rest_framework import serializers
from .models import VideoCardAbs


class VideoCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCardAbs
        fields = ['name', 'link', 'price', 'available']
