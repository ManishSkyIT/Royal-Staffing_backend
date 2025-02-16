from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AdminStaff(models.Model):
    staff_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="admin_staffs", null=True)  

    # General Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    # Client Information
    client_code = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)

    # Login Information
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    # Professional Information
    pan_card_number = models.CharField(max_length=20, blank=True, null=True)
    aadhar_number = models.CharField(max_length=20, blank=True, null=True)
    pf_number = models.CharField(max_length=20, blank=True, null=True)
    esic_number = models.CharField(max_length=20, blank=True, null=True)

    # Nominee Information
    nominee_name = models.CharField(max_length=100, blank=True, null=True)
    nominee_phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Address Information
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    location_area = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    # Bank Details
    account_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)

    # Status
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    # DateTime automatic
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.staff_role})"
    

class RolePermission(models.Model):
    PERMISSION_CHOICES = [
        ('Admin & Staffs', 'Admin & Staffs'),
        ('Admin & Staff Roles', 'Admin & Staff Roles'),    
        ('Candidates', 'Candidates'),
        ('Employers', 'Employers'),
        ('Job Posts', 'Job Posts'),    
        ('Interviews', 'Interviews'),    
        ('HR - Education', 'HR - Education'),    
        ('HR - Job Categories', 'HR - Job Categories'),    
        ('HR - Job Timings', 'HR - Job Timings'),    
        ('Pages - SEO Details', 'Pages - SEO Details'),    
        ('Pages - Contact Info', 'Pages - Contact Info'),    
        ('Pages - Terms & Policies', 'Pages - Terms & Policies'),    
        ('Tools - Settings', 'Tools - Settings'),    
        ('Tools - App Versions', 'Tools - App Versions')
    ]

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")  
    permission_name = models.CharField(max_length=255, choices=PERMISSION_CHOICES)  
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.role.name} - {self.permission_name} (Read: {self.can_read}, Write: {self.can_write})"




#admin job post section ok

from django.db import models

class JobPost(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    client_name = models.CharField(max_length=255, blank=True, null=True)
    job_category = models.CharField(max_length=255, blank=True, null=True)
    job_sub_category = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    job_position = models.CharField(max_length=255)
    require_qualification = models.CharField(max_length=255)
    min_experience = models.IntegerField(blank=True, null=True)
    max_experience = models.IntegerField(blank=True, null=True)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    require_skills = models.TextField(blank=True, null=True)
    job_timing = models.CharField(max_length=255)
    joining_date = models.DateField(blank=True, null=True)
    last_interview_date = models.DateField(blank=True, null=True)
    
    # Salary & Facilities
    facilities = models.TextField(blank=True, null=True)
    ctc_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    in_hand_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_deduction_details = models.TextField(blank=True, null=True)

    # Job Location
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    area_landmark = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_title} - {self.client_name}"
