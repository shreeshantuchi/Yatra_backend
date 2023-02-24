from django.shortcuts import render
from rest_framework import generics


from .serializers import NewsSerializer,InfoSerializer
from .models import News,Info
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