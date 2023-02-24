from django.urls import path
from Food.views import FoodCreateView, FoodListView,FoodUpdateView


urlpatterns = [
    path('create/',FoodCreateView.as_view(),name="food_create"),
    path('update/<int:pk>',FoodUpdateView.as_view(),name="food_update"),
    path('list/',FoodListView.as_view(),name="food_list"),
]

