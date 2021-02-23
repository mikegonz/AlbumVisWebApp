from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import urllib
from PIL import Image, ImageFilter
from math import floor, ceil
import operator

from django.conf import settings
from .models import Album, Render

MULT = 2

WIDTH = 2560
HEIGHT = 1600

### helper fn to return avg color sampled from top and bottom of image
def calculate_average_colors(im, sample_count):
    top_color = (0, 0, 0)
    bottom_color = (0, 0, 0)
    y = (im.height/(sample_count*2))
    for j in range(sample_count):
        x = j * im.width/sample_count + (im.width/(sample_count*2))
        top_color = tuple(map(operator.add, top_color, im.getpixel((x,y))))
    
    y = 15 * im.height/sample_count + (im.height/(sample_count*2))
    for j in range(sample_count):
        x = j * im.width/sample_count + (im.width/(sample_count*2))
        bottom_color = tuple(map(operator.add, bottom_color, im.getpixel((x,y))))
    top_color = tuple(map(operator.floordiv, top_color, (sample_count, sample_count, sample_count)))
    bottom_color = tuple(map(operator.floordiv, bottom_color, (sample_count, sample_count, sample_count)))
    return top_color, bottom_color

### render image flanked by mirrored panels on either side, with border
# on top and bottom of avg colors sampled from the top of bottom of img, respectively
# if is_blur, the mirrored side panels are blurred and muted as well
def render_image_mirror_side(im, is_blur):
    COLOR_SAMPLE_COUNT = 16
    BLUR_FACTOR = 10
    BLEND_FACTOR = 0.25

    width = floor(WIDTH / MULT)
    height = floor(HEIGHT / MULT)
    side_panel_width = round((width - im.width) / 2)
    border_height = round((height - im.height) / 2)
    top_color, bottom_color = calculate_average_colors(im, COLOR_SAMPLE_COUNT)

    left_panel = im\
        .crop((0, 0, side_panel_width, im.height))\
        .transpose(Image.FLIP_LEFT_RIGHT)
    right_panel = im\
        .crop((im.width - side_panel_width, 0, im.width, im.height))\
        .transpose(Image.FLIP_LEFT_RIGHT)

    if(is_blur):
        maskim = Image.new('RGB', (side_panel_width, im.height), tuple(map(operator.floordiv, tuple(map(operator.add, top_color, bottom_color)), (2, 2, 2))))
        left_panel = Image.blend(
            left_panel.filter(ImageFilter.GaussianBlur(BLUR_FACTOR)),
            maskim, BLEND_FACTOR)
        right_panel = Image.blend(
            right_panel.filter(ImageFilter.GaussianBlur(BLUR_FACTOR)),
            maskim, BLEND_FACTOR)

    fullim = Image.new('RGB', (width, height), bottom_color)
    fullim.paste(Image.new('RGB', (width, round(height/2)), top_color), (0, 0, width, round(height/2)))
    fullim.paste(im, (side_panel_width, border_height, side_panel_width + im.width, border_height + im.height))
    fullim.paste(left_panel, (0, border_height, side_panel_width, im.height + border_height))
    fullim.paste(right_panel, (width - side_panel_width, border_height, width, im.height + border_height))
#    fullim.save(write_path, 'PNG')
    return fullim

### render album art in center of a black background
def render_image_center(im):
    width = floor(WIDTH / MULT)
    height = floor(HEIGHT / MULT)
    fullim = Image.new('RGB', (width, height), 'black')
    fullim.paste(im, (floor(width/2 - im.width/2), floor(height/2 - im.height/2), floor(width/2 + im.width/2), floor(height/2 + im.height/2)))
    # fullim.save(write_path, 'PNG')
    return fullim        

### render album art in center of a solid background of a sampled average color
def render_image_solid(im):
    width = floor(WIDTH / MULT)
    height = floor(HEIGHT / MULT)

    avgcol = (0, 0, 0)
    for i in [0,15***REMOVED***:
        y = i * im.height/16 + (im.height/32)
        for j in range(16):
            x = j * im.width/16 + (im.width/32)
            avgcol = tuple(map(operator.add, avgcol, im.getpixel((x,y))))
    for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14***REMOVED***:
        y = i * im.height/16 + (im.height/32)
        for j in [0,15***REMOVED***:
            x = j * im.width/16 + (im.width/32)
            avgcol = tuple(map(operator.add, avgcol, im.getpixel((x,y))))
            
    avgcol = tuple(map(operator.floordiv, avgcol, (60, 60, 60)))
    fullim = Image.new('RGB', (width, height), avgcol)
    fullim.paste(im, (floor(width/2 - im.width/2), floor(height/2 - im.height/2), floor(width/2 + im.width/2), floor(height/2 + im.height/2)))
    # fullim.save(write_path, 'PNG')
    return fullim

class Visualizer:
    def __init__(self, username, spotify):
        self.sp = spotify

    def currently_playing_track(self):
        track = self.sp.current_user_playing_track()
        return track

    # TODO: it shouldn't return if track is different but from same album

    def wait_for_next_track(self):
        track = self.sp.current_user_playing_track()
        while(True):
            sleep(3)
            newtrack = self.sp.current_user_playing_track()
            if track is None:
                if newtrack is not None:
                    return newtrack
            ***REMOVED***
                if newtrack is not None:
                    if track['item'***REMOVED***['id'***REMOVED*** != newtrack['item'***REMOVED***['id'***REMOVED***: #TODO: (new)track['item'***REMOVED*** itself can be None!!!!
                        return newtrack

    def get_raw_album(self, track):
        raw_url = settings.MEDIA_URL + "raw/" + \
            track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED*** + '.jpg'
        if len(Album.objects.filter(uri=track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED***)) != 0:
            return Album.objects.get(uri=track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED***)

        raw_path = settings.MEDIA_ROOT + "/raw/" + \
            track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED*** + '.jpg'
        raw_img_url = track['item'***REMOVED***['album'***REMOVED***['images'***REMOVED***[0***REMOVED***['url'***REMOVED***
        urllib.request.urlretrieve(raw_img_url, raw_path)
        raw_img = Image.open(raw_path)
        if raw_img.mode == "L":  # if grayscale, convert to RGB
            raw_img = raw_img.convert("RGB")
            raw_img.save(raw_path, "PNG")
        alb = Album(uri=track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED***,
                    artist_name="someone", album_name="someone", raw_image=raw_path, url=raw_url)
        alb.save()
        return alb

    def get_render_path(self, track, render_mode):
        alb = self.get_raw_album(track)
        render_url = settings.MEDIA_URL + render_mode + "/" + \
            track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED*** + '.png'
        if len(alb.render_set.filter(render_mode=render_mode)) != 0:
            return render_url
        
        raw_img = Image.open(alb.raw_image)
        rendered_img = None
        if render_mode == "mirror-side":
            rendered_img = render_image_mirror_side(raw_img, False)
        elif render_mode == "mirror-side-blur":
            rendered_img = render_image_mirror_side(raw_img, True)
        elif render_mode == "solid":
            rendered_img = render_image_solid(raw_img)
        ***REMOVED***
            rendered_img = render_image_center(raw_img)
        
        render_path = settings.MEDIA_ROOT + "/" + render_mode + "/" + \
            track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED*** + ".png"
        rendered_img.save(render_path, "PNG")

        ren = Render(album=alb, render_mode=render_mode, image=render_path, url=render_url)
        ren.save()
        return render_url