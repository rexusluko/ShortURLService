from rest_framework import serializers
from .models import Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['original_url', 'short_url', 'created_at']

class DecodeLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['original_url']
