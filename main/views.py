from django.template.context_processors import request
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated

from .models import Course, CustomUser, Mentor, Group, Student, PointType, GivePoint
from .serializers import CourseSerializer, CustomUserSerializer, MentorSerializer, GroupSerializer, StudentSerializer, \
    PointTypeSerializer, GivePointSerializer
from .permissions import IsAdmin, IsMentor, IsStudent, IsMentorOrAdmin


# noinspection DuplicatedCode
class CourseListCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# CustomUser Views
# class CustomUserListCreateView(ListCreateAPIView):
#     permission_classes = [IsAdmin]
#
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#
#
# class CustomUserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAdmin]
#
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer


# Mentor Views
class MentorListCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]

    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class MentorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]

    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


# Group Views
class GroupListCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# noinspection DuplicatedCode
class GroupRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# Student Views
class StudentListCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# PointType Views
class PointTypeListCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]

    queryset = PointType.objects.all()
    serializer_class = PointTypeSerializer


class PointTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]

    queryset = PointType.objects.all()
    serializer_class = PointTypeSerializer


# GivePoint Views
class GivePointListCreateView(ListCreateAPIView):
    queryset = GivePoint.objects.all()
    serializer_class = GivePointSerializer

    def get_permissions(self):
        # noinspection PyUnresolvedReferences
        if request.method == 'POST':
            return [IsMentorOrAdmin]
        elif request.method == 'GET':
            return [IsAuthenticated]
        else:
            return [IsAdmin]


class GivePointRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    queryset = GivePoint.objects.all()
    serializer_class = GivePointSerializer

    def get_permissions(self):
        # noinspection PyUnresolvedReferences
        if request.method == 'GET':
            return [IsAuthenticated]
        else:
            return [IsMentorOrAdmin]
