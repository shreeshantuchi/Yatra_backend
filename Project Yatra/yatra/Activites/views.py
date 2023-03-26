from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from django.db.models import Case, When

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
    

class ActivityRecomendedListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class= ActivitySerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['user_id'] = self.kwargs['user_id']  # or however you get the user ID
        return context

    def get_queryset(self):
        import activityrecommender 
        from accounts.models import Interest
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
            if item.type =='ACT':
                names.append(item.name)
        print(names)
        # for interest in user_interests:
        #     Type,name=user_interests.split('/')
        #     print(Type,name)
        related_keywords_qs = Interest.objects.filter(name__in=names,type='ACT').values_list('related_keywords', flat=True)
        
        #converting to string
        related_keywords = ','.join(related_keywords_qs)
        
        # Call the recommender function to get a list of recommended food IDs
        recommended_food_ids = activityrecommender.activityrecomendation(user_location, related_keywords)
        
        # print(related_keywords)
        # print(user_location)

        recommended_food_ids=[x+1 for x in recommended_food_ids]
        # Query the database for the recommended food items, in the order returned by the recommender function
        queryset = Activity.objects.filter(id__in=recommended_food_ids).order_by(
            Case(*[When(id=id, then=pos) for pos, id in enumerate(recommended_food_ids)])
        )

        return queryset