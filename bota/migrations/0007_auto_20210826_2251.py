# Generated by Django 3.1.2 on 2021-08-26 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bota', '0006_telegaram_user_role_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='all_score_f_dad',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='all_score_f_mom',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='all_score_f_self',
            field=models.IntegerField(default=0),
        ),
    ]
