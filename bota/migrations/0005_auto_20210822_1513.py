# Generated by Django 3.1.2 on 2021-08-22 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bota', '0004_auto_20210821_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study_groups',
            name='telegram_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bota.telegram_guruxlar'),
        ),
    ]
