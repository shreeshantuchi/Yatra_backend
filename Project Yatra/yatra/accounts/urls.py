from django.urls import path
from accounts.views import (
    UserRegistrationView,
    UserLoginView,
    UserChangePasswordView,
    SendPasswordResetEmaiView,
    YatriView,
    InterestView,
    CountryView,
    LocationView,
    SahayatriExpertView,
    SahayatriGuideView,
    LanguageView,
    ShayatriExpertListView,
    ShayatriGuideListView
)




urlpatterns = [
    path('user/register/',UserRegistrationView.as_view(),name="register"),
    path('user/login/',UserLoginView.as_view(),name="login"),

    path('user/changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
    path('send-rest-password-email/',SendPasswordResetEmaiView.as_view(),name="send-rest-password-email"),

    path('user/yatri/<int:pk>/', YatriView.as_view(), name='yatri'),
    path('user/expertprofile/<int:pk>/', SahayatriExpertView.as_view(), name='expert_profile'),
    path('user/guideprofile/<int:pk>/', SahayatriGuideView.as_view(), name='guide_profile'),

    path('expertlist/', ShayatriExpertListView.as_view(), name='expert_list'),
    path('guidelist/', ShayatriGuideListView.as_view(), name='guide_list'),


    path('interests/',InterestView.as_view(),name="interests"),
    path('countries/',CountryView.as_view(),name="countries"),
    path('languages/',LanguageView.as_view(),name="languages"),





]