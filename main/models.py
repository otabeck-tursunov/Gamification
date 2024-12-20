from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        abstract = True


class Course(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser, BaseModel):
    ROLE_CHOICES = [
        ('mentor', 'Mentor'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)


class Mentor(CustomUser):
    point_limit = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'

    def save(self, *args, **kwargs):
        # Ensure the role field is always set to "mentor"
        self.role = 'mentor'
        super().save(*args, **kwargs)


class Group(BaseModel):
    NAME_CHOICES = [
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('Android', 'Android'),
        ('Grafik Dizayn', 'Grafik Dizayn'),
        ('Kiberxavfsizlik', 'Kiberxavfsizlik'),
    ]
    name = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField(default=1)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.number}"

    class Meta:
        unique_together = ('name', 'number')


class Student(CustomUser):
    birth_date = models.DateField()
    image = models.ImageField(upload_to='students/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    point = models.PositiveIntegerField(default=0)

    role = 'student'
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def save(self, *args, **kwargs):
        # Ensure the role field is always set to "student"
        self.role = 'student'
        super().save(*args, **kwargs)



class PointType(BaseModel):
    name = models.CharField(max_length=100)
    max_point = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class GivePoint(BaseModel):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.PositiveIntegerField()
    type = models.ForeignKey(PointType, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.student} {self.amount} {self.type}"

    def clean(self):
        """
        Custom validation:
        1. `amount` should not exceed `PointType.max_point`.
        2. Mentor must have enough point_limit to give.
        """
        if self.type and self.amount > self.type.max_point:
            raise ValidationError(f"Amount cannot exceed the max point of {self.type.max_point} for {self.type.name}.")

        if self.mentor and self.mentor.point_limit < self.amount:
            raise ValidationError(
                f"Mentor {self.mentor.username} does not have enough point_limit (available: {self.mentor.point_limit}).")

    def save(self, *args, **kwargs):
        """
        Save the Point and update Student's and Mentor's point_limit.
        """
        # Call the clean method to validate
        self.clean()

        # Fetch the previous instance of Point if exists
        if self.pk:
            # noinspection PyUnresolvedReferences
            prev_instance = GivePoint.objects.get(pk=self.pk)
            prev_student = prev_instance.student
            prev_mentor = prev_instance.mentor
            prev_amount = prev_instance.amount

            # Adjust previous point_limit
            if prev_student:
                prev_student.point -= prev_amount
                prev_student.save()
            if prev_mentor:
                prev_mentor.point_limit += prev_amount
                prev_mentor.save()

        # Save the new instance
        super().save(*args, **kwargs)

        # Update Student's point_limit
        if self.student:
            self.student.point += self.amount
            self.student.save()

        # Update Mentor's point_limit
        if self.mentor:
            self.mentor.point_limit -= self.amount
            self.mentor.save()
