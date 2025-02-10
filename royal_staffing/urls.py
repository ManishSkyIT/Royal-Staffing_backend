from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from candidate.views import RegisterView as CandidateRegisterView, LoginView as CandidateLoginView, DashboardView as CandidateDashboardView, QualificationsView as CandidateQualificationsView, QualificationDestroyView as CandidateQualificationDestroyView, QualificationUpdateView as CandidateQualificationUpdateView, ExperienceView as CandidateExperienceView
from candidate.views import ExperienceDestroyView as CandidateExperienceDestroyView, ExperienceUpdateView as CandidateExperienceUpdateView, MyProfileView, ProfileUpdateView
from employees.views import RegisterView as EmployeeRegisterView, LoginView as EmployeeLoginView, DashboardView as EmployeeDashboardView
from admin_dashboard.views import LoginView, DashboardView,AdminStaffRolesView, AdminStaffCreateView, AdminStaffListView, AdminStaffDeleteView, CreateRoleWithPermissionsView, AdminStaffRoleDetailView
from admin_dashboard.views import AdminStaffDetailView, AdminStaffUpdateView

urlpatterns = [
    # Admin path
    path('admin/', admin.site.urls),

    # Authentication routes for candidate
    path('api/candidate/auth/register/', CandidateRegisterView.as_view(), name="auth_register_candidate"),
    path('api/candidate/auth/login/', CandidateLoginView.as_view(), name="auth_login_candidate"),
    path('api/candidate/token/', TokenObtainPairView.as_view(), name='token_obtain_pair_candidate'),
    path('api/candidate/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_candidate'),
    path('api/candidate/dashboard/', CandidateDashboardView.as_view(), name="dashboard_candidate"),
    path('api/candidate/qualifications/', CandidateQualificationsView.as_view(), name='qualifications_candidate'),
    path('api/candidate/qualifications/delete/<int:pk>/', CandidateQualificationDestroyView.as_view(), name='qualification-delete_candidate'),  # DELETE endpoint
    path('api/candidate/qualifications/update/<int:pk>/', CandidateQualificationUpdateView.as_view(), name='qualification-update'),  # PUT/PATCH for updating
    path('api/candidate/experiences/', CandidateExperienceView.as_view(), name='experiences'),
    path('api/candidate/experiences/delete/<int:pk>/', CandidateExperienceDestroyView.as_view(), name='experience-delete'),  # DELETE endpoint for experience
    path('api/candidate/experiences/update/<int:pk>/', CandidateExperienceUpdateView.as_view(), name='experience-update'),
    path('api/candidate/myprofile/', MyProfileView.as_view(), name='myprofile'),
    path('api/candidate/update-profile/', ProfileUpdateView.as_view(), name='update-profile'),


    # Authentication routes for employees
    path('api/employee/auth/register/', EmployeeRegisterView.as_view(), name="auth_register_employee"),
    path('api/employee/auth/login/', EmployeeLoginView.as_view(), name="auth_login_employee"),
    path('api/employee/token/', TokenObtainPairView.as_view(), name='token_obtain_pair_employee'),
    path('api/employee/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_employee'),
    path('api/employee/dashboard/', EmployeeDashboardView.as_view(), name="dashboard_employee"),
    

    # Authentication routes for admin_dashboard
    path('api/admin_dashboard/login/', LoginView.as_view(), name='login'),  # for login superadmin and admin & staff
    path('api/admin_dashboard/token/', TokenObtainPairView.as_view(), name='token_obtain_pair_candidate'), 
    path('api/admin_dashboard/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_candidate'),
    path('api/admin_dashboard/dashboard/', DashboardView.as_view(), name='dashboard'),  # Protected dashboard for both

    path('api/admin-staff/create/', AdminStaffCreateView.as_view(), name='admin_staff_create'), #create new admin & staff
    path('api/admin-staff/delete/<int:pk>/', AdminStaffDeleteView.as_view(), name='admin-staff-delete'), # delete admin and staff
    path('api/admin-staff/', AdminStaffListView.as_view(), name='admin_staff'), # admin & staff list page
    path('api/admin-staff/<int:pk>/', AdminStaffDetailView.as_view(), name='admin_staff_detail'), #view created admin & staff all data
    path('api/admin-staff/update/<int:pk>/', AdminStaffUpdateView.as_view(), name='admin_staff_update'),# Update Admin & Staff Profile

    path('api/admin_staff_roles/', AdminStaffRolesView.as_view(), name='admin_staff_roles'), #show only id and roles
    path('api/admin_staff_roles/<int:role_id>/', AdminStaffRoleDetailView.as_view(), name='admin-staff-role-detail'),  # Edit pe Click kare to Details dikhayega
    path('api/create-role-with-permissions/', CreateRoleWithPermissionsView.as_view(), name='create-role-with-permissions'),
    


]




