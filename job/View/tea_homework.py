from job.models import course, question, homework, answer, submission, analysis, student
from job.serializers import HomeworkSer, StuAnswerSer, QuestionSer, SubmissionSer, AnalysisSer, CouSer
from rest_framework.views import APIView, Response
from django.db.models import Avg, Sum, Max, Min
from job.views import t_chk_token, chk_course_id, chk_submission_id, chk_homework_id
import json
import django.utils.timezone as timezone

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


# 教师发布作业 √
class publish_homework(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        course_id = request.POST.get('course_id')
        title = request.POST.get('title')
        # pubtime = request.POST.get('pubtime')
        endtime = request.POST.get('endtime')

        json_list = request.POST.get('json_list')
        '''
        示例：
        [{"quesno":"1","type":"0","content":"这是第一道选择题的题目","correctans":"正确答案A","score":"该题分值"},
        {"quesno":"2","type":"0","content":"这是第二道填空题的题目","correctans":"正确答案","score":"该题分值"}]
        其中type：客观题为0，主观题为1
        '''

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        c = chk_course_id(course_id)
        if isinstance(c, Response):
            return c

        # 向作业表中添加记录
        create_homework = homework.objects.create(
            Title=title,
            PubTime=timezone.now(),
            EndTime=endtime,
            Course=c
        )

        list = json.loads(json_list)
        print(list)
        # 向question中批量添加记录
        for i in list:
            create_question = question.objects.create(
                QuesNo=i['quesno'],
                Type=i['type'],
                Content=i['content'],
                CorrectAnswer=i['correctans'],
                Score=i['score'],
                Homework=create_homework
            )

        return Response({
            'info': 'success',
            'code': 200,
            #这里只能返回question的最后一条记录
            'data': QuestionSer(create_question).data
        }, status=200)


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


# 教师get学生已完成的作业
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
        token = request.META.get('HTTP_TOKEN')
        submission_id = request.POST.get('submission_id')

        json_list = request.POST.get('json_list')
        '''
        示例：
        [
            {"quesno":"1","grade":"24"},
            {"quesno":"2","grade":"12"},
            ......
        ]
        '''

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        s = chk_submission_id(submission_id)
        if isinstance(s, Response):
            return s

        list = json.loads(json_list)
        print(list)
        # answer中批量添加记录
        for i in list:
            quesno = i['quesno']
            grade = i['grade']
            update_grade = answer.objects.get(Submission=submission_id, QuesNo=quesno)
            update_grade.Grade = grade
            update_grade.save()

        # 提交表记录
        student_submission = submission.objects.get(pk=submission_id)
        # 所有答案记录
        all_answers = answer.objects.filter(Submission=submission_id)
        total = all_answers.aggregate(Sum('Grade'))
        totalgrade = total['Grade__sum']
        student_submission.TotalGrade = totalgrade
        student_submission.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': StuAnswerSer(all_answers, many=True).data
        }, status=200)


# 作业情况分析
class homework_analysis(APIView):
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

        if len(analysis.objects.filter(Homework=homework_id)) > 0:
            pass

        else:
            # 本次作业人数，平均分，满分，最高分，最低分，各分数人数分布，每道题目回答的正确率；
            ##### 本次作业需完成人数
            course_id=homework.objects.get(pk=homework_id).Course
            students=student.objects.filter(Course=course_id)
            all_counts=students.count()

            # 先提取出提交表中本次作业的所有提交记录
            all_submission=submission.objects.filter(Homework=homework_id)
            ##### 本次作业提交人数
            # count作业id为homeworkid的提交记录数量
            submission_counts=all_submission.count()

            ##### 平均分
            # 先提取出提交表中本次作业的所有提交记录，然后对TotalGrade求平均
            ave=all_submission.aggregate(Avg('TotalGrade'))
            print(ave)
            average = ave['TotalGrade__avg']

            ##### 满分
            all_question=question.objects.filter(Homework=homework_id)
            f=all_question.aggregate(Sum('Score'))
            full = f['Score__sum']

            ##### 最高分
            ma=all_submission.aggregate(Max('TotalGrade'))
            max = ma['TotalGrade__max']

            ##### 最低分
            mi=all_submission.aggregate(Min('TotalGrade'))
            min = mi['TotalGrade__min']

            create_analysis=analysis.objects.create(
                AllCounts=all_counts,
                SubCounts=submission_counts,
                Average=average,
                Full=full,
                Max=max,
                Min=min,
                Homework=h
            )

        get_analysis = analysis.objects.get(Homework=homework_id)

        return Response({
            'info': 'success',
            'code': 200,
            'data': AnalysisSer(get_analysis).data
        }, status=200)


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