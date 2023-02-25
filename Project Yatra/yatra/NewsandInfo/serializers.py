from rest_framework import serializers
from NewsandInfo.models import News,Info,NewsImage,InfoImage


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields="__all__"


class NewsSerializer(serializers.ModelSerializer):
    images=NewsImageSerializer(many=True,read_only=True)
    class Meta:
        model = News
        fields =['topic','source_name','source_link','date','description','interest','realted_keywords','images']


class InfoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoImage
        fields="__all__"


class InfoSerializer(serializers.ModelSerializer):
    images=InfoImageSerializer(many=True,read_only=True)
    class Meta:
        model = Info
        fields =['topic','source_name','source_link','date','description','interest','realted_keywords','images']
