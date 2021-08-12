from django.contrib import admin
from .models import Telegaram_user, Group_me, Student, Task, Scores

# Register your models here.
admin.site.register(Telegaram_user)
admin.site.register(Group_me)
admin.site.register(Student)
admin.site.register(Task)
admin.site.register(Scores)