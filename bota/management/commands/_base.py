from telegram.ext import Updater
from django.core.management.base import BaseCommand
from config.settings import BOT_TOKEN


class BotBase(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(BotBase, self).__init__(*args, **kwargs)

        self.updater = Updater(BOT_TOKEN)