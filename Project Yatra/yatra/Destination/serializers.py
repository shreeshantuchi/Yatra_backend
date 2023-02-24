from rest_framework import serializers
from Destination.models import Destination
from accounts.models import Location


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        exclude = ['created_at','updated_at']
        