from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser,FormParser


from .serializers import NewsSerializer,InfoSerializer,NewsImageSerializer,InfoImageSerializer
from .models import News,Info,InfoImage,NewsImage
from accounts.rendererss import UserRenderer

class NewsCreateView(generics.CreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= NewsSerializer
    queryset= News.objects.all()

class NewsUpdateView(generics.UpdateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= NewsSerializer
    queryset= News.objects.all()

class NewsListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= NewsSerializer
    queryset= News.objects.all()


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= InfoSerializer
    queryset= News.objects.all()

class NewsImageCreateView(generics.CreateAPIView):
    queryset = NewsImage.objects.all()
    serializer_class = NewsImageSerializer
    parser_classes = [MultiPartParser,FormParser]



class InfoCreateView(generics.CreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= InfoSerializer
    queryset= Info.objects.all()

class InfoUpdateView(generics.UpdateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= InfoSerializer
    queryset= Info.objects.all()

class InfoListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= InfoSerializer
    queryset= Info.objects.all()




class InfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= InfoSerializer
    queryset= Info.objects.all()


class InfoImageCreateView(generics.CreateAPIView):
    queryset = InfoImage.objects.all()
    serializer_class = InfoImageSerializer
    parser_classes = [MultiPartParser,FormParser]