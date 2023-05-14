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

class TransferApiSerializer(serializers.Serializer):
    studentId = serializers.IntegerField(required=True)
    fromCourseId = serializers.IntegerField(required=True)
    toCourseId = serializers.IntegerField(required=True)