from job.models import course, teacher
from job.serializers import CouSer
from rest_framework.views import APIView, Response
from job.views import m_chk_token


# 请求所有课程列表 √
class get_course_list(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        course_list = course.objects.all()

        return Response({
            'info': 'success',
            'code': 200,
            'data': CouSer(course_list, many=True).data
        }, status=200)

# 添加课程 √
class add_course(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        course_no = request.POST.get('course_no')
        course_name = request.POST.get('course_name')
        teacher_no = request.POST.get('teacher_no')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        isExist = course.objects.filter(CourseNo=course_no)
        if len(isExist) > 0:
            return Response({
                'info': '该记录已存在',
                'code': 403,
            }, status=403)

        else:
            try:
                tea=teacher.objects.get(TeacherNo=teacher_no)
            except:
                return Response({
                    'info': '该教师不存在',
                    'code': 403,
                }, status=403)

            create_course = course.objects.create(
                CourseNo=course_no,
                CourseName=course_name,
                Teacher=tea
            )

            return Response({
                'info': 'success',
                'code': 200,
                'data': CouSer(create_course).data
            }, status=200)

# 修改课程 √
class modify_course(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        course_id = request.POST.get('course_id')
        new_course_no = request.POST.get('new_course_no')
        new_course_name = request.POST.get('new_course_name')
        new_teacher_no= request.POST.get('new_teacher_no')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        update_course = course.objects.get(pk=course_id)

        try:
            tea = teacher.objects.get(TeacherNo=new_teacher_no)
        except:
            return Response({
                'info': '该教师不存在',
                'code': 403,
            }, status=403)

        update_course.TeacherNo = new_teacher_no
        update_course.CourseNo = new_course_no
        update_course.CourseName = new_course_name
        update_course.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': CouSer(update_course).data
        }, status=200)

# 删除课程 √
class delete_course(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        course_id = request.GET.get('course_id')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        c = course.objects.get(pk=course_id)
        c.delete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': CouSer(c).data
        }, status=200)