from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser,FormParser


from .serializers import FoodSerializer,FoodImageSerializer
from Food.models import Food,FoodImage
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

class FoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= FoodSerializer
    queryset= Food.objects.all()


class FoodImageCreateView(generics.CreateAPIView):
    queryset = FoodImage.objects.all()
    serializer_class = FoodImageSerializer
    parser_classes = [MultiPartParser,FormParser]