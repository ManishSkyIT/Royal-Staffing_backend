from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AdminStaff, Role 
from .models import Role, RolePermission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


from rest_framework import serializers
from .models import AdminStaff, Role  # ✅ Role Model Import किया

class AdminStaffSerializer(serializers.ModelSerializer):
    staff_role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=True)

    class Meta:
        model = AdminStaff
        fields = '__all__'
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email_address': {'required': True},
            'phone_number': {'required': True},
            'username': {'required': True},
            'password': {'required': True, 'write_only': True},  # ✅ Password कभी भी API Response में नहीं दिखेगा
            'country': {'required': True},
        }

    def __init__(self, *args, **kwargs):
        """✅ Update API में Username और Password Fields Hide करना"""
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        # ✅ PUT/PATCH Method पर Username और Password Remove कर दो
        if request and request.method in ['PUT', 'PATCH']:
            self.fields.pop('username', None)
            self.fields.pop('password', None)

    def create(self, validated_data):
        """✅ Create के समय Password Hash करना"""
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """✅ Update के समय Username और Password Accept ही न करें"""
        if 'username' in validated_data:
            raise serializers.ValidationError({"username": "Username cannot be updated."})
        if 'password' in validated_data:
            raise serializers.ValidationError({"password": "Password cannot be updated."})

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """✅ Update के समय Username और Password API Response से Remove करना"""
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method in ['GET', 'PUT', 'PATCH']:
            data.pop('username', None)  # ✅ Username Remove
            data.pop('password', None)  # ✅ Password Remove

        # ✅ Empty Fields Remove करें
        return {key: value for key, value in data.items() if value not in [None, "", [], {}]}

    

class AdminStaffListSerializer(serializers.ModelSerializer):
    admin_and_staff = serializers.SerializerMethodField()

    class Meta:
        model = AdminStaff
        fields = ['admin_and_staff', 'phone_number', 'email_address', 'created_at', 'status']

    def get_admin_and_staff(self, obj):
        return f"{obj.first_name} {obj.last_name}"



class RolePermissionSerializer(serializers.ModelSerializer):
    permission_name = serializers.ChoiceField(choices=RolePermission.PERMISSION_CHOICES)

    class Meta:
        model = RolePermission
        fields = ['permission_name', 'can_read', 'can_write']
        

class RoleSerializer(serializers.ModelSerializer):
    permissions = RolePermissionSerializer(many=True, required=False)

    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']




#new wala hai ye candidate ke liye

from rest_framework import serializers
from django.contrib.auth.models import User
from candidate.models import Profile  # ✅ Register Data `Profile` Model में है

class CandidateSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()
    phone_number = serializers.CharField(source='profile.phone_number')  # ✅ Profile से Phone Number
    education = serializers.CharField(source='profile.skills', default="Any Graduate")  # ✅ Profile से Education (Default: Any Graduate)
    experience = serializers.SerializerMethodField()  # ✅ Fresher / Experience
    created_at = serializers.DateTimeField(source='date_joined', format="%b %d, %Y %I:%M %p")  # ✅ Register Date
    status = serializers.CharField(default="Active")  # ✅ Default Status: Active

    class Meta:
        model = User  
        fields = ['id', 'candidate_name', 'experience', 'phone_number', 'email', 'education', 'created_at', 'status']

    def get_candidate_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_experience(self, obj):
        """✅ Work Status को Show करना (Fresher / Experience)"""
        profile = Profile.objects.filter(user=obj).first()
        return profile.work_status if profile else "Fresher"



#job post ke liye admin ka


from rest_framework import serializers
from admin_dashboard.models import JobPost

class JobPostSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = JobPost
        fields = "__all__"


from rest_framework import serializers
from employees.models import JobPost
class AdminJobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'  # ✅ Admin ke liye sab fields dikhni chahiye




#human resource ke liye


from rest_framework import serializers
from admin_dashboard.models import JobTiming

class JobTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTiming
        fields = "__all__"
