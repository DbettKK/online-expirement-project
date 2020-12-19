from job.models import teacher, manager, student, token
from rest_framework.views import APIView, Response
from job.serializers import ManagerSer, TeacherSer, StudentSer
from job.views import md5


# 三类用户登录视图 √
class login(APIView):
    authentication_classes = []

    def post(self, request):
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        ro = request.POST.get('role')

        if not all([uname, pwd]):
            return Response({
                'info': '参数不完整',
                'code': 400
            }, status=400)

        if ro == '1':
            try:
                m= manager.objects.get(ManagerNo=uname)
            except:
                return Response({
                    'info': '用户名不存在',
                    'code': 403
                }, status=403)
            if pwd == m.MPassword:
                # 登录成功后生成token
                token_str = md5(m.ManagerNo)
                token.objects.update_or_create(muser=m, defaults={'token': token_str})
                res = {'info': 'success', 'token': token_str, 'code': 200, 'data': ManagerSer(m).data}
                return Response(res)
            else:
                return Response({
                    'info': '密码错误',
                    'code': 403
                }, status=403)

        elif ro == '2':
            try:
                print(uname)
                t= teacher.objects.get(TeacherNo = uname)

            except:
                return Response({
                    'info': '用户名不存在',
                    'code': 403
                }, status=403)
            if pwd == t.TPassword:
                # 登录成功后生成token
                token_str = md5(t.TeacherNo)
                token.objects.update_or_create(tuser=t, defaults={'token': token_str})
                res = {'info': 'success', 'token': token_str, 'code': 200, 'data': TeacherSer(t).data}
                return Response(res)
            else:
                return Response({
                    'info': '密码错误',
                    'code': 403
                }, status=403)

        else:
            try:
                s = student.objects.get(StudentNo=uname)
            except:
                return Response({
                    'info': '用户名不存在',
                    'code': 403
                }, status=403)
            if pwd == s.SPassword:
                # 登录成功后生成token
                token_str = md5(s.StudentNo)
                token.objects.update_or_create(suser=s, defaults={'token': token_str})
                res = {'info': 'success', 'token': token_str, 'code': 200, 'data': StudentSer(s).data}
                return Response(res)
            else:
                return Response({
                    'info': '密码错误',
                    'code': 403
                }, status=403)