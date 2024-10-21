import os

ROOT_DIR = os.getcwd()
FONTS_DIR = os.path.join(ROOT_DIR, "fonts")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
TEMP_DIR = os.path.join(ROOT_DIR, "temp")
DIGITAL_DIR = os.path.join(TEMP_DIR, "digital")
PRINTABLE_DIR = os.path.join(TEMP_DIR, "printable")

DROPBOX_BASE_PATH = "/Flyers"
DROPBOX_DIGITAL_PATH = DROPBOX_BASE_PATH + "/Digital"
DROPBOX_PRINTABLE_PATH = DROPBOX_BASE_PATH + "/Printable"
