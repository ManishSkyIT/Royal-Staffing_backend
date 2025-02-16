from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from .models import Qualification, Experience, UserProfile
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, QualificationSerializer, ExperienceSerializer, UserProfileSerializer




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Manually authenticate using email
        try:
            # Get the user by email
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=401)

        # Check if the password matches
        if not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=401)


        # If the user is found and password is correct, generate JWT tokens
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_serializer.data
        })
    

from rest_framework_simplejwt.authentication import JWTAuthentication
class DashboardView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = {
            'total_jobs_applied': 0,  # Agar jobs model ho, toh isko bhi filter kar sakte ho
            'total_qualifications': Qualification.objects.filter(user=request.user).count(),  # 👈 Sirf current user ke qualifications count
            'total_experiences': Experience.objects.filter(user=request.user).count(),  # 👈 Sirf current user ke experiences count
        }
        return Response(data)

    

class QualificationsView(generics.ListCreateAPIView):
    # permission_classes =(IsAuthenticated,)
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer

    def get_queryset(self):
        return Qualification.objects.filter(id=self.request.user.id)  # 👈 Sirf logged-in user ka data return karega

    def perform_create(self, serializer):
        serializer.save()  # 👈 Jo bhi qualification add karega, wo global nahi hoga 
        

class QualificationDestroyView(generics.DestroyAPIView):
    permission_classes =(IsAuthenticated,)
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


class QualificationUpdateView(generics.UpdateAPIView):
    permission_classes =(IsAuthenticated,)
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer



class ExperienceView(generics.ListCreateAPIView):
    # permission_classes =(IsAuthenticated,)
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


    def get_queryset(self):
        return Experience.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        
        serializer.save()


# Delete Experience
class ExperienceDestroyView(generics.DestroyAPIView):
    permission_classes =(IsAuthenticated,)
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


# Update Experience
class ExperienceUpdateView(generics.UpdateAPIView):
    permission_classes =(IsAuthenticated,)
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    
    def get(self, request, *args, **kwargs):
        experience = self.get_object()
        
        serializer = self.get_serializer(experience)
        
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class MyProfileView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=401)

        # Filter by email instead of user
        user_profile = UserProfile.objects.filter(email=request.user.email).first()

        if not user_profile:
            return Response({"error": "User profile not found"}, status=404)


    

        user_profile_data = UserProfileSerializer(user_profile).data if user_profile else {}

        qualifications = Qualification.objects.filter(user=request.user)  # ✅ Corrected filter
        experiences = Experience.objects.filter(user=request.user)  # ✅ Corrected filter

        qualification_data = QualificationSerializer(qualifications, many=True).data
        experience_data = ExperienceSerializer(experiences, many=True).data

        data = {
            "user_profile": user_profile_data,
            "qualifications": qualification_data if qualification_data else "Not Found",
            "experiences": experience_data if experience_data else "Not Found",
        }

        return Response(data)



class ProfileUpdateView(generics.UpdateAPIView):
    # permission_classes =(IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return UserProfile.objects.first()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return Response({
            "message": "Profile updated successfully!",
            "data": response.data 
        })
    




#admin dashboard ke liye candidate new
# from rest_framework.generics import ListAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from .models import UserProfile
# from .serializers import CandidateSerializer

# class CandidateListView(ListAPIView):
#     """✅ Admin Dashboard के लिए Registered Candidates Show करने की API"""
#     authentication_classes = [JWTAuthentication]  # ✅ Token Authentication Enable
#     permission_classes = [IsAuthenticated]  # ✅ सिर्फ Authenticated Users ही Access कर सकते हैं
#     queryset = UserProfile.objects.all().order_by('-id')  # ✅ Latest Candidates First Show होंगे
#     serializer_class = CandidateSerializer

