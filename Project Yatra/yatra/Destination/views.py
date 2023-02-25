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

class DestinationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= DestinationSerializer
    queryset= Destination.objects.all()

class DestinationImageCreateView(generics.CreateAPIView):
    queryset = DestinationImage.objects.all()
    serializer_class = DestinationImageSerializer
    parser_classes = [MultiPartParser,FormParser]

    def post(self, request, *args, **kwargs):
        destination = get_object_or_404(Destination, pk=kwargs['pk'])
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            image_data = serializer.validated_data['image']
            destination = serializer.validated_data['destination']
            image_file = ContentFile(base64.b64decode(image_data))
            image = DestinationImage(destination=destination, image=image_file)
            image.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)