from django.db import models

# Create your models here.


class Parent(models.Model):
    STATE_FULLNAME = 0
    STATE_PHONE = 1

    telegram_user_id = models.CharField(max_length=100, primary_key=True)
    # user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='client')
    fullName = models.CharField(max_length=50, default=None, null=True)
    phone = models.CharField(max_length=15, default=None, null=True)

    state = models.IntegerField(default=STATE_FULLNAME)

