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
    ShayatriGuideListView,
    YatriInterestUpdateView,
    YatriInterestView,
    YatriLanguageUpdateView,
    YatriLanguageView,
    GuideLanguageUpdateView,
    GuideLanguageView,
    ExpertLanguageUpdateView,
    ExpertLanguageView
)




urlpatterns = [
    path('user/register/',UserRegistrationView.as_view(),name="register"),
    path('user/login/',UserLoginView.as_view(),name="login"),

    path('user/changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
    path('send-rest-password-email/',SendPasswordResetEmaiView.as_view(),name="send-rest-password-email"),

    path('user/yatri/<int:pk>/', YatriView.as_view(), name='yatri-profile'),
    
    path('user/expert/<int:pk>/', SahayatriExpertView.as_view(), name='expert_profile'),
    path('user/guide/<int:pk>/', SahayatriGuideView.as_view(), name='guide_profile'),

    path('expertlist/', ShayatriExpertListView.as_view(), name='expert_list'),
    path('guidelist/', ShayatriGuideListView.as_view(), name='guide_list'),


    path('countries/',CountryView.as_view(),name="countries"),
    path('languages/',LanguageView.as_view(),name="languages"),
    
    path('interests/',InterestView.as_view(),name="interests"),
    
    path('user/yatri/<int:yatri_id>/interest/', YatriInterestUpdateView.as_view(), name='yatri-interest-update'),
    path('user/yatri/<int:yatri_id>/interest/list/', YatriInterestView.as_view(), name='yatri-interest-list'),
    



    path('user/yatri/<int:yatri_id>/language/', YatriLanguageUpdateView.as_view(), name='yatri-language-update'),
    path('user/yatri/<int:yatri_id>/language/list/', YatriLanguageView.as_view(), name='yatri-language-list'),

    path('user/guide/<int:guide_id>/language/', GuideLanguageUpdateView.as_view(), name='guide-language-update'),
    path('user/guide/<int:guide_id>/language/list/', GuideLanguageView.as_view(), name='guide-language-list'),

    path('user/expert/<int:expert_id>/language/', ExpertLanguageUpdateView.as_view(), name='expert-language-update'),
    path('user/expert/<int:expert_id>/language/list/', ExpertLanguageView.as_view(), name='expert-language-list'),



]