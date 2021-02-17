# Generated by Django 3.1.6 on 2021-02-17 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ***REMOVED***

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(max_length=100)),
                ('artist_name', models.CharField(max_length=100)),
                ('album_name', models.CharField(max_length=100)),
                ('raw_image', models.ImageField(upload_to='raw')),
            ***REMOVED***,
        ),
        migrations.CreateModel(
            name='Render',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('render_mode', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='rendered/<django.db.models.fields.CharField>')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualizer.album')),
            ***REMOVED***,
        ),
    ***REMOVED***
