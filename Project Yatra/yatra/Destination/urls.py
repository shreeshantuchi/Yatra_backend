from django.urls import path
from Destination.views import DestinationCreateView, DestinationListView,DestinationUpdateView,DestinationDetailView,DestinationImageCreateView


urlpatterns = [
    path('create/',DestinationCreateView.as_view(),name="destination_create"),
    path('update/<int:pk>',DestinationUpdateView.as_view(),name="destination_update"),
    path('view/<int:pk>',DestinationDetailView.as_view(),name="destination_view"),
    path('list/',DestinationListView.as_view(),name="destination_list"),
    path('<int:pk>/image/create/', DestinationImageCreateView.as_view(), name='destination-image-create'),

]