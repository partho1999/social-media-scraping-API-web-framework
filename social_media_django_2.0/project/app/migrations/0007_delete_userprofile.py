# Generated by Django 4.0.3 on 2022-03-31 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_userprofile_profile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
