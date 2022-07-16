# Generated by Django 3.2.13 on 2022-07-16 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('lfg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LFGProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('discord_username', models.CharField(max_length=32)),
                ('discord_discriminator', models.SmallIntegerField()),
                ('division', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Upper Division'), (2, 'Lower Division')], null=True)),
                ('standing', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Graduate'), (2, 'Senior'), (3, 'Junior'), (4, 'Sophomore'), (5, 'Freshman'), (6, 'Other')], null=True)),
                ('active', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
    ]
