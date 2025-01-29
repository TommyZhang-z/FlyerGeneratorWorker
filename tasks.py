from io import BytesIO
import os
from dotenv import load_dotenv
from celery import Celery
from data import TEXT_DATA
from models import PDF, Font, Image, Text
import dropbox
import datetime
from helper import convert_to_currency, convert_to_syd_time
import requests
import logging
import config as cfg
import fitz
from google_drive import upload_or_replace_file, TARGET_FOLDER_ID

load_dotenv(".env.local")

# Get Redis URL from environment or use default
os.makedirs(cfg.TEMP_DIR, exist_ok=True)
os.makedirs(cfg.DIGITAL_DIR, exist_ok=True)
os.makedirs(cfg.PRINTABLE_DIR, exist_ok=True)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY", "")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET", "")
DROPBOX_REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN", "")

BANNER_PATH = os.path.join(cfg.ASSETS_DIR, "banner.png")
EMPTY_DIGITAL_PATH = os.path.join(cfg.ASSETS_DIR, "Empty_Digital.pdf")
EMPTY_PRINTABLE_PATH = os.path.join(cfg.ASSETS_DIR, "Empty_Printable.pdf")

# Initialize Celery app
app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)
app.conf.broker_connection_retry_on_startup = True
dbx = dropbox.Dropbox(
    app_key=DROPBOX_APP_KEY,
    app_secret=DROPBOX_APP_SECRET,
    oauth2_refresh_token=DROPBOX_REFRESH_TOKEN,
)


@app.task
def generate_flyer(
    flyer_id,
    generate,
    property_id,
    facade,
    floorplan_model,
    price,
    suburb,
    address,
    lot,
    land_price,
    house_price,
    land_size,
    house_size,
    lot_width,
    rego,
    bedroom,
    bathroom,
    parking_slot,
    facade_file_url,
    floorplan_file_url,
):
    logging.info(f"generating flyer [#{flyer_id}] ...")
    facade_name = facade
    digital_file_name = f"{flyer_id}_digital.pdf"

    digital_path = os.path.join(cfg.DIGITAL_DIR, digital_file_name)

    try:
        with (
            requests.Session() as session,
            open(BANNER_PATH, "rb") as banner_file,
            open(EMPTY_DIGITAL_PATH, "rb") as empty_digital_file,
            # open(EMPTY_PRINTABLE_PATH, "rb") as empty_printable_file,
            open(
                os.path.join(cfg.ASSETS_DIR, "fc_names", f"{facade_name}.png"), "rb"
            ) as png_file,
        ):
            facade = Image(session.get(facade_file_url).content)
            floorplan = PDF(
                fitz.open(stream=BytesIO(session.get(floorplan_file_url).content))
            )
            banner = Image(banner_file.read())
            empty_digital = PDF(fitz.open(empty_digital_file))
            # empty_printable = PDF(fitz.open(empty_printable_file))
            png_image = Image(png_file.read())
        empty_digital.insert_font(Font.INTER_LIGHT)
        empty_digital.insert_font(Font.INTER_REGULAR)
        empty_digital.insert_font(Font.INTER_BOLD)
        empty_digital.insert_font(Font.INTER_SEMIBOLD)

        empty_digital.add_image(facade, position=(0, 0), stretch=True)
        empty_digital.add_image(
            banner, position=(841.8900146484375 - 179.2, 44), image_size=(179.2, 56)
        )
        empty_digital.add_pdf(
            floorplan,
            position=(35, 632),
            size=(175 / 297 * 841.8900146484375, 125 / 420 * 1190.550048828125),
        )

        page_width = 841.8900146484375
        page_height = 1190.550048828125
        image_width = 23.52
        image_height = 6.34
        image_width_pt = image_width * 2.8346  # ≈ 66.67 points
        image_height_pt = image_height * 2.8346  # ≈ 17.98 points
        x_pos = page_width - image_width_pt - 10
        y_pos = 420

        empty_digital.add_image(
            png_image,
            position=(x_pos, y_pos),
            image_size=(image_width_pt, image_height_pt),
        )

        digital_texts = [
            # Lot info
            Text(text=suburb, **TEXT_DATA["digital"]["lot_info"]["suburb"]),
            Text(text=address, **TEXT_DATA["digital"]["lot_info"]["address"]),
            Text(text=f"LOT {lot}", **TEXT_DATA["digital"]["lot_info"]["lot_number"]),
            Text(
                text=convert_to_syd_time(rego),
                **TEXT_DATA["digital"]["lot_info"]["date"],
            ),
            Text(
                text=f"{land_size}m²", **TEXT_DATA["digital"]["lot_info"]["land_size"]
            ),
            Text(
                text=f"{house_size}m²", **TEXT_DATA["digital"]["lot_info"]["house_size"]
            ),
            Text(text=f"{lot_width}m", **TEXT_DATA["digital"]["lot_info"]["lot_width"]),
            Text(
                text=convert_to_currency(land_price),
                **TEXT_DATA["digital"]["lot_info"]["land_price"],
            ),
            Text(
                text=convert_to_currency(house_price),
                **TEXT_DATA["digital"]["lot_info"]["house_price"],
            ),
            Text(
                text=convert_to_currency(price),
                **TEXT_DATA["digital"]["lot_info"]["package_price"],
            ),
            # Banner text
            Text(
                text="Package Price",
                **TEXT_DATA["digital"]["banner"]["label"],
            ),
            Text(
                text=convert_to_currency(price),
                **TEXT_DATA["digital"]["banner"]["price"],
            ),
            # Floorplan info
            Text(
                text=floorplan_model,
                **TEXT_DATA["digital"]["floorplan_info"]["floorplan_model"],
            ),
            Text(
                text=str(bedroom), **TEXT_DATA["digital"]["floorplan_info"]["bedrooms"]
            ),
            Text(
                text=str(bathroom),
                **TEXT_DATA["digital"]["floorplan_info"]["bathrooms"],
            ),
            Text(
                text=str(parking_slot),
                **TEXT_DATA["digital"]["floorplan_info"]["garages"],
            ),
        ]

        for text in digital_texts:
            empty_digital.add_text(text)

        empty_digital.pdf_file.save(digital_path)
        empty_digital.pdf_file.close()

        # Upload to Google Drive
        upload_or_replace_file(
            digital_file_name,
            digital_path,
            "application/pdf",
            parent_folder_id=TARGET_FOLDER_ID,
        )

        return {
            "digital_path": digital_path,
        }

    except Exception as e:
        logging.error(f"Error generating flyer: {str(e)}")
        raise

    finally:
        logging.warning("Cleaning up...")
        if os.path.exists(digital_path):
            os.remove(digital_path)
        logging.warning("Cleaned up, task complete")
