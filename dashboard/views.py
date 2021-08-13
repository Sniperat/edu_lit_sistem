from django.shortcuts import render
from bota.models import *

# Create your views here.


def index(request):
    groups = Group_me.objects.all()
    return render(request, 'index.html', {
        'groups': groups
    })


def students(request, pk):
    groups = Group_me.objects.get(id=pk)
    students = Student.objects.filter(group=groups)
    print(students)
    return render(request, 'students.html', {
        'groups': groups,
        'students': students
    })


def single_stu(request, pk):
    print('manashu joti ishladi')
    student = Student.objects.get(id=pk)
    print('buyam ishladi')
    print(student)
    return render(request, 'single_page.html', {
        'student': student
    })