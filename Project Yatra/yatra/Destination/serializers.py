from rest_framework import serializers
from Destination.models import Destination,DestinationImage
   

class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImage
        fields = '__all__'


class DestinationSerializer(serializers.ModelSerializer):
    images = DestinationImageSerializer(many=True, read_only=True)
    class Meta:
        model = Destination
        fields =['name','description','is_city','average_price','related_keywords','latitude','longitude','images']