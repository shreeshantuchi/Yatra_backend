from rest_framework import serializers
from Food.models import Food,FoodImage


class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields='__all__'

class FoodSerializer(serializers.ModelSerializer):
    images =FoodImageSerializer(many=True,read_only=True)
    class Meta:
        model = Food
        fields =['name','description','type','phone_no','average_price','related_keywords','latitude','longitude','images']