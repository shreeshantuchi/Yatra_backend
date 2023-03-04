from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
import base64
from django.core.files.base import ContentFile





from .serializers import DestinationSerializer
from Destination.models import Destination,DestinationImage
from Destination.serializers import DestinationSerializer,DestinationImageSerializer
from accounts.rendererss import UserRenderer
from Activites.serializers import ActivitySerializer
from Activites.models import Activity
from Food.serializers import FoodSerializer
from Food.models import Food

class DestinationCreateView(generics.CreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= DestinationSerializer
    queryset= Destination.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            destination = serializer.save()
            images_data = request.FILES.getlist('images')
            for image_data in images_data:
                destination_image = DestinationImage(destination=destination, image=image_data)
                destination_image.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestinationUpdateView(generics.UpdateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= DestinationSerializer
    queryset= Destination.objects.all()
    lookup_url_kwarg = 'destination_id'

class DestinationDetailView(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes =[UserRenderer]
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    lookup_url_kwarg = 'destination_id'

class DestinationListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= DestinationSerializer
    queryset= Destination.objects.all()

class DestinationImageCreateView(generics.CreateAPIView):
    queryset = DestinationImage.objects.all()
    serializer_class = DestinationImageSerializer
    parser_classes = [MultiPartParser,FormParser]


class ActivityListView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    def get_queryset(self):
        destination_id = self.kwargs.get('destination_id')
        print(destination_id)
        return Activity.objects.filter(destination__id=destination_id)
    

class FoodListView(generics.ListAPIView):
    serializer_class = FoodSerializer
    def get_queryset(self):
        destination_id = self.kwargs.get('destination_id')
        print(destination_id)
        return Food.objects.filter(destination__id=destination_id)