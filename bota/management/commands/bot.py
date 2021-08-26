from django.core.files.images import ImageFile
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Location, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, RegexHandler, \
    MessageHandler
import requests, calendar
import datetime
from django.contrib.auth.models import Group

from django.conf import settings
from ._base import BotBase
from bota.functions import user_func, task_func, score_func, last_task_off, student_func, telegram_group_func
from bota.models import Study_groups, Telegaram_user, Task, Scores, Student

from django.core.validators import EmailValidator

import random


class Command(BotBase):

    def language(self, update: Update, context: CallbackContext) -> None:
        user = user_func(update)
        user.state = 0
        user.save()
        update.message.reply_text("Ismingizni kiriting.")

    def message_handler(self, update: Update, context: CallbackContext) -> None:
        user = user_func(update)
        msg = str(update.message.text)

        if update.message.chat.type == 'group':
            telegram_group_func(update)
        else:
            text = ''
            if user.state == 0:
                user.firstName = msg
                user.state = 3
                text = 'Familiyangizni kiriting.'
                update.message.reply_text(text)
            elif user.state == 3:
                user.lastName = msg
                user.state = 4
                text = 'Sharifingizni kiriting.'
                update.message.reply_text(text)
            elif user.state == 4:
                user.secondName = msg
                user.state = 5
                text = "To'liq manzilingizni kiriting"
                update.message.reply_text(text)
            elif user.state == 5:
                user.address = msg
                user.state = 6
                user.save()
                text = 'telefon raqamingizni kiriting'
                update.message.reply_text(text)
            elif user.state == 11 or user.state == 12:
                user.role_name = msg
                user.save()
                text = "Farzandingiz o'qiydigan guruhni tanlang"
                sg = Study_groups.objects.all()
                content = []
                for i in sg:
                    content.append([
                        InlineKeyboardButton(i.name, callback_data='group{}'.format(i.id))
                    ])
                reply_markup = InlineKeyboardMarkup(content)
                update.message.reply_text(text, reply_markup=reply_markup)
            elif user.state == 6:
                user.phone = msg
                user.state = 7
                user.save()
                content = [[
                    InlineKeyboardButton("bekor qilish", callback_data='bekor qilish')

                ]]
                reply_markup = InlineKeyboardMarkup(content)
                text = "Iltmos suratingizni jo'nating (Selfi formad ham bo'laveradi)\n\n" \
                        "Surat jo'natish majburiy!"
                       # "Faqat arzirli sabab bilangina surat yuborishni bekor qiling "
                update.message.reply_text(text)
            elif user.state == 7:
                file = update.message.photo[2].file_id
                obj = context.bot.get_file(file)
                img = obj.download()
                print(img)
                # f = File(open('path-to-file-on-server', 'r'))
                user.photo = ImageFile(open(img, "rb"))
                user.state = 8
                user.save()
                text = "Men ..."
                grp = Group.objects.all()
                content = []
                for i in grp:
                    content.append([
                        InlineKeyboardButton(i.description, callback_data='role{}'.format(i.id))
                    ])
                reply_markup = InlineKeyboardMarkup(content)
                # update.message.reply_text(text, reply_markup=reply_markup)
                self.updater.bot.send_message(chat_id=user.telegram_user_id,
                                              text=text, reply_markup=reply_markup)

            elif not user.is_staff and msg == "izoh qoldirish" and user.state == 77:
                user.state = 909
                user.save()
                update.message.reply_text("O'z izohlaringiz bilan bo'lishing")
            elif not user.is_staff and user.state == 909:

                student = None
                if user.role.name == "Student":
                    student = Student.objects.get(self_telegram=user)
                if user.role.name == "Father":
                    student = Student.objects.get(dad_telegram=user)
                if user.role.name == "Mother":
                    student = Student.objects.get(mom_telegram=user)


                text = f"{student.group.name} {student.firstName} {student.lastName} from {user.role_name}"
                self.updater.bot.send_message(chat_id=student.group.mertor.telegram_user_id,
                                              text=text)
                self.updater.bot.forward_message(chat_id=student.group.mertor.telegram_user_id,
                                                 from_chat_id=user.telegram_user_id,
                                                 message_id=update.message.message_id)
                user.state = 77
                user.save()

            elif user.is_staff:
                if user == 77:
                    keyboard = [["E'lon"]]
                    reply_markup = ReplyKeyboardMarkup(keyboard)
                    update.message.reply_text(text="Topshiriqlar jo'natildi", reply_markup=reply_markup)

                # groups = user.groups.all()
                elif user.state == 707:
                    groups_f_s = Study_groups.objects.filter(mertor=user)
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
                    user.state = 77
                    user.save()

                elif msg == "E'lon":
                    update.message.reply_text("E'lon Jo'nating")
                    user.state = 707
                    user.save()
                #     todo BU polya topshiriq yuborish
                # elif msg == 'topshiriq yuborish':
                #     keyboard = []
                #     user.save()
                #     for i in groups:
                #         keyboard.append([i.name])
                #
                #     reply_markup = ReplyKeyboardMarkup(keyboard)
                #     update.message.reply_text(text="Guruhlarni tanlang", reply_markup=reply_markup)
                # todo BU POLYA TALABALARGA VA OTA ONALARGA TOPSHITIQ KETISHI
                # elif user.state != 707:
                #     try:
                #         msg_group = Study_groups.objects.get(name=msg)
                #     except:
                #         msg_group = None
                #
                #     task = task_func(user, 0)
                #     if msg_group in groups:
                #         last_task_off(msg_group)
                #         ttask = task_func(user, 0)
                #         ttask.group = msg_group
                #         ttask.save()
                #         update.message.reply_text(text="Savollarni yozing")
                #     elif task.state == 0:
                #         task.tasks = msg
                #         counts = msg.split("\n")
                #         print(counts)
                #         task.count = len(counts)
                #         # user.state = None
                #         user.save()
                #         task.save()
                #         students_ongroup = Student.objects.filter(group=task.group)
                #         parents = Telegaram_user.objects.all()
                #
                #         # TODO topshiriqlar jo'natilgandan keyin
                #         keyboard = [['topshiriq yuborish'], ["E'lon"]]
                #         reply_markup = ReplyKeyboardMarkup(keyboard)
                #         update.message.reply_text(text="Topshiriqlar jo'natildi", reply_markup=reply_markup)
                #
                #
                #         for ase in parents:
                #             # print(ase.groups.all().first())
                #             if ase.groups.all().first() == task.group:
                #                 contentTasks = []
                #                 if ase.is_staff:
                #                     pass
                #                 else:
                #                     keyboard = [['izoh qoldirish']]
                #                     reply_markup = ReplyKeyboardMarkup(keyboard)
                #                     self.updater.bot.send_message(chat_id=ase.telegram_user_id,
                #                                                   text=str(datetime.datetime.now())[:16],
                #                                                   reply_markup=reply_markup)
                #                 for val in counts:
                #                     contentTasks.append([
                #                         InlineKeyboardButton("Bajarildi", callback_data=f'{task.id}-1'),
                #                         InlineKeyboardButton("Bajarilmadi", callback_data=f'{task.id}-0')
                #                     ])
                #                     reply_markup = InlineKeyboardMarkup(contentTasks)
                #                     # update.bot.send_message()
                #                     if ase.is_staff:
                #                         pass
                #                     else:
                #                         self.updater.bot.send_message(chat_id=ase.telegram_user_id, text=str(val),
                #                                                       reply_markup=reply_markup)
                #                     contentTasks = []

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
            try:
                student = Student.objects.get(self_telegram=user)
            except:
                pass
            role = 1
        if user.role.name == "Father":
            try:
                student = Student.objects.get(dad_telegram=user)
            except:
                pass
            role = 2
        if user.role.name == "Mother":
            try:
                student = Student.objects.get(mom_telegram=user)
            except:
                pass
            role = 3

        task = Task.objects.get(id=task_id)
        print(task.tasks)

        score = score_func(student, task)

        if role == 1:
            score.answers_fs = score.answers_fs + 1
            score.score_fs = score.score_fs + int(qData)
        if role == 2:
            score.answers_fdad = score.answers_fdad + 1
            score.score_fdad = score.score_fdad + int(qData)
        if role == 3:
            score.answers_fmom = score.answers_fmom + 1
            score.score_fmom = score.score_fmom + int(qData)

        score.save()
        msg = query.message.text

        if qData == '1':
            query.edit_message_text(text=msg + "  ✅")
        elif qData == '0':
            query.edit_message_text(text=msg + "  ❌")

    def dec(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        user = user_func(update)
        user.state = 77
        user.save()
        text = "Ro'yhatdan o'tish muoffaqqiyatli yakunlandi"
        # update.message.reply_text(text)
        query.edit_message_text(text)

    def contin(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        pk = query.data[4:]
        print(pk)
        gruppa = Group.objects.get(id=int(pk))
        user = user_func(update)
        user.role = gruppa
        if gruppa.name == 'Student':
            newstudent = student_func(user)
            newstudent.firstName = ''.join(user.firstName),
            newstudent.lastName = ''.join(user.lastName),
            newstudent.secondName = ''.join(user.secondName),
            newstudent.address = ''.join(user.address),
            newstudent.self_telegram = user

            newstudent.save()

            newstudent.firstName = ''.join(newstudent.firstName)
            newstudent.lastName = ''.join(newstudent.lastName)
            newstudent.secondName = ''.join(newstudent.secondName)
            newstudent.address = ''.join(newstudent.address)
            newstudent.save()
            print(newstudent.firstName, newstudent.lastName, newstudent.secondName)
            text = "O'z guruhingizni tanlag"
            sg = Study_groups.objects.all()
            content = []
            for i in sg:
                content.append([
                    InlineKeyboardButton(i.name, callback_data='group{}'.format(i.id))
                ])
            reply_markup = InlineKeyboardMarkup(content)
            query.edit_message_text(text, reply_markup=reply_markup)
            user.state = 77
        elif gruppa.name == 'Father':

            user.state = 11
            content = [[
                        InlineKeyboardButton("Men farzandim nomidan to'dirdim", callback_data='stufparent')
                    ]]
            reply_markup = InlineKeyboardMarkup(content)
            text = "Iltimos Talabaga kim ekanligingizni yozing \n\n Agar Farzandingiz telefon ishlatmasa " \
                   "va siz malumotlarni uning nomidan to'ldirgan bo'lsangiz pastagi tugmani bosing"
            query.edit_message_text(text, reply_markup=reply_markup)
            #todo
            # text = "Farzandingiz o'qiydigan guruhni tanlang"
            # sg = Study_groups.objects.all()
            # content = []
            # for i in sg:
            #     content.append([
            #         InlineKeyboardButton(i.name, callback_data='group{}'.format(i.id))
            #     ])
            # reply_markup = InlineKeyboardMarkup(content)
            # query.edit_message_text(text, reply_markup=reply_markup)
        elif gruppa.name == 'Mother':

            user.state = 12
            content = [[
                InlineKeyboardButton("Men farzandim nomidan to'dirdim", callback_data='stufparent')
            ]]
            reply_markup = InlineKeyboardMarkup(content)
            text = "Iltimos Talabaga kim ekanligingizni yozing \n\n Agar Farzandingiz telefon ishlatmasa " \
                   "va siz malumotlarni uning nomidan to'ldirgan bo'lsangiz pastagi tugmani bosing"
            query.edit_message_text(text=text, reply_markup=reply_markup)

            # text = "Iltimos Talabaga kim ekanligingizni yozing"
            # todo
            # text = "Farzandingiz o'qiydigan guruhni tanlang"
            # sg = Study_groups.objects.all()
            # content = []
            # for i in sg:
            #     content.append([
            #         InlineKeyboardButton(i.name, callback_data='group{}'.format(i.id))
            #     ])
            # reply_markup = InlineKeyboardMarkup(content)
            # query.edit_message_text(text, reply_markup=reply_markup)
        elif gruppa.name == 'Teacher':
            query.message.delete()
            keyboard = [["E'lon"]]
            reply_markup = ReplyKeyboardMarkup(keyboard)
            text = 'salom {}'.format(user.firstName)
            self.updater.bot.send_message(chat_id=user.telegram_user_id, text=text,
                                          reply_markup=reply_markup)

        # user.gro = 77

        user.save()
        # text = "Ro'yhatdan o'tish muoffaqqiyatli yakunlandi"
        # # update.message.reply_text(text)
        # query.edit_message_text(text)

    # TODO Talaba registratsiyasi tugadi
    def group(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        pk = query.data[5:]
        print(pk)
        gruppa = Study_groups.objects.get(id=int(pk))
        user = user_func(update)
        if user.state == 77:
            student = student_func(user)
            student.group = gruppa
            student.save()
            keyboard = [['izoh qoldirish']]
            query.message.delete()
            reply_markup = ReplyKeyboardMarkup(keyboard)
            text = "Ro'yhatdan o'tish muoffaqqiyatli yakunlandi"
            self.updater.bot.send_message(chat_id=user.telegram_user_id, text=text, reply_markup=reply_markup)
            # query.edit_message_text(text, )
        else:
            text = "Ro'yxatdan farzandingizni belgilang"
            sg = Student.objects.filter(group=gruppa)
            content = []
            for i in sg:
                content.append([
                    InlineKeyboardButton(i.firstName+' '+i.lastName, callback_data='studfp{}'.format(i.id))
                ])
            reply_markup = InlineKeyboardMarkup(content)
            query.edit_message_text(text, reply_markup=reply_markup)


    def stud_f_p(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        pk = query.data[6:]
        user = user_func(update)
        stud = Student.objects.get(id=pk)
        if user.state == 11:
            stud.dad_telegram = user
        elif user.state == 12:
            stud.mom_telegram = user
        stud.save()
        user.state = 77
        user.save()
        query.message.delete()
        keyboard = [['izoh qoldirish']]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        text = "Ro'yhatdan o'tish muoffaqqiyatli yakunlandi"
        self.updater.bot.send_message(chat_id=user.telegram_user_id, text=text,
                                      reply_markup=reply_markup)
        # update.message.reply_text(text, reply_markup=reply_markup)
        # update.message.reply_text(text)
        # query.edit_message_text(text, reply_markup=reply_markup)

    def stufparent(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        text = "Farzandingiz guruhini tanlang"
        sg = Study_groups.objects.all()
        content = []
        for i in sg:
            content.append([
                InlineKeyboardButton(i.name, callback_data='groupv2{}'.format(i.id))
            ])
        reply_markup = InlineKeyboardMarkup(content)
        query.edit_message_text(text, reply_markup=reply_markup)

    def groupv2(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        pk = query.data[7:]
        print(pk)
        gruppa = Study_groups.objects.get(id=int(pk))
        user = user_func(update)
        newstudent = Student()
        newstudent.firstName = ''.join(user.firstName),
        newstudent.lastName = ''.join(user.lastName),
        newstudent.secondName = ''.join(user.secondName),
        newstudent.address = ''.join(user.address),
        newstudent.group = gruppa
        

        newstudent.save()

        newstudent.firstName = ''.join(newstudent.firstName)
        newstudent.lastName = ''.join(newstudent.lastName)
        newstudent.secondName = ''.join(newstudent.secondName)
        newstudent.address = ''.join(newstudent.address)
        newstudent.save()
        user.state = 0
        user.save()

        query.edit_message_text('Farzandingiz malumotlari saqlandi!\n\nEndi iltmos shaxsiy malumotlaringizni qaytadan '
                                'kiriting va oz shaxsingizni tasdiqlang')
        self.updater.bot.send_message(chat_id=user.telegram_user_id,
                                      text='ismingizni kiriting')




    def handle(self, *args, **kwargs):
        dispatcher = self.updater.dispatcher
        # dispatcher.add_handler(MessageHandler(Filters.photo, self.image_handler))
        # dispatcher.add_handler(CallbackQueryHandler(self.days2, pattern="^(\d{4}\-\d{2}\-\d{2})$"))
        dispatcher.add_handler(CallbackQueryHandler(self.delete, pattern="^(\d{1,10}\-\d{1})$"))
        dispatcher.add_handler(CallbackQueryHandler(self.dec, pattern="^(bekor qilish)$"))
        dispatcher.add_handler(CallbackQueryHandler(self.stufparent, pattern="^(stufparent)$"))
        dispatcher.add_handler(CallbackQueryHandler(self.contin, pattern="^(role\d{1})$"))
        dispatcher.add_handler(CallbackQueryHandler(self.group, pattern="^(group\d{1,10})$"))
        dispatcher.add_handler(CallbackQueryHandler(self.groupv2, pattern="^(groupv2\d{1,10})$"))
        dispatcher.add_handler(CallbackQueryHandler(self.stud_f_p, pattern="^(studfp\d{1,10})$"))
        # dispatcher.add_handler(CallbackQueryHandler(self.start, pattern="^(asd\d{1})$"))
        dispatcher.add_handler(CommandHandler('start', self.language))
        # dispatcher.add_handler(CallbackQueryHandler(self.button))

        dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, self.message_handler))

        self.updater.start_polling()
        self.updater.idle()
