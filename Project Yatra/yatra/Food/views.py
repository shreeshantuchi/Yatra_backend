from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser,FormParser
from django.db.models import Case, When


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
        recommended_food_ids = recomender.foodrecomendation(user_location, related_keywords)
        
        # print(related_keywords)
        # print(user_location)

        recommended_food_ids=[x+1 for x in recommended_food_ids]
        # Query the database for the recommended food items, in the order returned by the recommender function
        queryset = Food.objects.filter(id__in=recommended_food_ids).order_by(
            Case(*[When(id=id, then=pos) for pos, id in enumerate(recommended_food_ids)])
        )

        return queryset