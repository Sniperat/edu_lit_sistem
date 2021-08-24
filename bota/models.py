from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import Group

Group.add_to_class('description', models.CharField(max_length=255, null=True, blank=True))


class Telegaram_user(models.Model):
    STATE_FULLNAME = 0
    STATE_PHONE = 1
    STATE_PHOTO = 2

    telegram_user_id = models.CharField(max_length=100, primary_key=True)
    firstName = models.CharField(max_length=100, null=True)
    lastName = models.CharField(max_length=100, null=True)
    secondName = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, default=None, null=True)
    photo = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    state = models.IntegerField(default=STATE_FULLNAME, null=True)
    role = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    role_name = models.CharField(max_length=255, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.firstName) + " " + str(self.lastName) + " " + str(self.secondName)


class Study_groups(models.Model):
    name = models.CharField(max_length=255, null=True)
    yosh = models.CharField(max_length=255, null=True)
    kunlar = models.CharField(max_length=255, null=True)
    soat = models.CharField(max_length=255, null=True)
    dailyTask = models.TextField(null=True, blank=True)
    telegram_group = models.ForeignKey('Telegram_guruxlar', on_delete=models.CASCADE, null=True, blank=True)
    mertor = models.ForeignKey(Telegaram_user, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    firstName = models.CharField(max_length=100, null=True)
    lastName = models.CharField(max_length=100, null=True)
    secondName = models.CharField(max_length=100, null=True)
    group = models.ForeignKey(Study_groups, on_delete=models.RESTRICT, null=True, blank=True)
    address = models.CharField(max_length=255, null=True)
    self_telegram = models.ForeignKey(Telegaram_user, on_delete=models.RESTRICT, null=True,
                                      blank=True,
                                      related_name='studentTelegram')
    mom_telegram = models.ForeignKey(Telegaram_user, on_delete=models.RESTRICT, null=True,
                                     blank=True,
                                     related_name='motherTelegram')
    dad_telegram = models.ForeignKey(Telegaram_user, on_delete=models.RESTRICT, null=True,
                                     blank=True,
                                     related_name='fatherTelegram')

    def __str__(self):
        return self.firstName + " " + self.lastName


class Task(models.Model):
    created_day = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Study_groups, on_delete=models.RESTRICT, null=True)
    tasks = models.TextField(null=True)
    count = models.CharField(max_length=10, null=True)
    state = models.IntegerField(default=0)

    def __str__(self):
        return str(self.created_day)


class Scores(models.Model):
    score_day = models.DateField(auto_now=True)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    task = models.ForeignKey(Task, on_delete=models.RESTRICT, null=True)
    answers_fmom = models.IntegerField(default=0)
    answers_fdad = models.IntegerField(default=0)
    answers_fs = models.IntegerField(default=0)
    score_fs = models.IntegerField(default=0)
    score_fdad = models.IntegerField(default=0)
    score_fmom = models.IntegerField(default=0)

    def __str__(self):
        return self.student.firstName + " " + self.student.lastName + " " + self.task.group.name


class Telegram_guruxlar(models.Model):
    name = models.CharField(max_length=255)
    group_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name
