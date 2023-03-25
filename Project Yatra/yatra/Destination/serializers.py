from rest_framework import serializers
from Destination.models import Destination,DestinationImage
from Activites.serializers import ActivitySerializer
   

class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImage
        fields = '__all__'


class DestinationSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    images = DestinationImageSerializer(many=True, read_only=True)
    activity=ActivitySerializer(many=True,read_only=True)
    class Meta:
        model = Destination
        fields =['id','name','description','ratings','is_favorite','is_area','average_price','related_keywords','latitude','longitude','location','images','activity']

    def get_is_favorite(self,obj):
        user_id = self.context.get('user_id')
        if user_id:
            return obj.favorite_by.filter(user_id=user_id).exists()
        return False 