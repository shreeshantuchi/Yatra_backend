from django.contrib.auth import authenticate
from rest_framework import status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser

from rest_framework import generics

#for generating token
from rest_framework_simplejwt.tokens import RefreshToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


from accounts.rendererss import UserRenderer

from .models import (
    Yatri,
    SahayatriGuide,
    SahayatriExpert,
    Country,
    Location,
    Language,
    Interest,
    InterestRating
    
    )


from accounts.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserChangePasswordSearializer,
    UserProfileSearializer,
    SendPasswordResetEmailSerializer,
    YatriSerializer,
    SahayatriExpertSerializer,
    SahayatriGuideSerializer,
    LanguageSerializer,
    LocationSerializer,
    CountrySerializer,
    InterestSerializer,
    InterestRatingSerializer
)

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


# class UserPforileView(APIView):
#     renderer_classes =[UserRenderer]
#     permission_classes=[IsAuthenticated]
#     def get(self,request,format=None):
#         serializer=UserProfileSearializer(request.user)
#         return Response(serializer.data,status=status.HTTP_200_OK)


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
    parser_classes=[MultiPartParser,FormParser]


class SahayatriGuideView(generics.RetrieveUpdateAPIView):
    renderer_classes =[UserRenderer]
    # permission_classes=[IsAuthenticated]
    serializer_class = SahayatriGuideSerializer
    queryset = SahayatriGuide.objects.all()


# create view for guide/expert as list view the serializer also needs to be created

class SahayatriExpertView(generics.RetrieveUpdateAPIView):
    renderer_classes =[UserRenderer]
    # permission_classes=[IsAuthenticated]
    serializer_class = SahayatriExpertSerializer
    queryset = SahayatriExpert.objects.all()


class ShayatriGuideListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class = SahayatriGuideSerializer
    queryset = SahayatriGuide.objects.all()


class ShayatriExpertListView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class = SahayatriExpertSerializer
    queryset = SahayatriExpert.objects.all()

class CountryView(generics.ListCreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

class LocationAddView(generics.UpdateAPIView,generics.DestroyAPIView):
    renderer_classes =[UserRenderer]
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

class LocationView(generics.ListCreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

class LanguageView(generics.ListCreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()

class InterestView(generics.ListCreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()

# To return list
# class DestinationListView(generics.ListCreateAPIView):
#     queryset = Destination.objects.all()
#     serializer_class = DestinationSerializer

# urls
# path("destination/", DestinationListView.as_view(), name='destination-list')


class InterestRatingViewSet(viewsets.ModelViewSet):
    queryset = InterestRating.objects.all()
    serializer_class = InterestRatingSerializer