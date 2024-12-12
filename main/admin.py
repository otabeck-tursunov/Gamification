from django.contrib import admin
from django.contrib.auth.models import Group as GroupModel

admin.site.unregister(GroupModel)

from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role')
    list_display_links = ('id', 'username')


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                'fields':
                    ('username', 'password')
            }
        ),
        (
            'Info',
            {
                'fields':
                    (
                        'first_name', 'last_name', 'course', 'point_limit', 'role'
                    )
            }
        ),
    )

    list_display = ('id', 'username', 'first_name', 'last_name', 'course', 'point_limit')
    list_display_links = ('id', 'username')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number', 'mentor')
    list_display_links = ('id', 'name')
    list_filter = ('mentor', 'active')
    search_fields = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'point', 'group')
    list_display_links = ('id', 'username')
    list_filter = ('group',)
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('point',)


@admin.register(PointType)
class PointTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'max_point')
    list_display_links = ('id', 'name')


@admin.register(GivePoint)
class GivePointAdmin(admin.ModelAdmin):
    list_display = ('id', 'mentor', 'student', 'amount', 'type', 'description', 'date')
    list_display_links = ('id', 'mentor', 'student')
    list_filter = ('mentor', 'student', 'type')
    search_fields = (
        'student__first_name', 'student__username', 'student__last_name', 'mentor__first_name', 'mentor__username',
        'mentor__last_name'
    )
