from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, CustomAuthToken, UserRegistrationView, EnrollmentViewSet,
    UserProfileView
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view()),
    path('register/', UserRegistrationView.as_view()),
    path('profile/', UserProfileView.as_view()),
]
