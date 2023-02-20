from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics


from .models import Yatri


#for generating token
from rest_framework_simplejwt.tokens import RefreshToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#renderer start
from rest_framework import renderers
import json
class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self,data,accepted_media_type=None, renderer_context=None):
        response=''
        if 'ErrorDetail' in str(data):
            response=json.dumps({'errors':data})
        else:
            response=json.dumps(data)
        return response
#custom renderer

from django.contrib.auth import authenticate

from accounts.serializers import UserRegistrationSerializer,UserLoginSerializer,UserChangePasswordSearializer,UserProfileSearializer,SendPasswordResetEmailSerializer,YatriSerializer


class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serailizer=UserRegistrationSerializer(data=request.data)
        if serailizer.is_valid():
            user=serailizer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Sucessful'},status=status.HTTP_201_CREATED)
        
        return Response(serailizer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
  renderer_classes=[UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserPforileView(APIView):
    renderer_classes =[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSearializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes =[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserChangePasswordSearializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Sucessfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmaiView(APIView):
    renderer_classes =[UserRenderer]
    def post(self,request,formtat=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link Send. Please check your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class YatriView(generics.RetrieveUpdateAPIView):
    renderer_classes =[UserRenderer]
    # permission_classes=[IsAuthenticated]
    serializer_class = YatriSerializer
    queryset = Yatri.objects.all()



# To return list
# class DestinationListView(generics.ListCreateAPIView):
#     queryset = Destination.objects.all()
#     serializer_class = DestinationSerializer

# urls
# path("destination/", DestinationListView.as_view(), name='destination-list')