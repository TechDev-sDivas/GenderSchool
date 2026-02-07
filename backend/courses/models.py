from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='modules'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name='lessons'
    )
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Content in Markdown/Text")
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrollments'
    )
    progress = models.IntegerField(default=0)  # 0 to 100
    enrolled_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    photo = models.ImageField(
        upload_to='profile_photos/', blank=True, null=True
    )
    bio = models.TextField(blank=True, max_length=500)

    def __str__(self):
        return f"{self.user.username}'s Profile"
