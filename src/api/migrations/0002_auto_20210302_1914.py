# Generated by Django 3.1.6 on 2021-03-03 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='raw_image',
        ),
        migrations.RemoveField(
            model_name='render',
            name='image',
        ),
    ]
