from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Enrollment, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'bio']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'profile'
        ]
        read_only_fields = ['id', 'username']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Profile fields
        if profile_data:
            profile, created = Profile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(
        source='profile.bio', required=False, allow_blank=True
    )
    photo = serializers.ImageField(source='profile.photo', required=False)
    remove_photo = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'bio',
            'photo', 'remove_photo'
        ]
        read_only_fields = ['id', 'username']

    def update(self, instance, validated_data):
        # Extract profile data using source structure or manual pop
        # Note: 'source' works great for read, but for write with nested source,
        # DRF's ModelSerializer.update() might not handle creating the related
        # object automatically if it doesn't exist.

        remove_photo = validated_data.pop('remove_photo', False)
        
        profile_data = {}
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')

        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Profile fields
        profile, created = Profile.objects.get_or_create(user=instance)
        
        if remove_photo:
            profile.photo.delete(save=False)
            profile.photo = None
            profile.save()
        elif profile_data:
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


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
