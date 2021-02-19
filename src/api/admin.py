from django.contrib import admin
from .models import Album, Render

# Register your models here.
admin.site.site_title = "AlbumVis API"


admin.site.register(Album)
admin.site.register(Render)
