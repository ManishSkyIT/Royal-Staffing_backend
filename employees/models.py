from django.db import models
from django.contrib.auth.models import User

class EmployeesProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Profile')
    
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

    def __str__(self):
        return f"{self.user.username}'s Profile"
