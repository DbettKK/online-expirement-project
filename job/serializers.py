from rest_framework import serializers
from .models import manager, teacher, student, course, homework, question, answer, submission, analysis, notice, sign, StudentSign


class ManagerSer(serializers.ModelSerializer):

    class Meta:
        model = manager
        fields = '__all__'


class StudentSer(serializers.ModelSerializer):
    #student_courses = serializers.StringRelatedField(many=True)

    class Meta:
        model = student
        fields = '__all__'


class HomeworkSer(serializers.ModelSerializer):

    class Meta:
        model = homework
        fields = '__all__'


class CouSer(serializers.ModelSerializer):
    # course_students = StudentSer(many=True)
    teacher_name = serializers.CharField(source='Teacher.TeacherName')
    # course_homework = HomeworkSer(many=True)

    class Meta:
        model = course
        fields = '__all__'


class TeacherSer(serializers.ModelSerializer):

    class Meta:
        model = teacher
        fields = '__all__'


class QuestionSer(serializers.ModelSerializer):
    homework_title = serializers.CharField(source='Homework.Title')

    class Meta:
        model = question
        fields = '__all__'


class SubmissionSer(serializers.ModelSerializer):

    class Meta:
        model = submission
        fields = '__all__'


class StuAnswerSer(serializers.ModelSerializer):
    # Submission = SubmissionSer(many=True)

    class Meta:
        model = answer
        fields = '__all__'


class AnalysisSer(serializers.ModelSerializer):

    class Meta:
        model = analysis
        fields = '__all__'


class NoticeSer(serializers.ModelSerializer):

    class Meta:
        model = notice
        fields = '__all__'


class SignSer(serializers.ModelSerializer):

    class Meta:
        model = sign
        fields = '__all__'


class StudentSignSer(serializers.ModelSerializer):
    student_name=serializers.CharField(source='student.StudentName')

    class Meta:
        model = StudentSign
        fields = '__all__'