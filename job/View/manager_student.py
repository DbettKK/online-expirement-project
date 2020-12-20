from job.models import student
from job.serializers import StudentSer
from rest_framework.views import APIView, Response
from job.views import m_chk_token

# √
class get_student_list(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        student_list = student.objects.all().order_by('StudentNo')

        return Response({
            'info': 'success',
            'code': 200,
            'data': StudentSer(student_list, many=True).data
        }, status=200)

# √
class add_student(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        student_no = request.POST.get('student_no')
        student_name = request.POST.get('student_name')
        student_gender = request.POST.get('student_gender')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        if len(student.objects.filter(StudentNo=student_no)) > 0:
            return Response({
                'info': '该记录已存在',
                'code': 403,
            }, status=403)

        else:
            create_student = student.objects.create(
                StudentNo=student_no,
                StudentName=student_name,
                StudentGender=student_gender,
                SPassword='123'
            )

            return Response({
                'info': 'success',
                'code': 200,
                'data': StudentSer(create_student).data
            }, status=200)

# √
class modify_student(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        student_id = request.POST.get('student_id')
        new_student_no = request.POST.get('new_student_no')
        new_student_name = request.POST.get('new_student_name')
        new_student_gender = request.POST.get('new_student_gender')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        update_student = student.objects.get(pk=student_id)
        update_student.StudentNo = new_student_no
        update_student.StudentName = new_student_name
        update_student.StudentGender = new_student_gender
        update_student.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': StudentSer(update_student).data
        }, status=200)

# √
class delete_student(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        student_id = request.GET.get('student_id')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        s = student.objects.get(pk=student_id)
        s.delete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': StudentSer(s).data
        }, status=200)