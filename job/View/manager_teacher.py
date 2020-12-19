from job.models import teacher
from job.serializers import TeacherSer
from rest_framework.views import APIView, Response
from job.views import m_chk_token


class get_teacher_list(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        teacher_list = teacher.objects.all()

        return Response({
            'info': 'success',
            'code': 200,
            'data': TeacherSer(teacher_list, many=True).data
        }, status=200)


class add_teacher(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        teacher_no = request.POST.get('teacher_no')
        teacher_name=request.POST.get('teacher_name')
        teacher_gender = request.POST.get('teacher_gender')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        if len(teacher.objects.filter(TeacherNo=teacher_no)) > 0:
            return Response({
                'info': '该记录已存在',
                'code': 403,
            }, status=403)

        else:
            create_teacher = teacher.objects.create(
                TeacherNo=teacher_no,
                TeacherName=teacher_name,
                TeacherGender=teacher_gender,
                TPassword='123'
            )

            return Response({
                'info': 'success',
                'code': 200,
                'data': TeacherSer(create_teacher,many=True).data
            }, status=200)


class modify_teacher(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        teacher_id = request.GET.get('teacher_id')
        new_teacher_no = request.POST.get('new_teacher_no')
        new_teacher_name=request.POST.get('new_teacher_name')
        new_teacher_gender = request.POST.get('new_teacher_gender')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        update_teacher = teacher.objects.get(pk=teacher_id)
        update_teacher.TeacherNo=new_teacher_no
        update_teacher.TeacherName=new_teacher_name
        update_teacher.TeacherGender=new_teacher_gender
        update_teacher.save()

        all_teacher = teacher.objects.all()

        return Response({
            'info': 'success',
            'code': 200,
            'data': TeacherSer(all_teacher,many=True).data
        }, status=200)


class delete_teacher(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        teacher_id = request.GET.get('teacher_id')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        t = teacher.objects.get(pk=teacher_id)
        t.delete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': TeacherSer(t).data
        }, status=200)