from rest_framework import serializers
from Activites.models import Activity,ActivityImage

class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityImage
        fields="__all__"


class ActivitySerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    images=ActivityImageSerializer(many=True,read_only=True)
    class Meta:
        model = Activity
        fields =['id','name','description','is_favorite','type','phone_no','location','average_price','related_keywords','latitude','longitude','images']

    def get_is_favorite(self,obj):
        user_id = self.context.get('user_id')
        if user_id:
            print("true")
            return obj.favorite_by.filter(user_id=user_id).exists()
        return False 