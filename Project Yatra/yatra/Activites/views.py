from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser,FormParser


from .serializers import ActivitySerializer,ActivityImageSerializer
from Activites.models import Activity,ActivityImage
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

class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= ActivitySerializer
    queryset= Activity.objects.all()


class ActivityImageCreateView(generics.CreateAPIView):
    queryset = ActivityImage.objects.all()
    serializer_class = ActivityImageSerializer
    parser_classes = [MultiPartParser,FormParser]