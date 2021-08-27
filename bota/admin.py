from django.contrib import admin
from .models import Telegaram_user, Study_groups, Student, Task, Scores
from .models import Telegram_guruxlar


class StundentAdmin(admin.ModelAdmin):
    search_fields = ['firstName', 'lastName','secondName']

    def get_ordering(self, request):
        return ['firstName']



admin.site.register(Telegaram_user)
admin.site.register(Study_groups)
admin.site.register(Student, StundentAdmin)
admin.site.register(Task)
admin.site.register(Scores)
admin.site.register(Telegram_guruxlar)

