from django.contrib import admin
from django.urls import path, include
from .views import event

urlpatterns = [
    path('', event),
]
