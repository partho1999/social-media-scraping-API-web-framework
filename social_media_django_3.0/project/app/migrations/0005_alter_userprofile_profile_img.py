# Generated by Django 4.0.3 on 2022-03-31 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_img',
            field=models.ImageField(default='images/default.png', upload_to=''),
        ),
    ]
