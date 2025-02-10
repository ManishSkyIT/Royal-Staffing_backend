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


class RegisterSerializer(serializers.ModelSerializer):
    profile = EmployeesProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)

        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )

        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()

        if profile_data:
            EmployeesProfile.objects.create(
                user=user,
                **profile_data
            )

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        profile = EmployeesProfile.objects.filter(user=instance).first()
        if profile:
            representation['profile'] = EmployeesProfileSerializer(profile).data

        return representation
    


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
