# Generated by Django 3.1.2 on 2021-08-13 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bota', '0002_auto_20210813_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mom_telegram',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='motherTelegram', to='bota.telegaram_user'),
        ),
    ]
