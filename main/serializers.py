from rest_framework import serializers
from .models import Course, CustomUser, Mentor, Group, Student, PointType, GivePoint


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'created_at']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']


class MentorSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Mentor
        fields = ['id', 'username', 'role', 'point_limit', 'course']


class GroupSerializer(serializers.ModelSerializer):
    mentor = MentorSerializer()

    class Meta:
        model = Group
        fields = ['id', 'name', 'mentor', 'created_at']


class StudentSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = Student
        fields = ['id', 'username', 'birth_date', 'image', 'bio', 'point', 'group', 'role', 'created_at']


class PointTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointType
        fields = ['id', 'name', 'max_point', 'created_at']


class GivePointSerializer(serializers.ModelSerializer):
    mentor = MentorSerializer()
    student = StudentSerializer()
    type = PointTypeSerializer()

    class Meta:
        model = GivePoint
        fields = ['id', 'mentor', 'student', 'amount', 'type', 'description', 'date', 'created_at']

    def validate(self, data):
        """
        Custom validation for GivePoint
        """
        mentor = data.get('mentor')
        amount = data.get('amount')
        point_type = data.get('type')

        # Validate that the amount does not exceed the maximum allowed for the point type
        if point_type and amount > point_type.max_point:
            raise serializers.ValidationError(
                f"Amount cannot exceed the max point of {point_type.max_point} for {point_type.name}.")

        # Validate that the mentor has enough points to give
        if mentor and mentor.points < amount:
            raise serializers.ValidationError(
                f"Mentor {mentor.username} does not have enough points (available: {mentor.points}).")

        return data

    def create(self, validated_data):
        """
        Overriding the create method to update points after creating the GivePoint record
        """
        mentor = validated_data.get('mentor')
        student = validated_data.get('student')
        amount = validated_data.get('amount')

        # Create the GivePoint record
        give_point = super().create(validated_data)

        # Update points for Mentor and Student
        if mentor:
            mentor.points -= amount
            mentor.save()
        if student:
            student.points += amount
            student.save()

        return give_point

    def update(self, instance, validated_data):
        """
        Overriding the update method to handle the updating of points when the GivePoint is updated
        """
        mentor = validated_data.get('mentor', instance.mentor)
        student = validated_data.get('student', instance.student)
        amount = validated_data.get('amount', instance.amount)

        # Update the GivePoint record
        give_point = super().update(instance, validated_data)

        # Adjust points for Mentor and Student
        if instance.student:
            instance.student.points -= instance.amount
            instance.student.save()
        if instance.mentor:
            instance.mentor.points += instance.amount
            instance.mentor.save()

        if student:
            student.points += amount
            student.save()
        if mentor:
            mentor.points -= amount
            mentor.save()

        return give_point
