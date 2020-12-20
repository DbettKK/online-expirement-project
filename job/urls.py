from django.urls import path

from . import views

app_name = 'job'


urlpatterns=[

    # 不需要token的api
    path('login/', views.login.as_view(), name='login'), #

    # 需要token的api

    # 管理员
    path('manager/homepage/password/', views.manager_modify_password.as_view()), #

    path('manager/teacher/', views.get_teacher_list.as_view()), #
    path('manager/teacher/add/', views.add_teacher.as_view()), #
    path('manager/teacher/modify/', views.modify_teacher.as_view()), #
    path('manager/teacher/delete/', views.delete_teacher.as_view()), #

    path('manager/student/', views.get_student_list.as_view()), #
    path('manager/student/add/', views.add_student.as_view()), #
    path('manager/student/modify/', views.modify_student.as_view()), #
    path('manager/student/delete/', views.delete_student.as_view()), #

    path('manager/notice/', views.get_notice_list.as_view()), #
    path('manager/notice/add/', views.add_notice.as_view()), #
    path('manager/notice/delete/', views.delete_notice.as_view()), #

    path('manager/course/', views.get_course_list.as_view()), #
    path('manager/course/add/', views.add_course.as_view()), #
    path('manager/course/modify/', views.modify_course.as_view()), #
    path('manager/course/delete/', views.delete_course.as_view()), #


    # 教师
    path('teacher/course/', views.teacher_course.as_view()), #
    path('teacher/password/', views.teacher_modify_password.as_view()), #
    path('teacher/notice/', views.teacher_get_notice.as_view()), #

    path('teacher/homework/', views.teacher_get_homework_list.as_view()),#
    path('teacher/homework/add/', views.publish_homework.as_view()),#
    path('teacher/homework/check/', views.teacher_get_homework_detail.as_view()),#
    path('teacher/homework/list/', views.get_completed_list.as_view()),#
    path('teacher/homework/completed/', views.get_completed_homework.as_view()),
    path('teacher/homework/score/', views.manual_score.as_view()),
    path('teacher/homework/analysis/', views.homework_analysis.as_view()),
    path('teacher/homework/delete/', views.delete_homework.as_view()),

    path('teacher/sign/', views.teacher_get_sign_list.as_view()), #
    path('teacher/sign/add/', views.publish_sign.as_view()), #
    path('teacher/sign/detail/', views.sign_detail.as_view()), #
    path('teacher/sign/delete/', views.delete_sign.as_view()), #


    # 学生
    path('student/course/', views.student_course.as_view()), #
    path('student/password/', views.student_modify_password.as_view()), #
    path('student/notice/', views.student_get_notice.as_view()), #

    path('student/homework/', views.student_get_homework.as_view()), #
    path('student/homework/detail/', views.student_get_homework_detail.as_view()),#
    path('student/homework/add/', views.handin_homework.as_view()),
    path('student/homework/grade/', views.student_get_grade.as_view()),

    path('student/sign/', views.student_get_sign.as_view()), #
    path('student/sign/add/', views.student_sign.as_view()), #

]


