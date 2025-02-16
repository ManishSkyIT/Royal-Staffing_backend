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




#new wala candidate dashboard ke liey

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from .serializers import CandidateSerializer  

class CandidateListView(ListAPIView):
    """✅ Admin Dashboard ke liye Registered Candidates Show karne ki API"""
    # authentication_classes = [JWTAuthentication]  
    # permission_classes = [IsAuthenticated]  
    queryset = User.objects.prefetch_related('profile').order_by('-date_joined')  # ✅ Profile ko Prefetch kiya  
    serializer_class = CandidateSerializer



#download excel

import openpyxl
from django.http import HttpResponse
from django.contrib.auth.models import User
from candidate.models import Profile, Qualification, Experience, UserProfile

def export_candidates_to_excel(request):
    """✅ Candidates Data को Excel में Export करने की API"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Candidates Data"

    # ✅ Header Row (जो आपने Provide किया है)
    headers = [
        "#", "Candidate", "Phone Number", "Email Address", "Education", "Highest Qualification",
        "Education Board", "Medium", "Course", "Specialization", "University", "Percentage",
        "Course Type", "Passing Year", "Highest Experience", "Organisation", "Designation",
        "Working From", "Working Till", "Work Status", "Skills", "Address_line_1",
        "Address_line_2", "Area", "Pincode", "Phone Number_2", "Whatsapp Number",
        "Gender", "Birth Date", "Parent Name", "Parent Phone", "Nominee Name", "Nominee Phone",
        "Aadhar Number", "Pan Number", "PF Number", "ESIC Number", "Created", "Status"
    ]
    ws.append(headers)

    # ✅ Fetch Candidates Data
    candidates = User.objects.prefetch_related('profile').all().order_by('-date_joined')

    for index, candidate in enumerate(candidates, start=1):
        profile = Profile.objects.filter(user=candidate).first()
        qualification = Qualification.objects.filter(user=candidate).first()
        experience = Experience.objects.filter(user=candidate).first()
        user_profile = UserProfile.objects.filter(email=candidate.email).first()

        ws.append([
            index,
            f"{candidate.first_name} {candidate.last_name}",
            profile.phone_number if profile else "",
            candidate.email,
            qualification.education_level if qualification else "",
            qualification.degree if qualification else "",
            qualification.education_board if qualification else "",
            qualification.school_medium if qualification else "",
            qualification.degree if qualification else "",
            qualification.specialization if qualification else "",
            qualification.university if qualification else "",
            qualification.percentage if qualification else "",
            qualification.course_type if qualification else "",
            qualification.passing_year if qualification else "",
            "Experience" if (profile and profile.work_status == "Experience") else "Fresher",
            experience.organisation if experience else "",
            experience.designation if experience else "",
            experience.started_working_from if experience else "",
            experience.is_current_company if experience else "",
            profile.work_status if profile else "",
            profile.skills if profile else "",
            user_profile.address_line1 if user_profile else "",
            user_profile.address_line2 if user_profile else "",
            user_profile.location if user_profile else "",
            user_profile.pincode if user_profile else "",
            user_profile.phone2 if user_profile else "",
            user_profile.whatsapp_number if user_profile else "",
            user_profile.gender if user_profile else "",
            user_profile.birth_date if user_profile else "",
            user_profile.parent_name if user_profile else "",
            user_profile.parent_phone if user_profile else "",
            user_profile.nominee_name if user_profile else "",
            user_profile.nominee_phone if user_profile else "",
            user_profile.aadhar_number if user_profile else "",
            user_profile.pan_card_number if user_profile else "",
            user_profile.pf_number if user_profile else "",
            user_profile.esic_number if user_profile else "",
            candidate.date_joined.strftime("%d-%m-%Y"),
            "Active"
        ])

    # ✅ Response as Excel File
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="candidates_data.xlsx"'
    wb.save(response)
    return response






#employee admin ke liye

from employees.models import EmployeesProfile
from employees.serializers import EmployeesProfileSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import UpdateAPIView

class EmployeeStatusUpdateView(UpdateAPIView):
    queryset = EmployeesProfile.objects.all()
    serializer_class = EmployeesProfileSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        employee = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ['approved', 'rejected']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        employee.status = new_status
        employee.save()

        return Response({"message": f"Employee status updated to {new_status}"}, status=status.HTTP_200_OK)
    



from rest_framework import generics, permissions
from rest_framework.response import Response
from employees.models import EmployeesProfile
from employees.serializers import EmployeesProfileSerializer

class EmployeesListView(generics.ListAPIView):
    queryset = EmployeesProfile.objects.all()
    serializer_class = EmployeesProfileSerializer
    permission_classes = [permissions.IsAdminUser]  # Sirf admin access kar sakega

    def list(self, request, *args, **kwargs):
        employees = self.get_queryset()
        data = []

        for emp in employees:
            data.append({
                "id": emp.id,
                "company_name": emp.company_name,
                "company_phone": emp.company_phone_number,
                "company_email": emp.company_email,
                "company_address": emp.company_address,
                "corporate_office_address": emp.corporate_office_address,
                "authorised_person": {
                    "name": emp.authorised_person_name,
                    "position": emp.authorised_person_position,
                    "phone": emp.authorised_person_phone_number,
                    "email": emp.authorised_person_email_address
                },
                "created_at": emp.created_at.strftime("%b %d, %Y %I:%M %p"),  # Jan 29, 2025 12:27 PM format
                "status": emp.status,
            })

        return Response(data)
    

class DeleteEmployeeView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, employee_id):
        employee = get_object_or_404(EmployeesProfile, id=employee_id)
        user = employee.user  # User bhi delete karna hoga

        employee.delete()  # EmployeesProfile delete
        user.delete()  # User bhi delete
        return Response({"message": "Employee deleted successfully"}, status=200)

# ✅ 3. View Single Employee Data
class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = EmployeesProfile.objects.all()
    serializer_class = EmployeesProfileSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_context(self):
        return {"request": self.request}




import openpyxl
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from employees.models import EmployeesProfile

class ExportEmployeesExcelView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # ✅ Excel Workbook aur Sheet Create karna
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Employees Data"

        # ✅ Header Row likhna
        headers = [
            "#", "Company", "Company Phone", "Company Email", "Company Address",
            "Corporate Address", "Authorised Person", "Position", "Phone Number",
            "Email Id", "Created", "Status"
        ]
        sheet.append(headers)

        # ✅ Employees Data Fill Karna
        employees = EmployeesProfile.objects.all()
        for index, emp in enumerate(employees, start=1):
            sheet.append([
                index,
                emp.company_name,
                emp.company_phone_number,
                emp.company_email,
                emp.company_address,
                emp.corporate_office_address,
                emp.authorised_person_name,
                emp.authorised_person_position,
                emp.authorised_person_phone_number,
                emp.authorised_person_email_address,
                emp.created_at.strftime("%d-%m-%Y"),
                emp.status,
            ])

        # ✅ Response Me Excel File Send Karna
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="employees_data.xlsx"'
        workbook.save(response)
        return response




#job post ka section ok admin ka


from rest_framework import generics, permissions
from admin_dashboard.models import JobPost
from admin_dashboard.serializers import JobPostSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# ✅ 1. Job List API (Admin)
class JobPostListView(generics.ListCreateAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # ✅ Sirf Admin access

    def get_queryset(self):
        return JobPost.objects.all()

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from employees.models import JobPost as EmployeeJobPost
from admin_dashboard.models import JobPost as AdminJobPost
from employees.serializers import JobPostSerializer
from admin_dashboard.serializers import AdminJobPostSerializer, JobPostSerializer
from django.core.exceptions import ObjectDoesNotExist

class AdminJobEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        """✅ Admin ke liye alag serializer, Employee ke liye alag"""
        job_id = self.kwargs["pk"]

        if AdminJobPost.objects.filter(id=job_id).exists():
            return JobPostSerializer  # ✅ Admin Job Ke Liye
        elif EmployeeJobPost.objects.filter(id=job_id).exists():
            return AdminJobPostSerializer  # ✅ Employee Job Ke Liye Bhi Admin Serializer (Kyuki Admin Edit Kar Raha Hai)
        return JobPostSerializer

    def get_object(self):
        job_id = self.kwargs["pk"]

        job = AdminJobPost.objects.filter(id=job_id).first()
        if job:
            return job

        job = EmployeeJobPost.objects.filter(id=job_id).first()
        if job:
            return job

        raise ObjectDoesNotExist("Job post not found")









from rest_framework.views import APIView

# ✅ Admin Ke Liye Job Delete API (Employee & Admin Dono Ke Jobs Ke Liye)
class AdminJobDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk, *args, **kwargs):
        try:
            job = AdminJobPost.objects.filter(id=pk).first()
            if not job:
                job = EmployeeJobPost.objects.filter(id=pk).first()

            if not job:
                return Response({"error": "Job post not found"}, status=404)

            job.delete()
            return Response({"message": "Job post deleted successfully"}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from admin_dashboard.models import JobPost as AdminJobPost
from employees.models import JobPost as EmployeeJobPost

class AdminAllJobsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        job_list = []

        # ✅ 1. Admin Ke Jobs Fetch Karo
        admin_jobs = AdminJobPost.objects.all()
        for job in admin_jobs:
            job_list.append({
                "id": job.id,
                "client_name": job.client_name,
                "job_details": f"Hiring: {job.job_title}, Location: {job.city}, {job.state}, Qualification: {job.require_qualification}",
                "job_category": job.job_category,
                "status": job.status,
            })

        # ✅ 2. Employee Ke Jobs Fetch Karo
        employee_jobs = EmployeeJobPost.objects.all()
        for job in employee_jobs:
            if job.created_by and hasattr(job.created_by, 'employees_profile'):
                employee_profile = job.created_by.employees_profile
                client_detail = f"{employee_profile.company_name} ({employee_profile.company_email})"
            else:
                client_detail = "Unknown"

            job_list.append({
                "id": job.id,
                "client_name": client_detail,  # ✅ Employee Ki Details Show
                "job_details": f"Hiring: {job.job_title}, Location: {job.city}, {job.state}, Qualification: {job.require_qualification}",
                "job_category": job.job_category,
                "statuss": job.statuss,
            })

        return Response(job_list, status=200)
