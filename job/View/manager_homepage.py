from job.models import manager
from job.serializers import ManagerSer
from rest_framework.views import APIView, Response
from job.views import m_chk_token

# 管理员修改密码 √√
class manager_modify_password(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        manager_id = request.POST.get('manager_id')
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        pwd = manager.objects.get(pk=manager_id).MPassword

        if old_pwd==pwd:
            update_pwd = manager.objects.get(pk=manager_id)
            update_pwd.MPassword = new_pwd
            update_pwd.save()

            return Response({
                'info': 'success',
                'code': 200,
                'data': ManagerSer(update_pwd).data
            }, status=200)

        else:
            return Response({
                'info': '旧密码错误',
                'code': 400,
            }, status=400)