from google.cloud import storage
import os
from PIL import Image
from io import BytesIO


class GCS:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(
            os.environ['GCS_BUCKET_NAME'])

    def save_rendered_image(self, img, album_id, render_mode):
        print("saving rendered image")
        blob = storage.Blob("%s/%s.png" % (render_mode, album_id), self.bucket)
        temp = BytesIO()
        img.save(temp, "PNG")
        blob.upload_from_string(temp.getvalue(), content_type="image/png")
        return os.environ['GCS_MEDIA_URL'] + render_mode + "/" + album_id + ".png"
