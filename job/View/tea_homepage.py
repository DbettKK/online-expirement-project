from job.models import teacher
from job.serializers import CouSer, TeacherSer
from rest_framework.views import APIView, Response
from job.views import t_chk_token

# 教师端主页-课程列表
class teacher_course(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        course_list = teacher.objects.get(pk=tea_id).teacher_courses.all()

        return Response({
            'info': 'success',
            'code': 200,
            'data': CouSer(course_list, many=True).data
        }, status=200)


class teacher_modify_password(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        teacher_id = request.GET.get('teacher_id')
        new_pwd = request.POST.get('new_pwd')

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        update_pwd = teacher.objects.get(pk=teacher_id)
        update_pwd.TPassword = new_pwd
        update_pwd.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': TeacherSer(update_pwd).data
        }, status=200)