# Generated by Django 3.1.4 on 2020-12-06 10:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('CuNo', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='课程编号')),
                ('CuName', models.CharField(max_length=50, verbose_name='课程名称')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
            },
        ),
        migrations.CreateModel(
            name='homework',
            fields=[
                ('HomNo', models.IntegerField(primary_key=True, serialize=False, verbose_name='作业编号')),
                ('Title', models.CharField(default='a', max_length=50, verbose_name='作业标题')),
                ('PubDate', models.DateField(default=django.utils.timezone.now, verbose_name='发布日期')),
                ('Cont', models.CharField(max_length=5000, verbose_name='作业内容')),
                ('CorAns', models.CharField(max_length=5000, verbose_name='作业标准答案')),
            ],
            options={
                'ordering': ['-PubDate'],
            },
        ),
        migrations.CreateModel(
            name='manager',
            fields=[
                ('MaNo', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='管理员编号')),
                ('MaName', models.CharField(max_length=50, verbose_name='管理员姓名')),
            ],
        ),
        migrations.CreateModel(
            name='sign',
            fields=[
                ('SignNo', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='签到编号')),
                ('StuNo', models.CharField(max_length=50, verbose_name='学生学号')),
                ('PubTime', models.DateTimeField(verbose_name='发布时间')),
                ('SubTime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='签到时间')),
                ('CuNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.course', verbose_name='课程编号')),
            ],
            options={
                'verbose_name': '签到',
                'verbose_name_plural': '签到',
            },
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('StuNo', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='学生学号')),
                ('StuName', models.CharField(max_length=50, verbose_name='学生姓名')),
                ('StuSex', models.CharField(choices=[('male', '男'), ('female', '女')], default='女', max_length=30, null=True, verbose_name='学生性别')),
                ('Major', models.CharField(max_length=50, null=True, verbose_name='学生专业名称')),
                ('CuNo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job.course', verbose_name='学生选修的课程编号')),
            ],
            options={
                'verbose_name': '学生',
                'verbose_name_plural': '学生',
                'ordering': ['-Major', 'StuNo'],
            },
        ),
        migrations.CreateModel(
            name='teacher',
            fields=[
                ('TeaNo', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='教师编号')),
                ('TeaName', models.CharField(max_length=50, verbose_name='教师姓名')),
                ('TeaSex', models.CharField(choices=[('male', '男'), ('female', '女')], default='女', max_length=30, null=True, verbose_name='教师性别')),
                ('CuNo', models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='job.course', verbose_name='课程编号')),
                ('SignNo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job.sign', verbose_name='签到编号')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
                'ordering': ['-TeaName'],
            },
        ),
        migrations.CreateModel(
            name='submission',
            fields=[
                ('SubNo', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='提交编号')),
                ('Ans', models.CharField(blank=True, max_length=50, null=True, verbose_name='学生答案')),
                ('Score', models.FloatField(verbose_name='作业成绩')),
                ('SubTime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='提交时间')),
                ('HomeNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.homework', verbose_name='作业编号')),
                ('StuNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.student', verbose_name='学号')),
            ],
        ),
        migrations.AddField(
            model_name='sign',
            name='TeaNo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.teacher', verbose_name='教师编号'),
        ),
        migrations.AddField(
            model_name='homework',
            name='TeaNo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.teacher', verbose_name='教师编号'),
        ),
        migrations.AddField(
            model_name='course',
            name='HomeNo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job.homework', verbose_name='作业编号'),
        ),
        migrations.AddField(
            model_name='course',
            name='TeaNo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job.teacher', verbose_name='教师编号'),
        ),
    ]