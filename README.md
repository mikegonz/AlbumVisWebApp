# AlbumVis - Spotify Album Art Visualizer

## What is this?

AlbumVis is a web app that displays the album artwork of a Spotify user’s currently playing track.

You're asked to sign in with Spotify, and once you allow the app access you can select a display-mode from one of the following:

- **center** - display album image on a black background
- **solid** - display image on a background of an appropriate color
- **mirror-side** - display image side by side with mirrored images
- **mirror-side-blur** - same as above but with the mirrored images blurred and blended

Then click `start visualization` and it will create and display an image containing the album art of your currently playing track on Spotify.

## Where?

It's currently hosted on Google Cloud App Engine here:

https://albumvis.uk.r.appspot.com/

## Internals

The application’s update loop queries the Spotify API every 2 seconds for the user’s currently playing track. If the track has changed since the last update, it checks if a track from this album has been played before. If so, it can grab the album artwork image from its directory of cached images. Otherwise, it gets the album artwork URL from the API call’s response and saves it to the cache.

If AlbumVis has seen this song before while running under the same visualization mode, then it can grab the rendered fullscreen visualization from the cache and display that. If not, it calls the appropriate render function to create this visualization—perhaps by placing the album artwork on a background of an appropriate color, or creating a mirror effect with several copies of the image. The visualization for the previous track fades into the new one and waits for the next update.
