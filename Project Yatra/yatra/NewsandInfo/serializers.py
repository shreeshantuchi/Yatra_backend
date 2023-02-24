from rest_framework import serializers
from NewsandInfo.models import News,Info


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        exclude = ['created_at','updated_at']




class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        exclude = ['created_at','updated_at']