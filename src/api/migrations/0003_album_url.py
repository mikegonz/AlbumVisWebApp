# Generated by Django 3.1.6 on 2021-02-20 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210220_2243'),
    ***REMOVED***

    operations = [
        migrations.AddField(
            model_name='album',
            name='url',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ***REMOVED***