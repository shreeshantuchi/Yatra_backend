from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
import base64
from django.core.files.base import ContentFile
from django.db.models import Case, When






from .serializers import DestinationSerializer
from Destination.models import Destination,DestinationImage
from Destination.serializers import DestinationSerializer,DestinationImageSerializer
from accounts.rendererss import UserRenderer
from Activites.serializers import ActivitySerializer
from Activites.models import Activity
from Food.serializers import FoodSerializer
from Food.models import Food

from accounts.models import Yatri,Interest
import destinationrecomender


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
    
class DestinationRecomendedListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= DestinationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id'] = self.kwargs['user_id']  # or however you get the user ID
        print('activated')
        return context
    
    def get_queryset(self):
        # Get the user ID from the URL
        user_id = self.kwargs['user_id']

        # Get the user's location from the User model
        user = Yatri.objects.get(pk=user_id)
        user_location = user.get_address()

        # Get the user's interests from the query parameters
        user_interests = user.interests.all()
        lst=user_interests[0:]
        names=[]
        for item in lst:
            if item.type =='DES':
                names.append(item.name)
        print(names)
        # for interest in user_interests:
        #     Type,name=user_interests.split('/')
        #     print(Type,name)
        related_keywords_qs = Interest.objects.filter(name__in=names,type='DES').values_list('related_keywords', flat=True)
        
        #converting to string
        related_keywords = ','.join(related_keywords_qs)
        
        # Call the recommender function to get a list of recommended food IDs
        recommended_destination_ids = destinationrecomender.destinationrecomendation(user_location, related_keywords)
        
        # print(related_keywords)
        # print(user_location)

        recommended_destination_ids=[x+1 for x in recommended_destination_ids]
        # Query the database for the recommended food items, in the order returned by the recommender function
        queryset = Destination.objects.filter(id__in=recommended_destination_ids).order_by(
            Case(*[When(id=id, then=pos) for pos, id in enumerate(recommended_destination_ids)])
        )

        return queryset

class DestinationPopularListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= DestinationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id'] = self.kwargs['user_id']  # or however you get the user ID
        print('activated')
        return context
    
    def get_queryset(self):
        # Get the user ID from the URL
        user_id = self.kwargs['user_id']

        # Get the user's location from the User model
        user = Yatri.objects.get(pk=user_id)
        user_location = user.get_address()

        # Get the user's interests from the query parameters
        user_interests = user.interests.all()
        lst=user_interests[0:]
        names=[]
        for item in lst:
            if item.type =='DES':
                names.append(item.name)
        print(names)
        # for interest in user_interests:
        #     Type,name=user_interests.split('/')
        #     print(Type,name)
        related_keywords_qs = Interest.objects.filter(name__in=names,type='DES').values_list('related_keywords', flat=True)
        
        #converting to string
        related_keywords = ','.join(related_keywords_qs)
        
        # Call the recommender function to get a list of recommended food IDs
        recommended_destination_ids = destinationrecomender.destinationpopular(user_location, related_keywords)
        
        # print(related_keywords)
        # print(user_location)

        recommended_destination_ids=[x+1 for x in recommended_destination_ids]
        # Query the database for the recommended food items, in the order returned by the recommender function
        queryset = Destination.objects.filter(id__in=recommended_destination_ids).order_by(
            Case(*[When(id=id, then=pos) for pos, id in enumerate(recommended_destination_ids)])
        )

        return queryset

#for the likes
class DestinationFavoritesView(generics.GenericAPIView):
    serializer_class = DestinationSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = Yatri.objects.get(pk=self.kwargs['user_id'])
        destination = generics.get_object_or_404(Destination, pk=self.kwargs['destination_id'])
        destination.favorite_by.add(user)
        return Response(self.serializer_class(destination).data)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = Yatri.objects.get(pk=user_id)
        destination = generics.get_object_or_404(Destination, pk=self.kwargs['destination_id'])
        destination.favorite_by.remove(user)
        return Response(status=204)
