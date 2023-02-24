from django.shortcuts import render
from rest_framework import generics


from .serializers import FoodSerializer
from Food.models import Food
from accounts.rendererss import UserRenderer

class FoodCreateView(generics.CreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= FoodSerializer
    queryset= Food.objects.all()

class FoodUpdateView(generics.UpdateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= FoodSerializer
    queryset= Food.objects.all()

class FoodListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= FoodSerializer
    queryset= Food.objects.all()
