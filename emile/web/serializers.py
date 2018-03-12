from rest_framework import serializers
from .models import WallMessages, Institution, CourseSectionStudents, CourseType, Users, Students, Program, Permissions, Destinations,Teachers, Courses, CourseSections
from django.utils import timezone

class InstitutionsSerializer(serializers.ModelSerializer):
    #student = StudentsSerializer(many=False, read_only=True)
    class Meta:
        model = Institution
        fields = '__all__'


class DestinationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destinations
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    messagedestinations = DestinationsSerializer(many=True, read_only=True)
    class Meta:
        model = Permissions
        fields = ('id','description','messagedestinations')


class UsersSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer(many=False, read_only=True)
    class Meta:
        model = Users
        fields = ('id', 'email', 'name','birth_date','gender','address','push_notification_token','image_path','permission')

class TeachersSerializer(serializers.ModelSerializer):
    user = UsersSerializer(many=False, read_only=True)
    class Meta:
        model = Teachers
        fields = ('user','siape')

class ProgramSerializer(serializers.ModelSerializer):
    coordinator = TeachersSerializer(many=False, read_only=True)

    class Meta:
        model = Program
        fields = ('id','name','abbreviation','total_hours','total_credits','institution','coordinator')

class StudentsSerializer(serializers.ModelSerializer):
    user = UsersSerializer(many=False, read_only=True)
    program = ProgramSerializer(many=False, read_only=True)
    class Meta:
        model = Students
        fields = ('user','enrollment','program')

class CourseTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseType
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(many=False, read_only=True)
    course_type = CourseTypeSerializer(many=False, read_only=True)
    class Meta:
        model = Courses
        fields = '__all__'

class CourseSectionsSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False, read_only=True)
    teacher = TeachersSerializer(many=False, read_only=True)
    class Meta:
        model = CourseSections
        fields = ('id','code','name','course','teacher','course_section_period')

class CourseSectionStudentsSerializer(serializers.ModelSerializer):
    #student = StudentsSerializer(many=False, read_only=True)
    class Meta:
        model = CourseSectionStudents
        fields = '__all__'

class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id','name')

class WallMessagesSerializer(serializers.ModelSerializer):
    sender = SenderSerializer(many=False, read_only=True)
    class Meta:
        model = WallMessages
        fields = ('id','date','sender','message','title')
