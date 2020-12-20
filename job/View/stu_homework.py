from job.models import question, homework, submission, student, answer
from job.serializers import HomeworkSer, QuestionSer, StuAnswerSer, SubmissionSer
from rest_framework.views import APIView, Response
from job.views import s_chk_token, chk_course_id, chk_homework_id, chk_submission_id
from django.db.models import Sum
import django.utils.timezone as timezone
import json

# 学生get作业列表 √
class student_get_homework(APIView):
    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        course_id=request.GET.get('course_id')
# 查token确认用户
        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id
        stuno = student.objects.get(pk=stu_id).StudentNo

# 确认是哪门课
        c = chk_course_id(course_id)
        if isinstance(c, Response):
            return c

# 获取作业列表
        time_now=timezone.now()
        # 过期作业,截止时间小于等于现在
        expired_homework = homework.objects.filter(Course=course_id, EndTime__lte=time_now)
        # 未过期作业，截止时间大于现在
        unexpired_homework = homework.objects.filter(Course=course_id, EndTime__gt=time_now)
# 将作业时间状态存入数据库，默认为未过期，所以只用更新已过期的作业记录
        expired_homework.update(isExpired = True)
        # expired_homework.save()

        all_homework = homework.objects.filter(Course=course_id)

        return Response({
            'info': 'success',
            'code': 200,
            'data': HomeworkSer(all_homework, many=True).data,
        }, status=200)


# 学生get作业详情 √
class student_get_homework_detail(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        homework_id = request.GET.get('homework_id')
# 查token确认用户
        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id
# 确认作业chk_homework
        h = chk_homework_id(homework_id)
        if isinstance(h, Response):
            return h
# 获取题目列表
        questions = question.objects.filter(Homework=homework_id).order_by('QuesNo')

        return Response({
            'info': 'success',
            'code': 200,
            'data': QuestionSer(questions, many=True).data
        }, status=200)


# 学生提交作业+自动批改作业
class handin_homework(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        homework_id = request.POST.get('homework_id')
        subtime = request.POST.get('subtime')

        json_list = request.POST.get('json_list')
        '''
        示例：
        [
            {"quesno":"1","stuans":"我不会做"},
            {"quesno":"2","stuans":"略略略"},
            ......
        ]
        '''

        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id

        h = chk_homework_id(homework_id)
        if isinstance(h, Response):
            return h

# 根据token获取学生学号
        stuno = student.objects.get(pk=stu_id).StudentNo

        if len(submission.objects.get(Homework=homework_id, StudentNo=stuno)) > 0:  #已提交
            # 查看作业表和答案表
            return Response({
                'info': '已经完成过作业，跳转到查看已完成作业、答案和分数的页面',
                'code': 403,
            }, status=403)

        else:
# 处理是否过期的需求
            check_isExpired = homework.objects.get(pk=homework_id).isExpired
            print(check_isExpired)
        # 已过期
            if check_isExpired==True:
                return Response({
                    'info': '该作业已过期，不可提交',
                    'code': 400,
                }, status=400)

            else:
                list = json.loads(json_list)
                print(list)

                create_submission = submission.objects.create(
                    StudentNo=stuno,
                    SubTime=subtime,
                    isSubmitted=True,
                    Homework=h
                )

                # 向answer中批量添加记录
                for i in list:
                    quesno=i['quesno']
                    create_answer = question.objects.create(
                        QuesNo=quesno,
                        Type=i['stuans'],
                        Submission=create_submission
                    )

                ############# 这里放自动批改的方法
                # 通过作业id查提交id
                sub_id = submission.objects.get(Homework=homework_id, StudentNo=stuno).pk
                # 取出学生所有答案的记录
                all_answers = answer.objects.filter(Submission=sub_id)

                # 取题目表中所有题的记录
                all_questions = question.objects.filter(Homework=homework_id)
                # # 取所有题个数
                # all_counts = all_questions.count()
                # # 取该次作业所有题的类型type
                # all_type = all_questions.Type

                # 循环计分
                for i in all_questions:
                    # 如果不是客观题就跳出当前循环
                    if i.Type != '0':
                        continue
                    # 分别取出标准答案和学生答案
                    correct_answer = all_questions[i-1].CorrectAnswer
                    student_answer = all_answers[i-1].StudentAnswer
                    # 取出学生那道题的记录
                    certain_answer = all_answers[i-1]
                    # 取出那道题的分值
                    score = all_questions[i-1].Score
                    # 比较学生答案和标准答案并给分
                    if student_answer == correct_answer:
                        certain_answer.Grade = score
                        certain_answer.save()
                    else:
                        certain_answer.Grade = float('0')
                        certain_answer.save()

                # 提交表记录
                student_submission = submission.objects.get(pk=sub_id)
                # 所有答案记录
                all_answers = answer.objects.filter(Submission=sub_id)
                totalgrade = all_answers.aggregate(Sum('Grade'))
                student_submission.update(TotalGrade = totalgrade)
                # student_submission.save()

                return Response({
                    'info': 'success',
                    'code': 200,
                    'data': StuAnswerSer(all_answers, many=True).data
                }, status=200)

            # else:
            #     return Response({
            #         'info': '未填写答案',
            #         'code': 400
            #     }, status=400)


# 学生get分数
class student_get_grade(APIView):

    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        submission_id=request.GET.get('sub_id')

        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id
        # 查提交id
        s = chk_submission_id(submission_id)
        if isinstance(s, Response):
            return s

        # 查看已提交答案，小分，总分
        answers = answer.objects.filter(Submission=submission_id)

        return Response({
            'info': 'success',
            'code': 200,
            'data': StuAnswerSer(answers)
        }, status=200)