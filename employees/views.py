from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

from .models import EmployeesProfile


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            employee_profile = EmployeesProfile.objects.get(user=user)  # 🔹 Fetch employee profile

            # 🔴 Only allow login if status is 'approved'
            if employee_profile.status != "approved":
                return Response({'detail': 'Your account is not approved yet.'}, status=403)

        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=401)
        except EmployeesProfile.DoesNotExist:
            return Response({'detail': 'Employee profile not found'}, status=401)

        if not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=401)

        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_serializer.data
        })

    
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from employees.models import JobPost
# from job_applications.models import JobApplication  # Job Applications ka model (agar hai)

class DashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        # ✅ Total job posts count (logged-in user ke)
        total_job_posts = JobPost.objects.filter(created_by=user).count()

        # ✅ Total job applied (Filhal default 0 rakha hai)
        total_job_applied = 0

        return Response({
            'total_job_posts': total_job_posts,
            'total_job_applied': total_job_applied
        }, status=200)

    

#dashboard wala emp


from rest_framework import generics, permissions
from .models import JobPost
from .serializers import JobPostSerializer

# ✅ Job List API
class JobListView(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = (IsAuthenticated,)
    queryset = JobPost.objects.all().order_by('-created_att')
    serializer_class = JobPostSerializer
    # permission_classes = [permissions.IsAuthenticated]  # केवल लॉगिन यूजर ही देख सकते हैं

# ✅ Create Job API
from rest_framework import generics, permissions
from .models import JobPost
from .serializers import JobPostSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

# ✅ Employee Job Post API
class CreateJobView(generics.CreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer

    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)  # ✅ Employee ka job store hoga

    




class MyJobPostsView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobPostSerializer

    def get_queryset(self):
        user = self.request.user
        return JobPost.objects.filter(created_by=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        job_posts = queryset.values(
            'job_title', 'job_category', 'job_timing',
            'min_salary', 'max_salary', 'created_att', 'statuss'
        )

        return Response({"job_posts": job_posts})



from rest_framework import generics, permissions
from rest_framework.response import Response
from employees.models import EmployeesProfile
from employees.serializers import EmployeesProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class EmployeesProfileView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmployeesProfileSerializer

    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            employee_profile = user.employees_profile  # ✅ EmployeeProfile fetch karo
            serializer = self.get_serializer(employee_profile)

            # ✅ Name split karne ka logic
            full_name = employee_profile.authorised_person_name or ""
            name_parts = full_name.split(maxsplit=1)
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            # ✅ Only Required Fields Return Karna
            profile_data = {
                "company_name": employee_profile.company_name,
                "company_address": employee_profile.company_address,
                "gst_no": employee_profile.gst_no,
                "company_description": employee_profile.company_description,
                "company_email": employee_profile.company_email,
                "company_phone_number": employee_profile.company_phone_number,
                # "country": employee_profile.country,

                "authorised_person": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "position": employee_profile.authorised_person_position,
                    "phone_number": employee_profile.authorised_person_phone_number,
                    "email": employee_profile.authorised_person_email_address
                }
            }

            return Response(profile_data, status=200)

        except EmployeesProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)





from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from employees.models import EmployeesProfile
from employees.serializers import UpdateEmployeesProfileSerializer

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateEmployeesProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.employees_profile  # ✅ Sirf logged-in user ka profile update hoga
