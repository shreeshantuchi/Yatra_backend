from rest_framework import serializers
from Activites.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude = ['created_at','updated_at']