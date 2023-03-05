from django.contrib.auth import authenticate
from rest_framework import status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser
from django.shortcuts import get_object_or_404

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
    Interest    
    )


from accounts.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserChangePasswordSearializer,
    UserProfileSearializer,
    SendPasswordResetEmailSerializer,
    YatriSerializerView,
    YatriSerializerUpdate,
    SahayatriExpertSerializer,
    SahayatriGuideSerializer,
    LanguageSerializer,
    LocationSerializer,
    CountrySerializer,
    InterestSerializer
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




class YatriView(generics.RetrieveAPIView):
    renderer_classes =[UserRenderer]
    # permission_classes=[IsAuthenticated]
    serializer_class = YatriSerializerView
    queryset = Yatri.objects.all()
    parser_classes=[MultiPartParser,FormParser]

class YatriUpdateView(generics.UpdateAPIView):
    renderer_classes =[UserRenderer]
    # permission_classes=[IsAuthenticated]
    serializer_class = YatriSerializerUpdate
    queryset = Yatri.objects.all()
    parser_classes=[MultiPartParser,FormParser]


class SahayatriGuideView(generics.RetrieveUpdateAPIView):
    renderer_classes =[UserRenderer]
    # permission_classes=[IsAuthenticated]
    serializer_class = SahayatriGuideSerializer
    queryset = SahayatriGuide.objects.all()
    parser_classes=[MultiPartParser,FormParser]


# create view for guide/expert as list view the serializer also needs to be created

class SahayatriExpertView(generics.RetrieveUpdateAPIView):
    renderer_classes =[UserRenderer]
    # permission_classes=[IsAuthenticated]
    serializer_class = SahayatriExpertSerializer
    queryset = SahayatriExpert.objects.all()
    parser_classes=[MultiPartParser,FormParser]


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
    parser_classes=[FormParser,MultiPartParser]

# view to  view language for yatri
class YatriLanguageView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class=LanguageSerializer
    
    def get_queryset(self):
        # Get the user profile object based on the user ID in the request
        user_id = self.kwargs['yatri_id']
        yatri = Yatri.objects.get(user_id=user_id)
        # Return the interests associated with the user profile
        return yatri.languages.all()

#Now to update the language for a yatri same as for interest
class YatriLanguageUpdateView(generics.UpdateAPIView):
    serializer_class = YatriSerializerView
    # permission_classes = [IsAuthenticated]
    
    def get_object(self):
        yatri_id = self.kwargs.get('yatri_id')
        return get_object_or_404(Yatri, pk=yatri_id)
    
    def update(self, request, *args, **kwargs):
        yatri = self.get_object()
        language_ids = request.data.get('languages', [])

        languages = Language.objects.filter(id__in=language_ids)
        # if len(interests) != len(interest_ids):
        #     return Response({'error': 'Please provide valid interest IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        yatri.languages.set(languages)

        serializer = self.get_serializer(yatri, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


# view to  view language for guide
class GuideLanguageView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class=LanguageSerializer
    
    def get_queryset(self):
        # Get the user profile object based on the user ID in the request
        user_id = self.kwargs['guide_id']
        sahayatri = SahayatriGuide.objects.get(user_id=user_id)
        # Return the interests associated with the user profile
        return sahayatri.languages.all()

#Now to update the language for a yatri same as for interest
class GuideLanguageUpdateView(generics.UpdateAPIView):
    serializer_class = SahayatriGuideSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_object(self):
        sahayatri_id = self.kwargs.get('guide_id')
        return get_object_or_404(SahayatriGuide, pk=sahayatri_id)
    
    def update(self, request, *args, **kwargs):
        sahayatri = self.get_object()
        language_ids = request.data.get('languages', [])

        languages = Language.objects.filter(id__in=language_ids)
        # if len(interests) != len(interest_ids):
        #     return Response({'error': 'Please provide valid interest IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        sahayatri.languages.set(languages)

        serializer = self.get_serializer(sahayatri, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

#languages for expert
class ExpertLanguageView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class=LanguageSerializer
    
    def get_queryset(self):
        # Get the user profile object based on the user ID in the request
        user_id = self.kwargs['expert_id']
        sahayatri = SahayatriExpert.objects.get(user_id=user_id)
        # Return the interests associated with the user profile
        return sahayatri.languages.all()

#Now to update the language for a yatri same as for interest
class ExpertLanguageUpdateView(generics.UpdateAPIView):
    serializer_class = SahayatriExpertSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_object(self):
        sahayatri_id = self.kwargs.get('expert_id')
        return get_object_or_404(SahayatriExpert, pk=sahayatri_id)
    
    def update(self, request, *args, **kwargs):
        sahayatri = self.get_object()
        language_ids = request.data.get('languages', [])

        languages = Language.objects.filter(id__in=language_ids)
        # if len(interests) != len(interest_ids):
        #     return Response({'error': 'Please provide valid interest IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        sahayatri.languages.set(languages)

        serializer = self.get_serializer(sahayatri, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class InterestView(generics.ListCreateAPIView):
    renderer_classes =[UserRenderer]
    serializer_class = InterestSerializer
    queryset = Interest.objects.all()



#replicate these parts for guide and expert
class YatriInterestView(generics.ListAPIView):
    renderer_classes =[UserRenderer]
    serializer_class=InterestSerializer
    
    def get_queryset(self):
        # Get the user profile object based on the user ID in the request
        user_id = self.kwargs['yatri_id']
        yatri = Yatri.objects.get(user_id=user_id)
        # Return the interests associated with the user profile
        return yatri.interests.all()


class YatriInterestUpdateView(generics.UpdateAPIView):
    serializer_class = YatriSerializerView
    # permission_classes = [IsAuthenticated]
    
    def get_object(self):
        yatri_id = self.kwargs.get('yatri_id')
        return get_object_or_404(Yatri, pk=yatri_id)
    
    def update(self, request, *args, **kwargs):
        yatri = self.get_object()
        interest_ids = request.data.get('interests', [])

        interests = Interest.objects.filter(id__in=interest_ids)
        # if len(interests) != len(interest_ids):
        #     return Response({'error': 'Please provide valid interest IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        yatri.interests.set(interests)

        serializer = self.get_serializer(yatri, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
# To return list
# class DestinationListView(generics.ListCreateAPIView):
#     queryset = Destination.objects.all()
#     serializer_class = DestinationSerializer

# urls
# path("destination/", DestinationListView.as_view(), name='destination-list')


