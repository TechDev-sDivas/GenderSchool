from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Enrollment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_description = serializers.CharField(
        source='course.description', read_only=True
    )

    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'course', 'course_title',
            'course_description', 'progress', 'enrolled_at'
        ]
        read_only_fields = [
            'user', 'enrolled_at', 'course_title', 'course_description'
        ]


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    is_enrolled = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'price', 'instructor',
            'created_at', 'updated_at', 'is_enrolled', 'progress'
        ]

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(
                user=request.user, course=obj
            ).exists()
        return False

    def get_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                enrollment = Enrollment.objects.get(
                    user=request.user, course=obj
                )
                return enrollment.progress
            except Enrollment.DoesNotExist:
                return None
        return None
