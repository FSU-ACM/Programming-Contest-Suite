# Generated by Django 3.1 on 2020-08-24 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='name',
            field=models.CharField(default='Programming I', max_length=50),
            preserve_default=False,
        ),
    ]