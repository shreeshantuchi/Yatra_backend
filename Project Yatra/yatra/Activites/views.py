from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response


from .serializers import ActivitySerializer,ActivityImageSerializer
from Activites.models import Activity,ActivityImage
from accounts.rendererss import UserRenderer
from accounts.models import Yatri

class ActivityCreateView(generics.CreateAPIView):
    #renderer_classes =[UserRenderer]
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
    
    

class ActivityFavoriteListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= ActivitySerializer
    queryset= Activity.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id'] = self.kwargs['user_id']  # or however you get the user ID
        return context

class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= ActivitySerializer
    queryset= Activity.objects.all()


class ActivityImageCreateView(generics.CreateAPIView):
    queryset = ActivityImage.objects.all()
    serializer_class = ActivityImageSerializer
    parser_classes = [MultiPartParser,FormParser]


class ActivityFavoritesView(generics.GenericAPIView):
    serializer_class = ActivitySerializer
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = Yatri.objects.get(pk=self.kwargs['user_id'])
        activity = generics.get_object_or_404(Activity, pk=self.kwargs['activity_id'])
        activity.favorite_by.add(user)
        return Response(self.serializer_class(activity).data)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = Yatri.objects.get(pk=user_id)
        activity = generics.get_object_or_404(Activity, pk=self.kwargs['activity_id'])
        activity.favorite_by.remove(user)
        return Response(status=204)