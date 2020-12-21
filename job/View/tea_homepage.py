from job.models import teacher, notice
from job.serializers import CouSer, TeacherSer, NoticeSer
from rest_framework.views import APIView, Response
from job.views import t_chk_token

# 教师端主页-课程列表 √
class teacher_course(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id


        course_list = teacher.objects.get(pk=tea_id).teacher_courses.all().order_by('CourseNo')

        return Response({
            'info': 'success',
            'code': 200,
            'data': CouSer(course_list, many=True).data
        }, status=200)

# √
class teacher_modify_password(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        teacher_id = request.POST.get('teacher_id')
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        pwd = teacher.objects.get(pk=teacher_id).TPassword

        if old_pwd == pwd:
            update_pwd = teacher.objects.get(pk=teacher_id)
            update_pwd.TPassword = new_pwd
            update_pwd.save()

            return Response({
                'info': 'success',
                'code': 200,
                'data': TeacherSer(update_pwd).data
            }, status=200)

        else:
            return Response({
                'info': '旧密码错误',
                'code': 403,
            }, status=403)


class teacher_get_notice(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        notice_list = notice.objects.all().order_by('-PubTime')

        return Response({
            'info': 'success',
            'code': 200,
            'data': NoticeSer(notice_list, many=True).data
        }, status=200)