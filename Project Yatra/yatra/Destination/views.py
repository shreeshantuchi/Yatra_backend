from django.shortcuts import render
from rest_framework import generics


from .serializers import DestinationSerializer
from Destination.models import Destination
from Destination.serializers import DestinationSerializer
from accounts.rendererss import UserRenderer

class DestinationCreateView(generics.CreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= DestinationSerializer
    queryset= Destination.objects.all()

class DestinationUpdateView(generics.UpdateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= DestinationSerializer
    queryset= Destination.objects.all()

class DestinationListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= DestinationSerializer
    queryset= Destination.objects.all()

