from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Course, Enrollment
import tempfile


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='profileuser', password='password'
        )

    def test_profile_creation(self):
        """Test if profile is created automatically via signal"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(str(self.user.profile), "profileuser's Profile")

    def test_profile_update(self):
        """Test profile update"""
        self.user.profile.bio = "Test Bio"
        self.user.profile.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.bio, "Test Bio")


class CourseModelTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='instructor', password='password'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            price=10.00,
            instructor=self.instructor
        )

    def test_course_creation(self):
        """Test if course is created correctly"""
        self.assertEqual(self.course.title, 'Test Course')
        self.assertEqual(self.course.instructor.username, 'instructor')
        self.assertEqual(str(self.course), 'Test Course')


class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='student', password='password'
        )
        self.instructor = User.objects.create_user(
            username='instructor', password='password'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            price=10.00,
            instructor=self.instructor
        )
        self.enrollment = Enrollment.objects.create(
            user=self.user, course=self.course
        )

    def test_enrollment_creation(self):
        """Test if enrollment is created correctly"""
        self.assertEqual(self.enrollment.user.username, 'student')
        self.assertEqual(self.enrollment.course.title, 'Test Course')
        self.assertEqual(self.enrollment.progress, 0)
        self.assertTrue(
            str(self.enrollment).startswith('student enrolled in Test Course')
        )


class CourseAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin', password='password', email='admin@example.com'
        )
        self.student = User.objects.create_user(
            username='student', password='password',
            email='student@example.com'
        )
        self.course_data = {
            'title': 'New Course',
            'description': 'New Description',
            'price': 20.00
        }
        self.instructor = User.objects.create_user(
            username='instructor', password='password'
        )
        self.course = Course.objects.create(
            title='Existing Course',
            description='Existing Description',
            price=10.00,
            instructor=self.instructor
        )

    def test_get_courses_public(self):
        """Test retrieving courses list without auth"""
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_course_admin(self):
        """Test admin can create course"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/courses/', self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_create_course_student_forbidden(self):
        """Test student cannot create course"""
        self.client.force_authenticate(user=self.student)
        response = self.client.post('/api/courses/', self.course_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_unauthenticated_forbidden(self):
        """Test unauthenticated user cannot create course"""
        response = self.client.post('/api/courses/', self.course_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_enroll_course(self):
        """Test student can enroll in a course"""
        self.client.force_authenticate(user=self.student)
        response = self.client.post(f'/api/courses/{self.course.id}/enroll/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)

        # Test duplicate enrollment
        response = self.client.post(f'/api/courses/{self.course.id}/enroll/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'already enrolled')


class AuthAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='password', email='test@example.com'
        )

    def test_login_username(self):
        """Test login with username"""
        response = self.client.post(
            '/api/login/', {'username': 'testuser', 'password': 'password'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_email(self):
        """Test login with email"""
        response = self.client.post(
            '/api/login/',
            {'username': 'test@example.com', 'password': 'password'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid(self):
        """Test login with wrong password"""
        response = self.client.post(
            '/api/login/',
            {'username': 'testuser', 'password': 'wrongpassword'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent(self):
        """Test login with nonexistent user"""
        response = self.client.post(
            '/api/login/',
            {'username': 'nouser', 'password': 'password'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        # Check if profile was created
        user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(user, 'profile'))


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ProfileAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='profiletest', password='password',
            email='profile@test.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        """Test retrieving user profile"""
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'profiletest')
        self.assertIn('profile', response.data)

    def test_update_profile_bio(self):
        """Test updating user bio"""
        data = {'bio': 'Updated Bio'}
        response = self.client.patch('/api/profile/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Updated Bio')

    def test_update_profile_photo(self):
        """Test updating user photo"""
        # Create a tiny 1x1 GIF (simplest valid image structure)
        # GIF89a + Logical Screen Descriptor + Image Descriptor + Data
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
            b'\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
            b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        )
        image = SimpleUploadedFile(
            "test_image.gif", image_content, content_type="image/gif"
        )
        data = {'photo': image}
        response = self.client.patch(
            '/api/profile/', data, format='multipart'
        )
        if response.status_code != 200:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.profile.photo)

    def test_update_user_fields(self):
        """Test updating standard user fields via profile endpoint"""
        data = {'first_name': 'NewName'}
        response = self.client.patch('/api/profile/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewName')
