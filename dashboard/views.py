import json

from django.shortcuts import render, redirect
from bota.models import *
# Create your views here.


def index(request):
    groups = Study_groups.objects.all()
    return render(request, 'index.html', {
        'groups': groups
    })


def students(request, pk):
    groups = Study_groups.objects.get(id=pk)
    students = Student.objects.filter(group=groups)
    asd = []
    for i in students:
        asd.append(
            {'obj': i, 'min': min([i.all_score_f_self, i.all_score_f_mom, i.all_score_f_dad])}
        )

    newlist = sorted(asd, key=lambda k: k['min'])
    print(newlist)
    finallist = []
    for i in newlist:
        finallist.append(i['obj'])
    return render(request, 'students.html', {
        'groups': groups,
        'students': finallist
    })

def all_students(request):
    students = Student.objects.all()
    asd = []
    for i in students:
        asd.append(
            {'obj': i, 'min': min([i.all_score_f_self, i.all_score_f_mom, i.all_score_f_dad])}
        )
    newlist = sorted(asd, key=lambda k: k['min'])
    print(newlist)
    finallist = []
    for i in newlist:
        finallist.append(i['obj'])
    return render(request, 'all_students_list.html', {
        'students': finallist
    })


def single_stu(request, pk):
    student = Student.objects.get(id=pk)
    answers = Scores.objects.filter(student=student).order_by('task_id')
    date_list = []
    mom_list = []
    dad_list = []
    self_list = []
    for i in answers:
        date_list.append(str(i.task.created_day.date()))
        self_list.append(i.score_fs)
        mom_list.append(i.score_fmom)
        dad_list.append(i.score_fdad)
    date_list = json.dumps(date_list)
    self_list = json.dumps(self_list)
    mom_list = json.dumps(mom_list)
    dad_list = json.dumps(dad_list)
    return render(request, 'single_page.html', {
        'student': student,
        'answers': answers,
        'date_list': date_list,
        'self_list': self_list,
        'mom_list': mom_list,
        'dad_list': dad_list
    })


def change_task(request, pk):
    groups = Study_groups.objects.get(id=pk)
    groups.dailyTask = request.POST['tasks']
    groups.save()
    return redirect('students', pk)


def task_list(request, pk):
    groups = Study_groups.objects.get(id=pk)
    students = Student.objects.filter(group=groups)
    tasks = Task.objects.filter(group=groups)
    answers = Scores.objects.filter(student__in=students).order_by('task_id')

    return render(request, 'tasks_list.html', {
        'groups': groups,
        'students': students,
        'tasks': tasks,
        'answers': answers
    })
