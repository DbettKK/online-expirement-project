from job.models import sign, StudentSign, student
from job.serializers import SignSer, StudentSignSer
from rest_framework.views import APIView, Response
from job.views import s_chk_token, chk_sign_id, chk_course_id
import django.utils.timezone as timezone

#get签到 √
class student_get_sign(APIView):
    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        course_id=request.GET.get('course_id')

        # 查token确认用户
        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id
        stu = student.objects.get(pk=stu_id)

        # 确认是哪门课
        c = chk_course_id(course_id)
        if isinstance(c, Response):
            return c

        time_now = timezone.now()
        # 获取签到
        sign_ing = sign.objects.get(Course=c, EndTime__gt=time_now)
        sign_id = sign_ing.pk

        s = chk_sign_id(sign_id)
        if isinstance(s, Response):
            return s

        if len(StudentSign.objects.filter(student=stu, sign=s)) > 0:
            return Response({
                'info': '你已经完成签到了',
                'code': 403,
            }, status=403)

        else:
            return Response({
                'info': 'success',
                'code': 200,
                'data': StudentSignSer(sign_ing).data
            }, status=200)


# 完成签到
class sign(APIView):
    def post(self, request):
        token=request.META.get('HTTP_TOKEN')
        sign_id=request.GET.get('sign_id')
        sign_time=request.POST.get('sign_time')

        # 查token确认用户
        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id
        stu = student.objects.get(pk=stu_id)

        # 确认是哪个签到
        s = chk_sign_id(sign_id)
        if isinstance(s, Response):
            return s

        if len(StudentSign.objects.filter(student=stu, sign=s)) > 0:
            return Response({
                'info': '你已经完成签到了',
                'code': 403,
            }, status=403)

        else:
            create_sign=StudentSign.objects.create(
                student=stu,
                sign=s,
                SignTime=sign_time
            )

            return Response({
                'info': 'success',
                'code': 200,
                'data': StudentSignSer(create_sign).data
            }, status=200)
