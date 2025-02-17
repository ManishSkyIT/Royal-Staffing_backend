from rest_framework import serializers
from django.contrib.auth.models import User
from employees.models import EmployeesProfile



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class EmployeesProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeesProfile
    
        fields = (
            'company_name', 'company_description', 'company_address', 
            'company_phone_number', 'company_email', 'corporate_office_address', 
            'gst_no', 'authorised_person_name', 'authorised_person_position', 
            'authorised_person_phone_number', 'authorised_person_email_address', 
            'login_phone_number', 'login_email', 'login_password'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request', None)

        if request and request.user.is_staff:  
            representation.pop('login_phone_number', None)
            representation.pop('login_email', None)
            representation.pop('login_password', None)

        return representation


class RegisterSerializer(serializers.ModelSerializer):
    profile = EmployeesProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)

        # ✅ User create karna
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()

        # ✅ EmployeesProfile create karna (default status = "requested")
        if profile_data:
            EmployeesProfile.objects.create(
                user=user,
                status="requested",  # Default status set karna
                **profile_data
            )

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # ✅ Profile ka data add karna response me
        profile = EmployeesProfile.objects.filter(user=instance).first()
        if profile:
            representation['profile'] = EmployeesProfileSerializer(profile).data

        return representation

    


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)



#dashboard wala emp

from rest_framework import serializers
from .models import JobPost
from admin_dashboard.models import JobTiming

class JobPostSerializer(serializers.ModelSerializer):
    job_timing = serializers.PrimaryKeyRelatedField(
        queryset=JobTiming.objects.all()  # ✅ Sirf Admin ke Banaye Hue Timings Show Honge
    )  

    class Meta:
        model = JobPost
        exclude = ['statuss']  # ✅ Employee ko status input nahi dikhega
        
    def create(self, validated_data):
        validated_data['statuss'] = 'requested'  # ✅ Auto set requested
        return super().create(validated_data)

    def validate(self, data):
        required_fields = [
            'job_title', 'job_description', 'job_position',
            'require_qualification', 'min_experience',
            'job_timing', 'address_line_1', 'country',
            'state', 'area_landmark', 'city'
        ]
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: "This field is required."})
        return data




from rest_framework import serializers
from employees.models import EmployeesProfile

class UpdateEmployeesProfileSerializer(serializers.ModelSerializer):
    authorised_person_first_name = serializers.CharField(source='authorised_person_name', required=False, allow_blank=True)
    authorised_person_last_name = serializers.SerializerMethodField()

    class Meta:
        model = EmployeesProfile
        fields = [
            "company_name", "company_description", "company_address", "company_phone_number",
            "company_email", "corporate_office_address", "gst_no",
            "authorised_person_first_name", "authorised_person_last_name",
            "authorised_person_position", "authorised_person_phone_number",
            "authorised_person_email_address"
        ]

    def get_authorised_person_last_name(self, obj):
        full_name = obj.authorised_person_name or ""
        name_parts = full_name.split(maxsplit=1)
        return name_parts[1] if len(name_parts) > 1 else ""

    def update(self, instance, validated_data):
        # ✅ First Name aur Last Name ko Properly Handle Karna
        first_name = validated_data.pop('authorised_person_name', instance.authorised_person_name)
        last_name = validated_data.pop('authorised_person_last_name', None)

        instance.authorised_person_name = f"{first_name} {last_name}".strip() if last_name else first_name

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
