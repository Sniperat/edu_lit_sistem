from django.urls import path, include
from .views import index, students, single_stu

urlpatterns = [
    path('', index, name='index'),
    path('students/<int:pk>/', students, name='students'),
    path('single/<int:pk>/', single_stu, name='single_stu')
]
