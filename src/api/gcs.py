from google.cloud import storage
***REMOVED***
from PIL import Image


class GCS:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(
            os.environ['GCS_BUCKET_NAME'***REMOVED***)

    def save_raw_image(self, img, album_id):
        print("saving raw image")
        blob = storage.Blob("raw/%s.png" % album_id, self.bucket)
        img.save("temp.png", "PNG")
        with open("temp.png", "rb") as f:
            blob.upload_from_file(f, content_type="image/png")
        return os.environ['GCS_MEDIA_URL'***REMOVED*** + "raw/" + album_id + ".png"

    def save_rendered_image(self, img, album_id, render_mode):
        print("saving rendered image")
        blob = storage.Blob("%s/%s.png" % (render_mode, album_id), self.bucket)
        img.save("temp.png", "PNG")
        with open("temp.png", "rb") as f:
            blob.upload_from_file(f, content_type="image/png")
        return os.environ['GCS_MEDIA_URL'***REMOVED*** + render_mode + "/" + album_id + ".png"
