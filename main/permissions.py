from rest_framework import permissions
from rest_framework.permissions import *


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.role == 'mentor':
            return True
        else:
            return False


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.role == 'student':
            return True
        else:
            return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.role == 'admin':
            return True
        else:
            return False


class IsMentorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user and (request.user.role == 'mentor' or request.user.role == 'admin'):
            return True
        else:
            return False