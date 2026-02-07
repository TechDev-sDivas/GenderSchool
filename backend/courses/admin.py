from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, Profile


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'price', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'instructor')
    inlines = [ModuleInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'progress', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

