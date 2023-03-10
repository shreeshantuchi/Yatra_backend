from rest_framework import serializers
from Destination.models import Destination,DestinationImage
from Activites.serializers import ActivitySerializer
   

class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImage
        fields = '__all__'


class DestinationSerializer(serializers.ModelSerializer):
    images = DestinationImageSerializer(many=True, read_only=True)
    activity=ActivitySerializer(many=True,read_only=True)
    class Meta:
        model = Destination
        fields =['id','name','description','is_area','average_price','related_keywords','latitude','longitude','location','images','activity']