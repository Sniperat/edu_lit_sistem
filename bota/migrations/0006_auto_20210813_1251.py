# Generated by Django 3.1.2 on 2021-08-13 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bota', '0005_auto_20210813_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegaram_user',
            name='groups',
            field=models.ManyToManyField(blank=True, to='bota.Group_me'),
        ),
    ]
