# Generated by Django 3.1.6 on 2021-02-22 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_album_url'),
    ***REMOVED***

    operations = [
        migrations.AddField(
            model_name='render',
            name='url',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ***REMOVED***
