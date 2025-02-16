from django.db import models
from django.contrib.auth.models import User

class EmployeesProfile(models.Model):

    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employees_profile')
    
    # Company Details
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_description = models.TextField(null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_phone_number = models.CharField(max_length=15, null=True, blank=True)
    company_email = models.EmailField(null=True, blank=True)
    corporate_office_address = models.CharField(max_length=255, null=True, blank=True)
    gst_no = models.CharField(max_length=20, null=True, blank=True)
    
    # Authorised Person Details
    authorised_person_name = models.CharField(max_length=255, null=True, blank=True)
    authorised_person_position = models.CharField(max_length=100, null=True, blank=True)
    authorised_person_phone_number = models.CharField(max_length=15, null=True, blank=True)
    authorised_person_email_address = models.EmailField(null=True, blank=True)

    # Login Details
    login_phone_number = models.CharField(max_length=15, null=True, blank=True)
    login_email = models.EmailField(null=True, blank=True)
    login_password = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')



    def __str__(self):
        return f"{self.user.username}'s Profile"
    


from django.db import models
from django.contrib.auth.models import User

class JobPost(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),  
        ('approved', 'Approved'),
    ]

    job_category = models.CharField(max_length=255)
    job_sub_category = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    job_position = models.CharField(max_length=255)
    require_qualification = models.CharField(max_length=255)
    min_experience = models.IntegerField()
    max_experience = models.IntegerField(null=True, blank=True)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    require_skills = models.TextField(null=True, blank=True)
    job_timing = models.CharField(max_length=255)
    joining_date = models.DateField(null=True, blank=True)
    last_interview_date = models.DateField(null=True, blank=True)

    # Salary and Facilities
    facilities = models.TextField(null=True, blank=True)
    ctc_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    in_hand_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_deduction_details = models.TextField(null=True, blank=True)

    # Location
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    area_landmark = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, default="India")
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # Metadata
    created_att = models.DateTimeField(auto_now_add=True)
    statuss = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_posts", null=True, blank=True)

    def __str__(self):
        return self.job_title
