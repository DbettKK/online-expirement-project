from job.models import student, notice
from job.serializers import CouSer, StudentSer, NoticeSer
from rest_framework.views import APIView, Response
from job.views import s_chk_token

# 学生端主页-课程列表 √
class student_course(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id
        print(stu_id)
        course_list = student.objects.get(pk=stu_id).Course.all()

        return Response({
            'info': 'success',
            'code': 200,
            'data': CouSer(course_list, many=True).data
        }, status=200)

# √
class student_modify_password(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        student_id = request.GET.get('student_id')
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')

        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id

        pwd = student.objects.get(pk=student_id).SPassword

        if old_pwd == pwd:
            update_pwd = student.objects.get(pk=student_id)
            update_pwd.SPassword = new_pwd
            update_pwd.save()

            return Response({
                'info': 'success',
                'code': 200,
                'data': StudentSer(update_pwd).data
            }, status=200)

        else:
            return Response({
                'info': '旧密码错误',
                'code': 403,
            }, status=403)


class student_get_notice(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id

        notice_list = notice.objects.all()

        return Response({
            'info': 'success',
            'code': 200,
            'data': NoticeSer(notice_list, many=True).data
        }, status=200)
