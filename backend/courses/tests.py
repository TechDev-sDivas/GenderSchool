from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Enrollment


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
            username='student', password='password', email='student@example.com'
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
