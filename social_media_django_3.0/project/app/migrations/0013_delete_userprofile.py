# Generated by Django 4.0.3 on 2022-04-02 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]