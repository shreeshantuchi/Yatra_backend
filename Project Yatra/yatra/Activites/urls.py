from django.urls import path
from Activites.views import ActivityCreateView,ActivityUpdateView,ActivityListView

urlpatterns = [
    path('create/',ActivityCreateView.as_view(),name="activity_create"),
    path('update/<int:pk>',ActivityUpdateView.as_view(),name="activity_update"),
    path('list/',ActivityListView.as_view(),name="activity_list"),
]

