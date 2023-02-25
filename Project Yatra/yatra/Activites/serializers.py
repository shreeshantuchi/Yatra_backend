from rest_framework import serializers
from Activites.models import Activity,ActivityImage

class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityImage
        fields="__all__"


class ActivitySerializer(serializers.ModelSerializer):
    images=ActivityImageSerializer(many=True,read_only=True)
    class Meta:
        model = Activity
        fields =['name','description','type','phone_no','average_price','related_keywords','latitude','longitude','images']

