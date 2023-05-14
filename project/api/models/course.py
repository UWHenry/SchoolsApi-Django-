from django.db import models

from .school import School
from .teacher import Teacher
from .student import Student


class Course(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    location = models.TextField(blank=False, null=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=False)
    students = models.ManyToManyField(Student, blank=True)


    def __str__(self):
        return self.name