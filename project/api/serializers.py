from rest_framework import serializers

from api.models import School
from api.models import Administrator
from api.models import Teacher
from api.models import Student
from api.models import Course


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["name", "address"]

class SchoolStatsResponse(serializers.Serializer):
    id = serializers.IntegerField(required=True, label="School ID")
    courses = serializers.IntegerField(required=True, label="Number of courses")
    admins = serializers.IntegerField(required=True, label="Number of administrators")
    teachers = serializers.IntegerField(required=True, label="Number of teachers")
    students = serializers.IntegerField(required=True, label="Number of students")
    
class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = ["name", "school"]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["name", "school"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["name", "school"]

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["name", "location", "teacher", "school", "students"]

class TransferApiRequest(serializers.Serializer):
    studentId = serializers.IntegerField(required=True)
    fromCourseId = serializers.IntegerField(required=True)
    toCourseId = serializers.IntegerField(required=True)

class TransferApiError(serializers.Serializer):
    studentId = serializers.CharField(required=False, label="Error Message")
    fromCourseId = serializers.CharField(required=False, label="Error Message")
    toCourseId = serializers.CharField(required=False, label="Error Message")