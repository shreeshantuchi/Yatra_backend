from rest_framework import serializers
from Food.models import Food,FoodImage


class FoodImageSerializer(serializers.ModelSerializer):
    favorites = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = FoodImage
        fields='__all__'

class FoodSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    images =FoodImageSerializer(many=True,read_only=True)
    class Meta:
        model = Food
        fields =('id','name','description','is_favorite','ratings','type','phone_no','location','average_price','related_keywords','latitude','longitude','images')

    def get_is_favorite(self,obj):
        user_id = self.context.get('user_id')
        if user_id:
            return obj.favorite_by.filter(user_id=user_id).exists()
        return False 