from django.contrib.auth.models import Group
from django.db import models


# Create your models here.


class Telegaram_user(models.Model):
    STATE_FULLNAME = 0
    STATE_PHONE = 1

    telegram_user_id = models.CharField(max_length=100, primary_key=True)
    fullName = models.CharField(max_length=50, default=None, null=True)
    phone = models.CharField(max_length=15, default=None, null=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField('Group_me')
    state = models.IntegerField(default=STATE_FULLNAME, null=True)
    role = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.fullName


class Group_me(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    secondName = models.CharField(max_length=100, null=True)
    group = models.ForeignKey(Group_me, on_delete=models.RESTRICT)
    self_telegram = models.ForeignKey(Telegaram_user, on_delete=models.RESTRICT, null=True,
                                      related_name='studentTelegram')
    mom_telegram = models.ForeignKey(Telegaram_user, on_delete=models.RESTRICT, null=True,
                                     related_name='motherTelegram')
    dad_telegram = models.ForeignKey(Telegaram_user, on_delete=models.RESTRICT, null=True,
                                     related_name='fatherTelegram')

    def __str__(self):
        return self.firstName + " " + self.lastName + " " + self.secondName + "  " + self.group.name


class Task(models.Model):
    owner = models.ForeignKey(Telegaram_user, on_delete=models.RESTRICT)
    created_day = models.DateField(auto_now=True)
    group = models.ForeignKey(Group_me, on_delete=models.RESTRICT, null=True)
    tasks = models.TextField(null=True)
    count = models.CharField(max_length=10, null=True)
    state = models.IntegerField(default=0)

    def __str__(self):
        return str(self.owner.fullName) + " " + str(self.created_day)


class Scores(models.Model):
    score_day = models.DateField(auto_now=True)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    task = models.ForeignKey(Task, on_delete=models.RESTRICT, null=True)
    answers_fmom = models.IntegerField(default=0)
    answers_fdad = models.IntegerField(default=0)
    answers_fs = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.student.firstName + " " + self.student.lastName + " " + self.task.group.name
