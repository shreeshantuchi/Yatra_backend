from django.urls import path
from NewsandInfo.views import (
    NewsCreateView, 
    NewsListView,
    NewsUpdateView,
    NewsDetailView,
    InfoCreateView, 
    InfoListView,
    InfoUpdateView,
    InfoDetailView
    )


urlpatterns = [
    path('create/',NewsCreateView.as_view(),name="food_create"),
    path('update/<int:pk>',NewsUpdateView.as_view(),name="food_update"),
    path('view/<int:pk>',NewsDetailView.as_view(),name="food_view"),
    path('list/',NewsListView.as_view(),name="food_list"),
    path('create/',InfoCreateView.as_view(),name="food_create"),
    path('update/<int:pk>',InfoUpdateView.as_view(),name="food_update"),
    path('list/',InfoListView.as_view(),name="food_list"),
    path('view/<int:pk>',InfoDetailView.as_view(),name="info_view"),

]