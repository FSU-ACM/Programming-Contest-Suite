# Generated by Django 3.1 on 2021-02-26 23:01

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('division', models.PositiveSmallIntegerField(choices=[(1, 'Upper Division'), (2, 'Lower Division')])),
                ('pin', models.CharField(max_length=4, unique=True)),
                ('contest_id', models.CharField(blank=True, max_length=7, null=True, unique=True)),
                ('contest_password', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('questions_answered', models.PositiveSmallIntegerField(default=0)),
                ('members', django_mysql.models.ListTextField(models.CharField(max_length=181), default=[], max_length=543, size=3)),
                ('num_members', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
    ]
