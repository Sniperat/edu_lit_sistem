from django.core.files.images import ImageFile
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Location, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, RegexHandler, \
    MessageHandler
import requests, calendar
import datetime

from django.conf import settings
from ._base import BotBase
from bota.functions import user_func, task_func, score_func, last_task_off
from bota.models import Group_me, Telegaram_user, Task, Scores, Student

from django.core.validators import EmailValidator

import random


class Command(BotBase):

    def language(self, update: Update, context: CallbackContext) -> None:
        user = user_func(update)
        update.message.reply_text("To'liq ismingizni kiriting.")

    def message_handler(self, update: Update, context: CallbackContext) -> None:
        user = user_func(update)
        msg = str(update.message.text)
        # print(update.message)


        text = ''
        if user.state == 0:
            user.fullName = msg
            user.state = 1
            text = 'telefon raqamingizni kiriting'
            update.message.reply_text(text)
        elif user.state == 1:
            user.phone = msg
            user.state = 2
            user.save()
            text = "Iltmos suratingizni jo'nating (Selfi formad ham bo'laveradi)"
            update.message.reply_text(text)
        elif user.state == 2:
            file = update.message.photo[2].file_id
            obj = context.bot.get_file(file)
            img = obj.download()
            print(img)
            # f = File(open('path-to-file-on-server', 'r'))
            user.photo = ImageFile(open(img, "rb"))
            user.state = 7
            user.save()
            text = "Ro'yhatdan o'tish muoffaqqiyatli yakunlandi"
            update.message.reply_text(text)

        elif not user.is_staff and msg == "comment":
            user.state = 909
            user.save()
            update.message.reply_text("Comment jo'nating")
        elif not user.is_staff and user.state == 909:

            student = None
            if user.role.name == "Student":
                student = Student.objects.get(self_telegram=user)
            if user.role.name == "Father":
                student = Student.objects.get(dad_telegram=user)
            if user.role.name == "Mother":
                student = Student.objects.get(mom_telegram=user)
            commentators = Telegaram_user.objects.filter(is_staff=1)
            commentator = None
            for com in commentators:
                if student.group in com.groups.all():
                    commentator = com

            text = f"{student.group.name} {student.firstName} {student.lastName} from {user.role}"
            self.updater.bot.send_message(chat_id=commentator.telegram_user_id,
                                          text=text)
            self.updater.bot.forward_message(chat_id=commentator.telegram_user_id,
                                             from_chat_id=user.telegram_user_id,
                                             message_id=update.message.message_id)
            user.state = 7
            user.save()

        elif user.is_staff:
            groups = user.groups.all()
            if user.state == 707:
                groups_f_s = user.groups.all()
                for gurux in groups_f_s:
                    stu = Student.objects.filter(group=gurux)
                    for stud in stu:
                        try:
                            self.updater.bot.forward_message(chat_id=stud.self_telegram.telegram_user_id,
                                                             from_chat_id=user.telegram_user_id,
                                                             message_id=update.message.message_id)
                        except:
                            pass
                        try:
                            self.updater.bot.forward_message(chat_id=stud.mom_telegram.telegram_user_id,
                                                             from_chat_id=user.telegram_user_id,
                                                             message_id=update.message.message_id)
                        except:
                            pass
                        try:
                            self.updater.bot.forward_message(chat_id=stud.dad_telegram.telegram_user_id,
                                                             from_chat_id=user.telegram_user_id,
                                                             message_id=update.message.message_id)
                        except:
                            pass
                user.state = 7
                user.save()

            elif msg == "E'lon":
                update.message.reply_text("E'lon Jo'nating jo'nating")
                user.state = 707
                user.save()
            elif msg == 'topshiriq yuborish':
                keyboard = []
                user.save()
                for i in groups:
                    keyboard.append([i.name])

                reply_markup = ReplyKeyboardMarkup(keyboard)
                update.message.reply_text(text="Guruhlarni tanlang", reply_markup=reply_markup)
            elif user.state != 707:
                try:
                    msg_group = Group_me.objects.get(name=msg)
                except:
                    msg_group = None

                task = task_func(user, 0)
                if msg_group in groups:
                    last_task_off(msg_group)
                    ttask = task_func(user, 0)
                    ttask.group = msg_group
                    ttask.save()
                    update.message.reply_text(text="Savollarni yozing")
                elif task.state == 0:
                    task.tasks = msg
                    counts = msg.split("\n")
                    print(counts)
                    task.count = len(counts)
                    # user.state = None
                    user.save()
                    task.save()
                    students_ongroup = Student.objects.filter(group=task.group)
                    parents = Telegaram_user.objects.all()

                    # TODO topshiriqlar jo'natilgandan keyin
                    keyboard = [['topshiriq yuborish'], ["E'lon"]]
                    reply_markup = ReplyKeyboardMarkup(keyboard)
                    update.message.reply_text(text="Topshiriqlar jo'natildi", reply_markup=reply_markup)


                    for ase in parents:
                        # print(ase.groups.all().first())
                        if ase.groups.all().first() == task.group:
                            contentTasks = []
                            if ase.is_staff:
                                pass
                            else:
                                keyboard = [['comment']]
                                reply_markup = ReplyKeyboardMarkup(keyboard)
                                self.updater.bot.send_message(chat_id=ase.telegram_user_id,
                                                              text=str(datetime.datetime.now())[:16],
                                                              reply_markup=reply_markup)
                            for val in counts:
                                contentTasks.append([
                                    InlineKeyboardButton("Bajarildi", callback_data=f'{task.id}-1'),
                                    InlineKeyboardButton("Bajarilmadi", callback_data=f'{task.id}-0')
                                ])
                                reply_markup = InlineKeyboardMarkup(contentTasks)
                                # update.bot.send_message()
                                if ase.is_staff:
                                    pass
                                else:
                                    self.updater.bot.send_message(chat_id=ase.telegram_user_id, text=str(val),
                                                                  reply_markup=reply_markup)
                                contentTasks = []

            # update.message.reply_text('salom')
        user.save()

    def delete(self, update: Update, context: CallbackContext) -> None:
        user = user_func(update)
        query = update.callback_query
        query.answer()
        task_id = query.data[:-2]
        qData = query.data[len(query.data)-1:]

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

        task = Task.objects.get(id=task_id)
        print(task.tasks)

        score = score_func(student, task)

        if role == 1:
            score.answers_fs = score.answers_fs + 1
        if role == 2:
            score.answers_fdad = score.answers_fdad + 1
        if role == 3:
            score.answers_fmom = score.answers_fmom + 1

        score.score = score.score + int(qData)
        score.save()
        msg = query.message.text

        if qData == '1':
            query.edit_message_text(text=msg + "  ✅")
        elif qData == '0':
            query.edit_message_text(text=msg + "  ❌")

    def image_handler(bot, update):
        file = bot.getFile(update.message.photo.file_id)
        print("file_id: " + str(update.message.photo.file_id))
        file.download('image.jpg')


    def handle(self, *args, **kwargs):
        dispatcher = self.updater.dispatcher
        # dispatcher.add_handler(MessageHandler(Filters.photo, self.image_handler))
        # dispatcher.add_handler(CallbackQueryHandler(self.days2, pattern="^(\d{4}\-\d{2}\-\d{2})$"))
        dispatcher.add_handler(CallbackQueryHandler(self.delete, pattern="^(\d{1,10}\-\d{1})$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.start, pattern="^(asd\d{1})$"))
        dispatcher.add_handler(CommandHandler('start', self.language))
        # dispatcher.add_handler(CallbackQueryHandler(self.button))

        dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, self.message_handler))

        self.updater.start_polling()
        self.updater.idle()
