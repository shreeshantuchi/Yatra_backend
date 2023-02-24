from django.urls import path
from NewsandInfo.views import (
    NewsCreateView, 
    NewsListView,
    NewsUpdateView,
    InfoCreateView, 
    InfoListView,
    InfoUpdateView
    )


urlpatterns = [
    path('create/',NewsCreateView.as_view(),name="food_create"),
    path('update/<int:pk>',NewsUpdateView.as_view(),name="food_update"),
    path('list/',NewsListView.as_view(),name="food_list"),
    path('create/',InfoCreateView.as_view(),name="food_create"),
    path('update/<int:pk>',InfoUpdateView.as_view(),name="food_update"),
    path('list/',InfoListView.as_view(),name="food_list"),
]