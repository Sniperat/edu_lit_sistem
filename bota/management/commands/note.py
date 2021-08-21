from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from ._base import BotBase
import datetime
from bota.models import Study_groups, Student, Task, Scores


class Command(BotBase):
    def handle(self, *args, **options):
        main_hour = datetime.datetime.now().time().hour
        main_minut = datetime.datetime.now().time().minute
        print('mass')

        for i in Study_groups.objects.all():
            students = Student.objects.filter(group=i)
            ansverst_to_group = '{}\nStudent name   self, father, mother'.format(i.name)
            for stu in students:
                try:
                    scores = Scores.objects.get(task__state=0, student=stu)
                    ansverst_to_group += '\n{} - {}, {}, {}'.format(stu.firstName+" "+stu.lastName, scores.score_fs,
                                                                    scores.score_fdad, scores.score_fmom)
                except:
                    pass
            self.updater.bot.send_message(chat_id=i.telegram_group.group_id, text=ansverst_to_group)
            taskb = Task.objects.filter(state=0)
            for tas in taskb:
                tas.state = 1
                tas.save()
            if i.dailyTask != '':
                counts = i.dailyTask.split("\r\n")

                task = Task(
                    group=i,
                    tasks=i.dailyTask,
                    count=len(counts)
                )
                task.save()
                stud = Student.objects.filter(group=i)

                contentTasks = []
                for s in stud:
                    keyboard = [['comment']]
                    reply_markup = ReplyKeyboardMarkup(keyboard)
                    try:
                        self.updater.bot.send_message(chat_id=s.self_telegram.telegram_user_id,
                                                  text=str(datetime.datetime.now())[:16],
                                                  reply_markup=reply_markup)
                        self.updater.bot.send_message(chat_id= s.mom_telegram.telegram_user_id,
                                                  text=str(datetime.datetime.now())[:16],
                                                  reply_markup=reply_markup)
                        self.updater.bot.send_message(chat_id= s.dad_telegram.telegram_user_id,
                                                  text=str(datetime.datetime.now())[:16],
                                                  reply_markup=reply_markup)
                    except:
                        pass
                    for val in counts:
                        contentTasks.append([
                            InlineKeyboardButton("Bajarildi", callback_data=f'{task.id}-1'),
                            InlineKeyboardButton("Bajarilmadi", callback_data=f'{task.id}-0')
                        ])
                        reply_markup = InlineKeyboardMarkup(contentTasks)
                        try:

                            self.updater.bot.send_message(chat_id=s.self_telegram.telegram_user_id, text=val,
                                                          reply_markup=reply_markup)
                        except:
                            pass
                        try:
                            self.updater.bot.send_message(chat_id=s.mom_telegram.telegram_user_id, text=val,
                                                          reply_markup=reply_markup)
                        except:
                            pass
                        try:
                            self.updater.bot.send_message(chat_id=s.dad_telegram.telegram_user_id, text=val,
                                                          reply_markup=reply_markup)
                        except:
                            pass
                        contentTasks = []

        # if datetime.timedelta(hours=main_hour, minutes=main_minut) == (datetime.timedelta(hours=3, minutes=25)):
        #     print('passs')
