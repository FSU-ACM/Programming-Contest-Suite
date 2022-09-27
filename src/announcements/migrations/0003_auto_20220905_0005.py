# Generated by Django 3.2.15 on 2022-09-05 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0002_alter_announcement_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='send_discord',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='announcement',
            name='send_email',
            field=models.BooleanField(default=True),
        ),
    ]
