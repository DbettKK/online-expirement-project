from job.models import course
from job.serializers import CouSer
from rest_framework.views import APIView, Response
from job.views import m_chk_token


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


class add_course(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        course_no = request.POST.get('course_no')
        course_name = request.POST.get('course_name')
        teacher_no = request.POST.get('teacher_no')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        if len(course.objects.filter(CourseNo=teacher_no)) > 0:
            return Response({
                'info': '该记录已存在',
                'code': 403,
            }, status=403)

        else:
            create_course = course.objects.create(
                CourseNo=course_no,
                CourseName=course_name,
                TeacherNo=teacher_no
            )

            return Response({
                'info': 'success',
                'code': 200,
                'data': CouSer(create_course).data
            }, status=200)


class modify_course(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        course_id = request.GET.get('course_id')
        new_course_no = request.POST.get('new_course_no')
        new_course_name = request.POST.get('new_course_name')
        new_teacher_no= request.POST.get('new_teacher_no')

        ma_id = m_chk_token(token)
        if isinstance(ma_id, Response):
            return ma_id

        update_course = course.objects.get(pk=course_id)
        update_course.CourseNo = new_course_no
        update_course.CourseName = new_course_name
        update_course.TeacherNo = new_teacher_no
        update_course.save()

        all_course = course.objects.all()

        return Response({
            'info': 'success',
            'code': 200,
            'data': CouSer(all_course).data
        }, status=200)


class delete_coruse(APIView):
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