from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Profile, Qualification, Experience, MyProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email')


class RegisterSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15, write_only=True)
    country = serializers.CharField(max_length=255, write_only=True)
    skills = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'country', 'skills')

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number', None)
        country = validated_data.pop('country', None)
        skills = validated_data.pop('skills', None)

        user= User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()


        Profile.objects.create(
            user=user,
            phone_number=phone_number,
            country=country,
            skills=skills
        )
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)



#dashboard candidate

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

    def validate(self, attrs):
        education_level = attrs.get('education_level')

        if education_level == '12th Pass or Below 12th':
            if not attrs.get('education_board') or not attrs.get('school_medium') or not attrs.get('percentage'):
                raise serializers.ValidationError("Education Board, School Medium and Percentage are required for 12th Pass.")
    
        return attrs
    

# Serializer for Experience model
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProfile
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__' 