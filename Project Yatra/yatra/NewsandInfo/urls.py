from django.urls import path
from NewsandInfo.views import (
    NewsCreateView, 
    NewsListView,
    NewsUpdateView,
    NewsDetailView,
    NewsImageCreateView,
    InfoCreateView, 
    InfoListView,
    InfoUpdateView,
    InfoDetailView,
    InfoImageCreateView
    )


urlpatterns = [
    path('news/create/',NewsCreateView.as_view(),name="news_create"),
    path('news/update/<int:pk>/',NewsUpdateView.as_view(),name="news_update"),
    path('news/view/<int:pk>/',NewsDetailView.as_view(),name="news_view"),
    path('news/list/',NewsListView.as_view(),name="news_list"),
    path('news/<int:pk>/image/create/', NewsImageCreateView.as_view(), name='news-image-create'),
    path('info/create/',InfoCreateView.as_view(),name="info_create"),
    path('info/update/<int:pk>/',InfoUpdateView.as_view(),name="info_update"),
    path('info/list/',InfoListView.as_view(),name="info_list"),
    path('info/view/<int:pk>/',InfoDetailView.as_view(),name="info_view"),
    path('info/<int:pk>/image/create/', InfoImageCreateView.as_view(), name='info-image-create'),

]