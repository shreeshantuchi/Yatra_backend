from django.shortcuts import render
from rest_framework import generics


from .serializers import ActivitySerializer
from Activites.models import Activity
from accounts.rendererss import UserRenderer

class ActivityCreateView(generics.CreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= ActivitySerializer
    queryset= Activity.objects.all()

class ActivityUpdateView(generics.UpdateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= ActivitySerializer
    queryset= Activity.objects.all()

class ActivityListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= ActivitySerializer
    queryset= Activity.objects.all()