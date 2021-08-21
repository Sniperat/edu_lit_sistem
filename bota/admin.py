from django.contrib import admin
from .models import Telegaram_user, Study_groups, Student, Task, Scores
from .models import Telegram_guruxlar

# Register your models here.
admin.site.register(Telegaram_user)
admin.site.register(Study_groups)
admin.site.register(Student)
admin.site.register(Task)
admin.site.register(Scores)
admin.site.register(Telegram_guruxlar)

