from job.models import notice
from job.serializers import NoticeSer
from rest_framework.views import APIView, Response
from job.views import m_chk_token
import django.utils.timezone as timezone

# 请求公告列表 √
class get_notice_list(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        notice_list = notice.objects.all().order_by('-PubTime')

        return Response({
            'info': 'success',
            'code': 200,
            'data': NoticeSer(notice_list, many=True).data
        }, status=200)

# 添加公告 √
class add_notice(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        title = request.POST.get('title')
        content = request.POST.get('content')
        # pubtime = request.POST.get('pubtime')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        create_notice = notice.objects.create(
            Title=title,
            Content=content,
            PubTime=timezone.now()
        )

        return Response({
            'info': 'success',
            'code': 200,
            'data': NoticeSer(create_notice).data
        }, status=200)

# 删除公告 √
class delete_notice(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        notice_id = request.GET.get('notice_id')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        n = notice.objects.get(pk=notice_id)
        n.delete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': NoticeSer(n).data
        }, status=200)