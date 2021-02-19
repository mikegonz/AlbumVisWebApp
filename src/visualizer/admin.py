from django.contrib import admin

from .models import Album, Render

admin.site.site_title = "AlbumVis - Spotify Album Visualizer"

admin.site.register(Album)
admin.site.register(Render)
