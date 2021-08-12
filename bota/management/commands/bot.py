from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Location, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, RegexHandler, \
    MessageHandler
import requests, calendar
import datetime

from django.conf import settings
from ._base import BotBase
from bota.functions import user_func, task_func, score_func
from bota.models import Group_me, Telegaram_user, Task, Scores, Student


from django.core.validators import EmailValidator

import random


class Command(BotBase):

    def language(self, update: Update, context: CallbackContext) -> None:
        # keyboard = [
        #     [
        #         InlineKeyboardButton("O'zbekcha", callback_data='asd1')
        #     ],
        #     [
        #         InlineKeyboardButton('Русский', callback_data='asd2')
        #     ],
        #     [
        #         InlineKeyboardButton('English', callback_data='asd3')
        #     ]
        # ]
        # reply_markup = InlineKeyboardMarkup(keyboard)
        user = user_func(update)
        update.message.reply_text("To'liq ismingizni kiriting.")

    def message_handler(self, update: Update, context: CallbackContext) -> None:
        user = user_func(update)
        msg = str(update.message.text)
        text = ''
        if user.state == 0:
            user.fullName = msg
            user.state = 1
            text = 'telefon raqamingizni kiriting'
            update.message.reply_text(text)
        elif user.state == 1:
            user.phone = msg
            user.state = 7
            user.save()
            text = "bo'ldi"
            update.message.reply_text(text)
        elif user.is_staff:
            groups = user.groups.all()
            if msg == 'topshiriq yuborish':
                keyboard = []
                user.state = None
                user.save()
                for i in groups:
                    keyboard.append([i.name])

                reply_markup = ReplyKeyboardMarkup(keyboard)
                update.message.reply_text(text="tanlang", reply_markup=reply_markup)
            else:
                try:
                    msg_group = Group_me.objects.get(name=msg)
                except:
                    msg_group = None

                task = task_func(user, user.state)
                if msg_group in groups:
                    task.group = msg_group
                    task.save()
                    user.state = task.id
                    update.message.reply_text(text="Savollarni yozing")
                elif task.state == 0:
                    task.tasks = msg
                    counts = msg.split("\n")
                    print(counts)
                    task.count = len(counts)
                    # user.state = None
                    user.save()
                    task.save()
                    parents = Telegaram_user.objects.all()
                    for ase in parents:
                        # print(ase.groups.all().first())
                        if ase.groups.all().first() == task.group:
                            contentTasks = []
                            self.updater.bot.send_message(chat_id=ase.telegram_user_id, text=str(datetime.datetime.now())[:16])
                            for val in counts:
                                contentTasks.append([
                                        InlineKeyboardButton("Bajarildi", callback_data='1'),
                                        InlineKeyboardButton("Bajarilmadi", callback_data='0')
                                    ])
                                reply_markup = InlineKeyboardMarkup(contentTasks)
                                # update.bot.send_message()
                                # if ase.is_staff:
                                #     pass
                                # else:
                                self.updater.bot.send_message(chat_id=ase.telegram_user_id, text=str(val),
                                                              reply_markup=reply_markup)
                                contentTasks = []






            keyboard = [['topshiriq yuborish']]
            for i in groups:
                keyboard.append([i.name])

            reply_markup = ReplyKeyboardMarkup(keyboard)
            update.message.reply_text(text="tanlang", reply_markup=reply_markup)
            # update.message.reply_text('salom')
        user.save()



    def delete(self, update: Update, context: CallbackContext) -> None:
        user = user_func(update)
        query = update.callback_query
        query.answer()
        student = None
        role = 0
        if user.role.name == "Student":
            student = Student.objects.get(self_telegram=user)
            role = 1
        if user.role.name == "Father":
            student = Student.objects.get(dad_telegram=user)
            role = 2
        if user.role.name == "Mother":
            student = Student.objects.get(mom_telegram=user)
            role = 3

        thisgroup = student.group
        comentator = Telegaram_user.objects.filter(is_staff=1)
        teacher = None
        for com in comentator:
            if thisgroup in com.groups.all():
                teacher = com
        task = task_func(teacher, teacher.state)
        score = score_func(student, task)
            # Task.objects.get(id=student.group, id=user)
        # score.ta = task.count
        if role == 1:
            score.answers_fs = score.answers_fs+1
        if role == 2:
            score.answers_fdad = score.answers_fdad+1
        if role == 3:
            score.answers_fmom = score.answers_fmom+1

        score.score = score.score+int(query.data)
        score.save()
        msg = query.message.text

        if query.data == '1':
            query.edit_message_text(text=msg +"  ✅")
        elif query.data == '0':
            query.edit_message_text(text=msg +"  ❌")



    def handle(self, *args, **kwargs):
        dispatcher = self.updater.dispatcher

        # dispatcher.add_handler(CallbackQueryHandler(self.days2, pattern="^(\d{4}\-\d{2}\-\d{2})$"))

        # dispatcher.add_handler(CallbackQueryHandler(self.main_me, pattern="^(main)$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.about, pattern="^(about)$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.course, pattern="^(course)$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.course1, pattern="^(course1)$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.money, pattern="^(money)$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.testing, pattern="^(testing)$"))
        dispatcher.add_handler(CallbackQueryHandler(self.delete, pattern="^(\d{1})$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.free, pattern="^(free)$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.free_edu, pattern="^(free_edu)$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.location, pattern="^(location)$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.start, pattern="^(asd\d{1})$"))
        dispatcher.add_handler(CommandHandler('start', self.language))
        # dispatcher.add_handler(CallbackQueryHandler(self.button))

        dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, self.message_handler))

        self.updater.start_polling()
        self.updater.idle()
