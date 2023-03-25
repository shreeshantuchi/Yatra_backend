from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser,FormParser
from django.db.models import Case, When
from rest_framework.response import Response

from .serializers import FoodSerializer,FoodImageSerializer
from Food.models import Food,FoodImage
from accounts.rendererss import UserRenderer
from accounts.models import Yatri,Interest
import foodrecomender

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


class FoodRecomendedListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= FoodSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id'] = self.kwargs['user_id']  # or however you get the user ID
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
            if item.type =='FOD':
                names.append(item.name)
        print(names)
        # for interest in user_interests:
        #     Type,name=user_interests.split('/')
        #     print(Type,name)
        related_keywords_qs = Interest.objects.filter(name__in=names,type='FOD').values_list('related_keywords', flat=True)
        
        #converting to string
        related_keywords = ','.join(related_keywords_qs)
        
        # Call the recommender function to get a list of recommended food IDs
        recommended_food_ids = foodrecomender.foodrecomendation(user_location, related_keywords)
        
        # print(related_keywords)
        # print(user_location)

        recommended_food_ids=[x+1 for x in recommended_food_ids]
        # Query the database for the recommended food items, in the order returned by the recommender function
        queryset = Food.objects.filter(id__in=recommended_food_ids).order_by(
            Case(*[When(id=id, then=pos) for pos, id in enumerate(recommended_food_ids)])
        )

        return queryset
    
class FoodPopularListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= FoodSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id'] = self.kwargs['user_id']  # or however you get the user ID
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
            if item.type =='FOD':
                names.append(item.name)
        print(names)
        # for interest in user_interests:
        #     Type,name=user_interests.split('/')
        #     print(Type,name)
        related_keywords_qs = Interest.objects.filter(name__in=names,type='FOD').values_list('related_keywords', flat=True)
        
        #converting to string
        related_keywords = ','.join(related_keywords_qs)
        
        # Call the recommender function to get a list of recommended food IDs
        recommended_food_ids = foodrecomender.foodpopular(user_location, related_keywords)
        
        # print(related_keywords)
        # print(user_location)

        recommended_food_ids=[x+1 for x in recommended_food_ids]
        # Query the database for the recommended food items, in the order returned by the recommender function
        queryset = Food.objects.filter(id__in=recommended_food_ids).order_by(
            Case(*[When(id=id, then=pos) for pos, id in enumerate(recommended_food_ids)])
        )

        return queryset
    
class FoodFavoritesView(generics.GenericAPIView):
    serializer_class = FoodSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = Yatri.objects.get(pk=self.kwargs['user_id'])
        food = generics.get_object_or_404(Food, pk=self.kwargs['food_id'])
        food.favorite_by.add(user)
        return Response(self.serializer_class(food).data)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = Yatri.objects.get(pk=user_id)
        food = generics.get_object_or_404(Food, pk=self.kwargs['food_id'])
        food.favorite_by.remove(user)
        return Response(status=204)