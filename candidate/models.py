from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username




#dashboard wala

class Qualification(models.Model):
    EDUCATION_CHOICES = [
        ('Any Graduate', 'Any Graduate'),
        ('12th Pass or Below 12th', '12th Pass or Below 12th'),
        ('ITI', 'ITI'),
        ('Diploma', 'Diploma'),
        ('Post Graduate', 'Post Graduate'),
        ('MBA', 'MBA')
    ]

    Degree_Choice = [
    ('B.Com', 'B.Com'),
    ('BBA', 'BBA'),
    ('BCA', 'BCA'),
    ('BA', 'BA'),
    ('BSC', 'BSC'),
    ('B.Pharma', 'B.Pharma'),
    ('B.Tech', 'B.Tech'),
    ('B.E', 'B.E'),
    ('Other', 'Other'),
    ('Electrical', 'Electrical'),
    ('Mechanical', 'Mechanical'),
    ('Chemistry', 'Chemistry'),
    ('COPA', 'COPA'),
    ('AOCP', 'AOCP'),
    ('CNC', 'CNC'),
    ('Fitter', 'Fitter'),
    ('Turner', 'Turner'),
    ('Machine Operator', 'Machine Operator'),
    ('Welder', 'Welder'),
    ('IT', 'IT'),
    ('Chemical', 'Chemical'),
    ('Fire & Safety', 'Fire & Safety'),
    ('Electronics', 'Electronics'),
    ('Civil', 'Civil'),
    ('Management', 'Management'),
    ('MA', 'MA'),
    ('M.COM', 'M.COM'),
    ('MBA', 'MBA'),
    ('M.C.A', 'M.C.A'),
    ('M.E', 'M.E'),
    ('M.TECH', 'M.TECH'),
    ('M.SC', 'M.SC'),
    ('M.PHARMA', 'M.PHARMA'),
    ('Human Resource', 'Human Resource')
]
    
    COURSE_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Correspondence / Distance Learning', 'Correspondence / Distance Learning')
    ]
    
    # Fields for Qualifications model
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    education_level = models.CharField(max_length=50, choices=EDUCATION_CHOICES, null=True, blank=True)
    degree = models.CharField(max_length=100, choices=Degree_Choice, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    university = models.CharField(max_length=200, null=True, blank=True)
    course_type = models.CharField(max_length=50, choices=COURSE_TYPE_CHOICES, null=True, blank=True)
    passing_year = models.PositiveIntegerField(null=True, blank=True)


    education_board = models.CharField(max_length=200, null=True, blank=True)
    school_medium = models.CharField(max_length=100, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.degree} - {self.specialization}"
    

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    organisation = models.CharField(max_length=200, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)  # use 'designation'
    

    IS_CURRENT_COMPANY_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    # other fields as before
    is_current_company = models.CharField(max_length=3, choices=IS_CURRENT_COMPANY_CHOICES, null=True, blank=True)
    notice_period = models.PositiveIntegerField(null=True, blank=True)
    started_working_from = models.DateField(null=True, blank=True)
    key_skills = models.TextField(null=True, blank=True)
    job_profile = models.TextField(null=True, blank=True)
    responsible_person_name = models.CharField(max_length=200, null=True, blank=True)
    responsible_person_mobile = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.designation} at {self.organisation}"
    

class MyProfile(models.Model):
    pass


class UserProfile(models.Model):
    # Personal details
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    phone2 = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Unknown', 'Unknown')], default='Unknown')
    parent_name = models.CharField(max_length=200, null=True, blank=True)
    parent_phone = models.CharField(max_length=15, null=True, blank=True)
    nominee_name = models.CharField(max_length=200, null=True, blank=True)
    nominee_phone = models.CharField(max_length=15, null=True, blank=True)
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    # Professional details
    highest_qualification = models.CharField(max_length=200, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    work_status = models.CharField(max_length=100, null=True, blank=True)
    total_experience_years = models.PositiveIntegerField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)
    pan_card_number = models.CharField(max_length=10, null=True, blank=True)
    pf_number = models.CharField(max_length=20, null=True, blank=True)
    esic_number = models.CharField(max_length=20, null=True, blank=True)

    # Job search requirements
    job_location = models.CharField(max_length=200, null=True, blank=True)
    expected_salary_min = models.PositiveIntegerField(null=True, blank=True)
    expected_salary_max = models.PositiveIntegerField(null=True, blank=True)
    industries_required = models.BooleanField(default=False)
    department_required = models.BooleanField(default=False)
    shift_wise = models.BooleanField(default=False)
    facilities_needed = models.BooleanField(default=False)
    commitment_ready = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"








