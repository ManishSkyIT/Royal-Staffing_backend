from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from .models import AdminStaff, Role
from .serializers import (
    LoginSerializer, UserSerializer, AdminStaffSerializer, 
    AdminStaffListSerializer, RoleSerializer 
)


User = get_user_model() 

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        """ Superuser & Admin/Staff dono ko Authenticate kare (Input Fields ke sath)"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # for super admin authenticate
        try:
            user = User.objects.get(email=email)
            if user.is_superuser and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "name": user.username,
                        "email": user.email
                    }
                }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass 

        # admin & staff authenticate
        admin_staff = get_object_or_404(AdminStaff, email_address=email)

        if admin_staff.status == "inactive":
            return Response({"error": "Your account is inactive. Please contact admin."}, status=status.HTTP_403_FORBIDDEN)

        if not admin_staff.check_password(password):
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not admin_staff.check_password(password):
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


        user, created = User.objects.get_or_create(username=admin_staff.email_address, defaults={"email": admin_staff.email_address})
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": admin_staff.id,
                "name": f"{admin_staff.first_name} {admin_staff.last_name}",
                "email": admin_staff.email_address
            }
        }, status=status.HTTP_200_OK)


class DashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_superadmins = User.objects.filter(is_superuser=True).count()
        total_admin_staff = AdminStaff.objects.count()
        total_all_admins = total_superadmins + total_admin_staff

        return Response({
            "dashboard": {
                # "total_candidates": Candidate.objects.count(),
                "total_signups": User.objects.count(),
                "total_admin_staff": total_all_admins
                # "total_employers": Employer.objects.count(),
                # "total_job_posts": JobPost.objects.count(),
                # "total_job_applied": JobApplication.objects.count()
            }
        }, status=200)
    


class AdminStaffCreateView(CreateAPIView):
    queryset = AdminStaff.objects.all()
    serializer_class = AdminStaffSerializer

    def create(self, request, *args, **kwargs):
        if not Role.objects.exists():
            return Response({"error": "No roles found! Create a role first."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        staff = AdminStaff.objects.all()
        serializer = AdminStaffSerializer(staff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AdminStaffListView(ListAPIView):
    queryset = AdminStaff.objects.all()
    serializer_class = AdminStaffListSerializer

class AdminStaffDeleteView(APIView):
    def get_object(self, pk):
        return get_object_or_404(AdminStaff, pk=pk)

    def delete(self, request, pk):
        staff = self.get_object(pk)
        staff.delete()
        return Response({"detail": "Admin staff deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class AdminStaffDetailView(APIView):
    def get(self, request, pk):
        staff = get_object_or_404(AdminStaff, pk=pk)  
        serializer = AdminStaffSerializer(staff)  
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminStaffUpdateView(RetrieveUpdateAPIView):
    queryset = AdminStaff.objects.all()
    serializer_class = AdminStaffSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ✅ Admin & Staff Roles API (Fixed)
from .models import Role
from .serializers import RoleSerializer

class AdminStaffRolesView(APIView):
    def get(self, request):
        """✅ Sirf Role Name aur Actions Show Karega"""
        roles = Role.objects.all().values("id", "name")  # ✅ Only Role Name aur ID fetch karega
        return Response(roles, status=status.HTTP_200_OK)

class AdminStaffRoleDetailView(APIView):
    def get(self, request, role_id):
        """✅ Jab Edit pe Click Kare to Role Details (Permissions) Show Karega"""
        role = get_object_or_404(Role, id=role_id)
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, role_id):
        """✅ Role Update (New Permissions Add) Karega"""
        role = get_object_or_404(Role, id=role_id)
        serializer = RoleSerializer(role, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, role_id):
        """✅ Role Delete Karega"""
        role = get_object_or_404(Role, id=role_id)
        role.delete()
        return Response({"message": "Role deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Role Creation with Permissions
from rest_framework.parsers import MultiPartParser, FormParser  
from .models import Role, RolePermission
from .serializers import RoleSerializer

class CreateRoleWithPermissionsView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        role_name = request.POST.get('name') 
        role = Role.objects.create(name=role_name)

        permission_names = request.POST.getlist('permission_name')
        can_read_values = request.POST.getlist('can_read') 
        can_write_values = request.POST.getlist('can_write')  

        for i in range(len(permission_names)):
            RolePermission.objects.create(
                role=role,
                permission_name=permission_names[i],
                can_read=can_read_values[i].lower() == 'true', 
                can_write=can_write_values[i].lower() == 'true'
            )

        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
