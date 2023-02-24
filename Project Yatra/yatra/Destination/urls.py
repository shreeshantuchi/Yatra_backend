from django.urls import path
from Destination.views import DestinationCreateView, DestinationListView,DestinationUpdateView


urlpatterns = [
    path('create/',DestinationCreateView.as_view(),name="destination_create"),
    path('update/<int:pk>',DestinationUpdateView.as_view(),name="destination_update"),
    path('list/',DestinationListView.as_view(),name="destination_list"),
]