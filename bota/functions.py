import datetime

from .models import Telegaram_user, Task, Scores, Student
from .models import Telegram_guruxlar


def telegram_group_func(update):
    try:
        user = Telegram_guruxlar.objects.get(group_id=update.message.chat.id)
    except:
        user = Telegram_guruxlar(
            name=update.message.chat.title,
            group_id=update.message.chat.id
        )
        user.save()
    return user

def user_func(update):
    try:
        user = Telegaram_user.objects.get(telegram_user_id=update.effective_user.id)
    except:
        user = Telegaram_user(telegram_user_id=update.effective_user.id, state=Telegaram_user.STATE_FULLNAME)
        user.save()
    return user


def task_func(user, status):
    try:
        task = Task.objects.get(owner=user, state=status)
    except:
        task = Task(owner=user)
        task.save()
    return task


def score_func(student, task):
    try:
        asd = Scores.objects.get(student=student, task=task)
    except:
        asd = Scores(student=student, task=task)
        asd.save()
    return asd


def last_task_off(group):
    for t in Task.objects.filter(state=0, group=group):
        t.state = 1
        t.save()


def student_func(user):
    try:
        asd = Student.objects.get(self_telegram=user)
    except:
        asd = Student(self_telegram=user)
        asd.save()
    return asd