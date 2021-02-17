from django.db import models


class Album(models.Model):
    uri = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    album_name = models.CharField(max_length=100)
    raw_image = models.ImageField(upload_to='raw')


class Render(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    render_mode = models.CharField(max_length=20)
    image = models.ImageField(upload_to='rendered')
