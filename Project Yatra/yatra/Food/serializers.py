from rest_framework import serializers
from Food.models import Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        exclude = ['created_at','updated_at']