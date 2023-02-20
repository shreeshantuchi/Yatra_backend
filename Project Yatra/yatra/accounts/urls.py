from django.urls import path
from accounts.views import UserRegistrationView,UserLoginView,UserPforileView,UserChangePasswordView,SendPasswordResetEmaiView,YatriView




urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name="register"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('profile/',UserPforileView.as_view(),name="profile"),
    path('changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
    path('send-rest-password-email/',SendPasswordResetEmaiView.as_view(),name="send-rest-password-email"),

    path('yatri/<int:pk>/', YatriView.as_view(), name='yatri'),



]