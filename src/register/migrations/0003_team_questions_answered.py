# Generated by Django 3.1 on 2020-09-06 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_auto_20200831_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='questions_answered',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]