from job.models import question, homework, submission, student, answer
from job.serializers import HomeworkSer, QuestionSer, StuAnswerSer
from rest_framework.views import APIView, Response
from job.views import s_chk_token, chk_course_id, chk_homework_id, chk_submission_id
from django.db.models import Sum
import django.utils.timezone as timezone
import json

# 学生get作业列表 ×未修改
class student_get_homework(APIView):
    def get(self, request):
        token=request.META.get('HTTP_TOKEN')
        course_id=request.GET.get('course_id')
# 查token确认用户
        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id
# 确认是哪门课
        c = chk_course_id(course_id)
        if isinstance(c, Response):
            return c

# 获取作业列表
        time_now=timezone.now()
        # 过期作业,截止时间小于等于现在
        expired_homework = homework.objects.filter(Course=course_id)#, EndTime__lte=time_now
        # 未过期作业，截止时间大于现在
        # unexpired_homework = homework.objects.filter(Course=course_id, EndTime__gt=time_now)
# 将作业时间状态存入数据库，默认为未过期，所以只用更新已过期的作业记录
#         expired_homework.isExpired = True
#         expired_homework.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': HomeworkSer(expired_homework, many=True).data
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


# 学生提交作业+自动批改作业 ×未修改
class handin_homework(APIView):
    def post(self, request):
        token = request.META.get('token')
        homework_id = request.POST.get('homework_id')
        quesno = request.POST.get('quesno')
        stuans= request.POST.get('stuans')
        subtime = request.POST.get('subtime')
        ansnums = request.POST.get('ansnums').strip() #获取题目数量
# 查token
        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id
# 查作业id
        h = chk_homework_id(homework_id)
        if isinstance(h, Response):
            return h
# 根据token获取学生学号
        stuno = student.objects.get(pk=stu_id).suser

# 处理是否过期的需求
        check_time = homework.objects.get(pk=homework_id).isExpired
        print(check_time)
        # 已过期
        if check_time==True:
            return Response({
                'info': '该作业已过期',
                'code': 400,
            }, status=400)

        else:
            if ansnums.isdigit() and int(ansnums) > 0:
                # 存提交表，存入字段为学生学号、提交时间，并将其与作业表关联起来
                create_submission = submission.objects.create(
                    StudentNo=stuno,
                    SubTime=subtime,
                    # 这里的h如果不是一条记录得改，得和作业编号为homework_id的那条记录关联
                    HomeworkId=h
                )
                # 存学生答案表，存入字段为学生每题编号、每题答案，并将其与提交表关联起来
                for i in range(int(ansnums)):
                    create_answer = answer.objects.create(
                        QuesNo=quesno,
                        StudentAnswer=stuans,
                        SubmissionID=create_submission
                    )

                ############# 这里放自动批改的方法
                # 通过作业id查提交id
                sub_id = submission.objects.get(HomeworkID=homework_id, StudentNo=stuno).pk
                # 取出学生所有答案的记录
                all_answers = answer.objects.filter(SubmissionID=sub_id)

                # 取题目表中所有题的记录
                all_questions = question.objects.filter(HomeworkID=homework_id)
                # 取所有题个数
                all_counts = all_questions.count()
                # 取该次作业所有题的类型type
                all_type = all_questions.Type

                # 循环计分
                for i in range(int(all_counts)):
                    # 如果不是客观题就跳出当前循环
                    if all_type != 'objective':
                        continue
                    # 分别取出标准答案和学生答案
                    correct_answer = all_questions.objects.get(QuesNo=i).CorrectAnswer
                    student_answer = all_answers.objects.get(QuesNo=i).StudentAnswer
                    # 取出学生那道题的记录
                    certain_answer = all_answers.objects.get(QuesNo=i)
                    # 取出那道题的分值
                    score = all_questions.objects.get(QuesNo=i).Score
                    # 比较学生答案和标准答案并给分
                    if student_answer == correct_answer:
                        certain_answer.Grade = score
                        certain_answer.save()
                    else:
                        certain_answer.Grade = int('0')
                        certain_answer.save()

                # 将提交表中的是否提交字段修改为已提交
                create_submission.isSubmitted=True
                create_submission.save()

                return Response({
                    'info': 'success',
                    'code': 200,
                    'data': StuAnswerSer(create_submission, create_answer)
                }, status=200)

            else:
                return Response({
                    'info': '未填写答案',
                    'code': 400
                }, status=400)


# 学生get分数 ×未修改
class student_get_grade(APIView):
    # 若并未所有题都已得到分数，则不显示
    def get(self, request):
        token=request.META.get('token')
        submission_id=request.GET.get('sub_id')

        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id
        # 查提交id
        h = chk_submission_id(submission_id)
        if isinstance(h, Response):
            return h

        # 提交表记录
        student_submission=submission.objects.get(pk=submission_id)
        # 所有答案记录
        all_answers= answer.objects.filter(SubmissionID=submission_id)
        totalgrade=all_answers.aggregate(Sum('Grade'))
        student_submission.TotalGrade=totalgrade
        student_submission.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': StuAnswerSer(student_submission,all_answers)
        }, status=200)