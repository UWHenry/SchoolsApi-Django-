from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from drf_yasg.utils import swagger_auto_schema
from api.models import School, Administrator, Teacher, Student, Course
from api.serializers import (
    SchoolSerializer, 
    SchoolStatsResponse,
    AdministratorSerializer, 
    TeacherSerializer, 
    StudentSerializer, 
    CourseSerializer, 
    TransferApiRequest,
    TransferApiError
)


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @swagger_auto_schema(
        method='get',
        operation_description="get school stats",
        responses={
            200: SchoolStatsResponse,
            404: "School Not found."
        }
    )
    @action(detail=True, methods=['get'], url_path="stats")
    def get_stats(self, request, pk):
        if not pk.isdigit():
            return Response("School Not found.", status=status.HTTP_404_NOT_FOUND)
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
        return Response(SchoolStatsResponse(stats).data)


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

@swagger_auto_schema(
    method='post',
    request_body=TransferApiRequest,
    operation_description="transfer student from one course to another",
    responses={
        200: "Success",
        400: TransferApiError
    }
)
@api_view(["POST"])
@transaction.atomic
def transfer(request):
    data = request.data
    errors = {}
    serializer = TransferApiRequest(data=data)
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
        return Response(TransferApiRequest(errors).data, status=status.HTTP_400_BAD_REQUEST)

    course_to_remove_student.students.remove(student)
    course_to_add_student.students.add(student)
    return Response("Success")