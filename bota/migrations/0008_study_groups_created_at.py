# Generated by Django 3.1.2 on 2021-08-27 10:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bota', '0007_auto_20210826_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='study_groups',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
