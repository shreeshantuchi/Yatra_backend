from django.urls import path
from Food.views import (
FoodCreateView, 
FoodListView,
FoodUpdateView,
FoodDetailView,
FoodImageCreateView,
FoodRecomendedListView)

urlpatterns = [
    path('create/',FoodCreateView.as_view(),name="food_create"),
    path('update/<int:pk>/',FoodUpdateView.as_view(),name="food_update"),
    path('view/<int:pk>/',FoodDetailView.as_view(),name="activity_view"),
    path('list/',FoodListView.as_view(),name="food_list"),
    path('<int:pk>/image/create/', FoodImageCreateView.as_view(), name='food-image-create'),
    path('list/<int:user_id>/',FoodRecomendedListView.as_view(),name="food_recommend"),

]

