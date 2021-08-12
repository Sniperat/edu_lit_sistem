import datetime

from .models import Telegaram_user, Task, Scores


def user_func(update):
    try:
        user = Telegaram_user.objects.get(telegram_user_id=update.effective_user.id)
    except:
        user = Telegaram_user(telegram_user_id=update.effective_user.id, state=Telegaram_user.STATE_FULLNAME)
        user.save()
    return user


def task_func(user, pk):
    try:
        task = Task.objects.get(owner=user, id=pk)
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