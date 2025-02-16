from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Profile, Qualification, Experience, MyProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email')


from rest_framework import serializers
from django.contrib.auth.models import User
from candidate.models import Profile  

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15, write_only=True)  
    country = serializers.CharField(max_length=255, write_only=True)  
    skills = serializers.CharField(max_length=255, write_only=True)  
    work_status = serializers.ChoiceField(choices=Profile.WORK_STATUS_CHOICES, write_only=True, default='Fresher')  # ✅ Work Status Field Added  

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'country', 'skills', 'work_status')

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number', None)
        country = validated_data.pop('country', None)
        skills = validated_data.pop('skills', None)
        work_status = validated_data.pop('work_status', 'Fresher')  

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()

        Profile.objects.create(
            user=user,
            phone_number=phone_number,
            country=country,
            skills=skills,
            work_status=work_status  # ✅ Work Status Save कर रहे हैं
        )
        return user

    def to_representation(self, instance):
        """✅ Response में `work_status`, `phone_number`, `country`, `skills` Add करना"""
        data = super().to_representation(instance)
        profile = Profile.objects.filter(user=instance).first()
        if profile:
            data['phone_number'] = profile.phone_number
            data['country'] = profile.country
            data['skills'] = profile.skills
            data['work_status'] = profile.work_status  # ✅ Work Status Response में Show होगा
        return data




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


#new for admin candidate
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from candidate.models import Profile  # ✅ Candidate Register ka Data `Profile` me hai

# class CandidateSerializer(serializers.ModelSerializer):
#     candidate_name = serializers.SerializerMethodField()
#     phone_number = serializers.CharField(source='profile.phone_number')  # ✅ Profile se phone_number
#     country = serializers.CharField(source='profile.country')  # ✅ Profile se country
#     created_at = serializers.DateTimeField(source='date_joined', format="%b %d, %Y %I:%M %p")  # ✅ User ke `date_joined` ko `created_at` bana diya

#     class Meta:
#         model = User  # ✅ User Model se Data Fetch karenge
#         fields = ['id', 'candidate_name', 'phone_number', 'email', 'country', 'created_at']

#     def get_candidate_name(self, obj):
#         return f"{obj.first_name} {obj.last_name}"
