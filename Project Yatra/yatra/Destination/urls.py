from django.urls import path
from Destination.views import (
    DestinationCreateView, 
    DestinationListView,
    DestinationUpdateView,
    DestinationDetailView,
    DestinationImageCreateView,
    ActivityListView,
    FoodListView,
    DestinationRecomendedListView,
    DestinationPopularListView,
    DestinationFavoritesView
)


urlpatterns = [
    path('create/',DestinationCreateView.as_view(),name="destination_create"),
    path('update/<int:pk>/',DestinationUpdateView.as_view(),name="destination_update"),
    path('view/<int:pk>/',DestinationDetailView.as_view(),name="destination_view"),


    path('list/',DestinationListView.as_view(),name="destination_list"),
    path('list/<int:user_id>/',DestinationRecomendedListView.as_view(),name="destination_recommendation"),
    path('popular/<int:user_id>/',DestinationPopularListView.as_view(),name="destination_popular"),
    path('<int:pk>/image/create/', DestinationImageCreateView.as_view(), name='destination-image-create'),
    path('<int:destination_id>/activity/',ActivityListView.as_view(),name="destination-activity_list"),
    path('<int:destination_id>/food/',FoodListView.as_view(),name="destination-food_list"),
    path('<int:destination_id>/favorite/user=<int:user_id>/', DestinationFavoritesView.as_view(), name='destination-favorites'),

]