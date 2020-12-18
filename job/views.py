import hashlib
from job.models import course, homework, submission, token, sign
from rest_framework.views import APIView, Response
import time


def md5(user):
    """md5 加密token"""
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

def t_chk_token(token_str):
    if token_str is None:
        return Response({
            'info': '用户未登录',
            'code': 403
        }, status=403)
    t = token.objects.filter(token=token_str)
    if len(t) <= 0:
        # token无效
        return Response({
            'info': '无效用户',
            'code': 403
        }, status=403)
    return t.get().tuser_id

def s_chk_token(token_str):
    if token_str is None:
        return Response({
            'info': '用户未登录',
            'code': 403
        }, status=403)
    t = token.objects.filter(token=token_str)
    if len(t) <= 0:
        # token无效
        return Response({
            'info': '无效用户',
            'code': 403
        }, status=403)
    return t.get().suser_id

def m_chk_token(token_str):
    if token_str is None:
        return Response({
            'info': '用户未登录',
            'code': 403
        }, status=403)
    t = token.objects.filter(token=token_str)
    if len(t) <= 0:
        # token无效
        return Response({
            'info': '无效用户',
            'code': 403
        }, status=403)
    return t.get().muser_id


def chk_course_id(course_id):
    try:
        c = course.objects.get(pk=course_id)
    except:
        return Response({
            'info': '该课程不存在',
            'code': 403,
        }, status=403)
    return c

def chk_homework_id(homework_id):
    try:
        h = homework.objects.get(pk=homework_id)
    except:
        return Response({
            'info': '该作业不存在',
            'code': 403,
        }, status=403)
    return h

def chk_submission_id(submission_id):
    try:
        s = submission.objects.get(pk=submission_id)
    except:
        return Response({
            'info': '该提交不存在',
            'code': 403,
        }, status=403)
    return s

def chk_sign_id(sign_id):
    try:
        s = sign.objects.get(pk=sign_id)
    except:
        return Response({
            'info': '该签到不存在',
            'code': 403,
        }, status=403)
    return s

from .View.login import login
from .View.stu_homepage import student_course
from .View.tea_homepage import teacher_course


