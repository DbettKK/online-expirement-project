from job.models import sign, StudentSign
from job.serializers import SignSer, StudentSignSer
from rest_framework.views import APIView, Response
from job.views import t_chk_token, chk_course_id, chk_sign_id


#get签到列表 √
class teacher_get_sign_list(APIView):
    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        course_id=request.GET.get('course_id')

        # 查token确认用户
        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id
        # 确认是哪门课
        c = chk_course_id(course_id)
        if isinstance(c, Response):
            return c

        # 获取签到列表
        sign_list = sign.objects.filter(Course=course_id)

        return Response({
            'info': 'success',
            'code': 200,
            'data': SignSer(sign_list, many=True).data
        }, status=200)


# 发布签到 √
class publish_sign(APIView):
    def post(self, request):
        token=request.META.get('HTTP_TOKEN')
        course_id=request.GET.get('course_id')

        title=request.POST.get('title')
        pubtime=request.POST.get('pubtime')
        endtime=request.POST.get('endtime')

        # 查token确认用户
        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id
        # 确认是哪门课
        c = chk_course_id(course_id)
        if isinstance(c, Response):
            return c

        create_sign=sign.objects.create(
            Title=title,
            PubTime=pubtime,
            EndTime=endtime,
            Course=c
        )

        return Response({
            'info': 'success',
            'code': 200,
            'data': SignSer(create_sign, many=True).data
        }, status=200)


# 删除签到 √
class delete_sign(APIView):
    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        sign_id=request.GET.get('sign_id')

        # 查token确认用户
        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        s = chk_sign_id(sign_id)
        if isinstance(s, Response):
            return s

        s.delete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': SignSer(s).data
        }, status=200)


# 学生签到详情
class sign_detail(APIView):
    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        sign_id=request.GET.get('sign_id')

        # 查token确认用户
        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        s = chk_sign_id(sign_id)
        if isinstance(s, Response):
            return s

        detail=StudentSign.objects.filter(sign=s)

        return Response({
            'info': 'success',
            'code': 200,
            'data': StudentSignSer(detail).data
        }, status=200)