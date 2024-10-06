import os
from dotenv import load_dotenv

load_dotenv(".env.local")
import dropbox

DROPBOX_APP_KEY = os.environ.get("DROPBOX_APP_KEY", "")
DROPBOX_APP_SECRET = os.environ.get("DROPBOX_APP_SECRET", "")
DROPBOX_REFRESH_TOKEN = os.environ.get("DROPBOX_REFRESH_TOKEN", "")

dbx = dropbox.Dropbox(
    app_key=DROPBOX_APP_KEY,
    app_secret=DROPBOX_APP_SECRET,
    oauth2_refresh_token=DROPBOX_REFRESH_TOKEN,
)

with open("./flyer/FlyerTemplate.pdf", "rb") as f:
    dbx.files_upload(f.read(), "/flyer/FlyerTemplate1.pdf")

print("Uploaded to Dropbox")
