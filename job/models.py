from django.db import models


class token(models.Model):
    muser = models.OneToOneField('manager', on_delete=models.CASCADE, null=True)
    tuser = models.OneToOneField('teacher', on_delete=models.CASCADE, null=True)
    suser = models.OneToOneField('student', on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=64, verbose_name='token')


class manager(models.Model):
    ManagerNo=models.CharField(verbose_name='管理员编号', max_length=50)
    ManagerName=models.CharField(verbose_name='管理员姓名', max_length=10)
    MPassword=models.CharField(verbose_name='管理员密码', max_length=50)

    def __str__(self):
        return self.ManagerName


class teacher(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    TeacherNo=models.CharField(verbose_name='教师工号', max_length=50)
    TeacherName=models.CharField(verbose_name='教师姓名', max_length=50)
    TPassword=models.CharField(verbose_name='教师密码', max_length=50)
    TeacherGender=models.CharField(verbose_name='教师性别', choices=gender, max_length=50)

    def __str__(self):
        return self.TeacherName

    class Meta:
        ordering = ['-TeacherNo']
        verbose_name = '教师'
        verbose_name_plural = verbose_name


class student(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    StudentNo = models.CharField(verbose_name='学生学号', max_length=50)
    StudentName = models.CharField(verbose_name='学生姓名', max_length=50)
    SPassword = models.CharField(verbose_name='学生密码', max_length=50)
    StudentGender = models.CharField(verbose_name='学生性别', choices=gender, max_length=50)

    Course = models.ManyToManyField(
        'course',
        verbose_name='课程编号',
        related_name='course_students'
    )

    need_to_sign = models.ManyToManyField(
        'sign',
        related_name='sign_students',
        verbose_name='需要完成的签到',
        through = 'StudentSign',
        through_fields = ('student', 'sign'),
    )

    def __str__(self):
        return self.StudentName

    class Meta:
        ordering = ['-StudentNo']
        verbose_name = '学生'
        verbose_name_plural = verbose_name


class course(models.Model):
    CourseNo=models.CharField(verbose_name='课程编号', max_length=50)
    CourseName=models.CharField(verbose_name='课程名称', max_length=50)

    Teacher=models.ForeignKey(
        'teacher',
        verbose_name='教师编号',
        on_delete=models.CASCADE,
        related_name='teacher_courses'
    )

    Student=models.ManyToManyField(
        'student',
        verbose_name='学生学号',
        related_name='student_courses',
    )

    def __str__(self):
        return self.CourseName

    class Meta:
        ordering = ['-CourseNo']
        verbose_name = '课程'
        verbose_name_plural = verbose_name


class homework(models.Model):
    Title=models.CharField(verbose_name='作业标题', max_length=50)
    PubTime=models.DateTimeField(verbose_name='发布时间')
    EndTime=models.DateTimeField(verbose_name='结束时间')

    isExpired=models.BooleanField(verbose_name='是否过期', default=False)

    Course=models.ForeignKey(
        'course',
        verbose_name='课程编号',
        on_delete=models.CASCADE,
        related_name='course_homework'
    )

    def __str__(self):
        return self.Title

    class Meta:
        ordering = ['-PubTime']
        verbose_name = '作业'
        verbose_name_plural = verbose_name


class question(models.Model):
    QuesNo=models.CharField(verbose_name='题号', max_length=50)
    Type=models.CharField(verbose_name='题目类型', max_length=50)
    Content=models.CharField(verbose_name='题目内容', max_length=50)
    CorrectAnswer=models.CharField(verbose_name='正确答案', max_length=50)
    Score=models.CharField(verbose_name='该题分值', max_length=50, default='0')

    Homework=models.ForeignKey(
        'homework',
        verbose_name='作业编号',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.Content

    class Meta:
        ordering = ['-QuesNo']
        verbose_name = '题目'
        verbose_name_plural = verbose_name


class submission(models.Model):
    StudentNo=models.CharField(verbose_name='学生学号', max_length=50)
    SubTime=models.DateTimeField(verbose_name='提交时间', max_length=50)
    TotalGrade=models.FloatField(verbose_name='总成绩', default='0', null=True)

    isSubmitted=models.BooleanField(verbose_name='是否提交', default=False)

    Homework=models.ForeignKey(
        'homework',
        verbose_name='作业编号',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.StudentNo

    class Meta:
        ordering = ['-SubTime']
        verbose_name = '提交'
        verbose_name_plural = verbose_name


class answer(models.Model):
    QuesNo=models.CharField(verbose_name='题目编号', max_length=50)
    StudentAnswer=models.CharField(verbose_name='学生答案', max_length=50, blank=True, null=True)
    Grade=models.FloatField(verbose_name='该题得分', default='0')

    Submission=models.ForeignKey(
        'submission',
        verbose_name='提交编号',
        on_delete = models.CASCADE,
        related_name='submission'
    )

    def __str__(self):
        return self.QuesNo

    class Meta:
        ordering = ['-QuesNo']
        verbose_name = '学生答案'
        verbose_name_plural = verbose_name


class analysis(models.Model):
    AllCounts=models.IntegerField(verbose_name='需做作业人数')
    SubCounts=models.IntegerField(verbose_name='已提交数量')
    Average=models.FloatField(verbose_name='平均分')
    Full=models.FloatField(verbose_name='满分')
    Max=models.FloatField(verbose_name='最高分')
    Min=models.FloatField(verbose_name='最低分')

    Homework=models.ForeignKey(
        'homework',
        verbose_name='作业编号',
        on_delete=models.CASCADE,
    )


class sign(models.Model):
    Title = models.CharField(verbose_name='签到标题', max_length=50)
    PubTime = models.DateTimeField(verbose_name='发布时间')
    EndTime = models.DateTimeField(verbose_name='截止时间')

    Course = models.ForeignKey(
        'course',
        on_delete=models.CASCADE,
    )

    # sign_by = models.ManyToManyField(
    #     'student',
    #     related_name='student_signs',
    #     verbose_name='需要进行此次签到的学生'
    # )

    def __str__(self):
        return self.Title

    class Meta:
        ordering = ['-PubTime']
        verbose_name = '签到'
        verbose_name_plural = verbose_name


class StudentSign(models.Model):
    student = models.ForeignKey('student', on_delete=models.CASCADE, verbose_name='签到学生')
    sign = models.ForeignKey('sign', on_delete=models.CASCADE, verbose_name='签到')
    SignTime = models.DateTimeField(auto_now_add=True, verbose_name='签到时间')

    class Meta:
        ordering = ['-SignTime']

    def __str__(self):
        return self.student.StudentName


class notice(models.Model):
    Title=models.CharField(verbose_name='公告标题', max_length=50)
    Content = models.CharField(verbose_name='公告内容', max_length=5000)
    PubTime = models.DateTimeField(verbose_name='公告发布时间')

    def __str__(self):
        return self.Title

    class Meta:
        ordering = ['-PubTime']
        verbose_name = '公告'
        verbose_name_plural = verbose_name