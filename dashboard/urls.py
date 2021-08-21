from django.urls import path, include
from .views import index, students, single_stu, change_task, task_list

urlpatterns = [
    path('', index, name='index'),
    path('students/<int:pk>/', students, name='students'),
    path('tasks/<int:pk>/', task_list, name='task_list'),
    path('single/<int:pk>/', single_stu, name='single_stu'),
    path('change/<int:pk>/', change_task, name='change')
]
