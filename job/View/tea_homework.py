from job.models import course, question, homework, answer, submission, analysis
from job.serializers import HomeworkSer, StuAnswerSer, QuestionSer, SubmissionSer, AnalysisSer, CouSer
from rest_framework.views import APIView, Response
from django.db.models import Avg, Sum, Max, Min
from job.views import t_chk_token, chk_course_id, chk_submission_id, chk_homework_id
import json

# 教师get作业列表 √
class teacher_get_homework_list(APIView):
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
        # 获取作业列表
        homework_list = homework.objects.filter(Course=course_id)

        return Response({
            'info': 'success',
            'code': 200,
            'data': HomeworkSer(homework_list, many=True).data
        }, status=200)


# 教师发布作业
class publish_homework(APIView):
    def post(self, request):
        token = request.META.get('token')
        course_id = request.GET.get('course_id')

        title = request.POST.get('title')

        quesno = request.POST.get('quesno')
        type = request.POST.get('type')
        content = request.POST.get('content')
        correctans = request.POST.get('correctans')
        score = request.POST.get('score')
        #Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
        quesnums = request.POST.get('quesnums').strip() #获取题目数量

        pubtime = request.POST.get('pubtime')
        endtime = request.POST.get('endtime')

        # 1. 查token表 判断是哪个用户在操作
        # 2. 根据查表结果 判断是否合法
        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        # 查是哪门课的
        c = chk_course_id(course_id)
        if isinstance(c, Response):
            return c

        # 向作业表中添加记录
        create_homework = homework.objects.create(
            # HomNo=homno,
            Title=title,
            PubTime=pubtime,
            Endtime=endtime,
            # 这里可能要改
            CourseNo=c #与课程表关联起来
        )

        # 向question中批量添加记录
        if quesnums.isdigit() and int(quesnums) > 0:  #Python isdigit() 方法检测字符串是否只由数字组成。
            for i in range(int(quesnums)):
                create_question = question.objects.create(
                    QuesNo=quesno,
                    Type=type,
                    Content=content,
                    CorrectAnswer=correctans,
                    Score=score,
                    # 将题目和作业关联起来
                    HomeworkID=create_homework,
                )

            return Response({
                'info': 'success',
                'code': 200,
                'data': HomeworkSer(create_homework, create_question).data
            }, status=200)

        else:
            return Response({
                'info': '不完整',
                'code': 400
            }, status=400)


# 教师get作业详细内容 √
class teacher_get_homework_detail(APIView):
    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        homework_id=request.GET.get('homework_id')

        # 查token确认用户
        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id
        # 确认是哪门课
        h = chk_homework_id(homework_id)
        if isinstance(h, Response):
            return h

        # 获取作业详情
        homework_detail=question.objects.filter(Homework=homework_id).order_by('QuesNo')

        return Response({
            'info': 'success',
            'code': 200,
            'data': QuestionSer(homework_detail,many=True).data
        }, status=200)


# 教师get学生完成情况列表 √
class get_completed_list(APIView):
    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        homework_id=request.GET.get('homework_id')

        # 查token确认用户
        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id
        # 确认是哪门课
        h = chk_homework_id(homework_id)
        if isinstance(h, Response):
            return h

        # 获取学生完成情况列表
        student_homework_list = submission.objects.filter(Homework=homework_id).order_by('-id')

        return Response({
            'info': 'success',
            'code': 200,
            'data': SubmissionSer(student_homework_list, many=True).data
        }, status=200)


# 教师get学生已完成的作业 √
class get_completed_homework(APIView):
    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        submission_id=request.GET.get('submission_id')

        # 查token确认用户
        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id
        # 确认是哪门课
        s = chk_submission_id(submission_id)
        if isinstance(s, Response):
            return s

        # 获取提交内容详情
        answer_detail = answer.objects.filter(Submission=submission_id).order_by('QuesNo')

        return Response({
            'info': 'success',
            'code': 200,
            'data': StuAnswerSer(answer_detail, many=True).data
        }, status=200)


# 教师手动批改主观题
class manual_score(APIView):
    def post(self, request):
        token = request.META.get('token')
        submission_id = request.GET.get('submission_id')
        nums = request.POST.get('nums')
        quesno = request.POST.get('quesno')  # 要将分数和题号匹配起来，怎么做到
        grade = request.POST.get('grade')

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        s = chk_submission_id(submission_id)
        if isinstance(s, Response):
            return s

        if nums.isdigit() and int(nums) > 0:
            for i in range(int(nums)):
                # 将小题分数循环存入answer表
                update_grade = answer.objects.filter(SubmissionID=submission_id, QuesNo=i)
                update_grade.Grade = grade
                update_grade.save()

        return Response({
            'info': 'success',
            'code': 200,
            # 括号中的是不是要改一下
            'data': StuAnswerSer(update_grade).data
        }, status=200)


# 作业情况分析
class homework_analysis(APIView):
    def get(self, request):
        token=request.META.get('token')
        homework_id=request.GET.get('homework_id')

        # 查token确认用户
        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id
        # 确认是哪门课
        h = chk_homework_id(homework_id)
        if isinstance(h, Response):
            return h
        # 本次作业人数，平均分，满分，最高分，最低分，各分数人数分布，每道题目回答的正确率；
        ##### 本次作业需完成人数
        course_id=homework.obejcts.first(pk=homework_id).CourseNo
        all_counts=course.objects.filter(CourseNo=course_id).count()
        # 先提取出提交表中本次作业的所有提交记录
        all_submission=submission.objects.filter(HomeworkID=homework_id)
        ##### 本次作业提交人数
        # count作业id为homeworkid的提交记录数量
        submission_counts=all_submission.counts()
        ##### 平均分
        # 先提取出提交表中本次作业的所有提交记录，然后对TotalGrade求平均
        average=all_submission.aggregate(Avg('TotalGrade'))
        ##### 满分
        all_question=question.objects.filter(HomeworkID=homework_id)
        full=all_question.aggregate(Sum('Score'))
        ##### 最高分
        max=all_submission.aggregate(Max('TotalGrade'))
        ##### 最低分
        min=all_submission.aggregate(Min('TotalGrade'))

        create_analysis=analysis.objects.create(
            AllCounts=all_counts,
            SubCounts=submission_counts,
            Average=average,
            Full=full,
            Max=max,
            Min=min
        )

        return Response({
            'info': 'success',
            'code': 200,
            'data': AnalysisSer(create_analysis).data
        }, status=200)

        # nums=all_question.count()
        # ##### 每道题的正确率
        # # 正确率=满分数/总提交数
        # # 满分数=答案表中所有Grade==Score的记录
        # for i in range(int(nums)):
        #     question_score=question.objects.get(QuesNo=i).Score
        #     full_counts=answer.objects.filter(Grade=question_score).count()
        #     accuracy=full_counts/submission_counts


# 删除作业 √
class delete_homework(APIView):
    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        homework_id=request.GET.get('homework_id')

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        h = chk_homework_id(homework_id)
        if isinstance(h, Response):
            return h

        h.delete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': HomeworkSer(h).data
        }, status=200)