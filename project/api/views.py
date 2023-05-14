from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from api.models import School, Administrator, Teacher, Student, Course
from api.serializers import (
    SchoolSerializer, 
    AdministratorSerializer, 
    TeacherSerializer, 
    StudentSerializer, 
    CourseSerializer, 
    TransferApiSerializer
)


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @action(detail=True, methods=['get'], url_path="stats")
    def get_stats(self, request, pk):
        if not pk.isdigit():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        schools = School.objects.all()
        get_object_or_404(schools, pk=pk)

        num_courses = Course.objects.filter(school=pk).count()
        num_administrators = Administrator.objects.filter(school=pk).count()
        num_teachers = Teacher.objects.filter(school=pk).count()
        num_students = Student.objects.filter(school=pk).count()
        stats = {
            "id": pk,
            "courses": num_courses,
            "admins": num_administrators,
            "teachers": num_teachers,
            "students": num_students
        }
        return Response(stats)


class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


@api_view(["POST"])
@transaction.atomic
def transfer(request):
    data = request.data
    errors = {}
    serializer = TransferApiSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    student = Student.objects.filter(id=data["studentId"]).first()
    course_to_remove_student = Course.objects.filter(id=data["fromCourseId"]).first()
    course_to_add_student = Course.objects.filter(id=data["toCourseId"]).first()
    if not student:
        errors["studentId"] = ["Student does not exists."]
    if not course_to_remove_student:
        errors["fromCourseId"] = ["Course does not exists."]
    elif not course_to_remove_student.students.filter(id=data["studentId"]).exists():
        errors["fromCourseId"] = ["Student is not enrolled."]
    if not course_to_add_student:
        errors["toCourseId"] = ["Course does not exists."]
    elif course_to_add_student.students.filter(id=data["studentId"]).exists():
        errors["toCourseId"] = ["Student is already enrolled."]
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    course_to_remove_student.students.remove(student)
    course_to_add_student.students.add(student)
    return Response({})