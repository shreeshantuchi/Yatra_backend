from django.urls import path
from Activites.views import (
    ActivityCreateView,
    ActivityUpdateView,
    ActivityListView,
    ActivityDetailView,
    ActivityImageCreateView,
    ActivityFavoritesView,
    ActivityFavoriteListView
    )
urlpatterns = [
    path('create/',ActivityCreateView.as_view(),name="activity_create"),
    path('update/<int:pk>/',ActivityUpdateView.as_view(),name="activity_update"),
    path('view/<int:pk>/',ActivityDetailView.as_view(),name="activity_view"),
    path('list/',ActivityListView.as_view(),name="activity_list"),
    path('<int:pk>/image/create/', ActivityImageCreateView.as_view(), name='activity-image-create'),
    path('<int:activity_id>/favorite/user=<int:user_id>/', ActivityFavoritesView.as_view(), name='activity-favorites'),
    path('list/<int:user_id>/',ActivityFavoriteListView.as_view(),name="activity_list"),
    path('recommend/<int:user_id>/',ActivityFavoriteListView.as_view(),name="activity_recomended"),
]

