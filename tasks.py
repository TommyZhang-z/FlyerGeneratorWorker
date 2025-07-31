from io import BytesIO
import os
from dotenv import load_dotenv
from celery import Celery
from data import TEXT_DATA as TEXT_DATA_DICT
from models import PDF, Font, Image, Text
import dropbox
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
    template_name="SEVENSTAR",
):
    logging.info(f"generating flyer [#{flyer_id}] ...")
    facade_name = facade
    digital_file_name = f"{flyer_id}.pdf"

    digital_path = os.path.join(cfg.DIGITAL_DIR, digital_file_name)
    EMPTY_PATH = os.path.join(cfg.ASSETS_DIR, f"{template_name}.pdf")
    template_data = TEXT_DATA_DICT[template_name]

    try:
        with (
            requests.Session() as session,
            open(BANNER_PATH, "rb") as banner_file,
            open(EMPTY_PATH, "rb") as empty_template_file,
        ):
            facade = Image(session.get(facade_file_url).content)
            floorplan = PDF(
                fitz.open(stream=BytesIO(session.get(floorplan_file_url).content))
            )
            banner = Image(banner_file.read())
            empty_template = PDF(fitz.open(empty_template_file))
            # empty_printable = PDF(fitz.open(empty_printable_file))
            # png_image = Image(png_file.read())
        empty_template.insert_font(Font.INTER_LIGHT)
        empty_template.insert_font(Font.INTER_REGULAR)
        empty_template.insert_font(Font.INTER_BOLD)
        empty_template.insert_font(Font.INTER_SEMIBOLD)

        empty_template.add_image(facade, position=(0, 0), stretch=True)
        empty_template.add_image(
            banner, position=(841.8900146484375 - 179.2, 44), image_size=(179.2, 56)
        )
        empty_template.add_pdf(
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

        if os.path.exists(
            os.path.join(cfg.ASSETS_DIR, "fc_names", f"{facade_name}.png")
        ):
            with open(
                os.path.join(cfg.ASSETS_DIR, "fc_names", f"{facade_name}.png"), "rb"
            ) as png_file:
                png_image = Image(png_file.read())
                empty_template.add_image(
                    png_image,
                    position=(x_pos, y_pos),
                    image_size=(image_width_pt, image_height_pt),
                )

        digital_texts = [
            # Lot info
            Text(text=suburb, **template_data["digital"]["lot_info"]["suburb"]),
            Text(text=address, **template_data["digital"]["lot_info"]["address"]),
            Text(
                text=f"LOT {lot}", **template_data["digital"]["lot_info"]["lot_number"]
            ),
            Text(
                text=convert_to_syd_time(rego),
                **template_data["digital"]["lot_info"]["date"],
            ),
            Text(
                text=f"{land_size}m²",
                **template_data["digital"]["lot_info"]["land_size"],
            ),
            Text(
                text=f"{house_size}m²",
                **template_data["digital"]["lot_info"]["house_size"],
            ),
            Text(
                text=f"{lot_width}m",
                **template_data["digital"]["lot_info"]["lot_width"],
            ),
            Text(
                text=convert_to_currency(land_price),
                **template_data["digital"]["lot_info"]["land_price"],
            ),
            Text(
                text=convert_to_currency(house_price),
                **template_data["digital"]["lot_info"]["house_price"],
            ),
            Text(
                text=convert_to_currency(price),
                **template_data["digital"]["lot_info"]["package_price"],
            ),
            # Banner text
            Text(
                text="Package Price",
                **template_data["digital"]["banner"]["label"],
            ),
            Text(
                text=convert_to_currency(price),
                **template_data["digital"]["banner"]["price"],
            ),
            # Floorplan info
            Text(
                text=floorplan_model,
                **template_data["digital"]["floorplan_info"]["floorplan_model"],
            ),
            Text(
                text=str(bedroom),
                **template_data["digital"]["floorplan_info"]["bedrooms"],
            ),
            Text(
                text=str(bathroom),
                **template_data["digital"]["floorplan_info"]["bathrooms"],
            ),
            Text(
                text=str(parking_slot),
                **template_data["digital"]["floorplan_info"]["garages"],
            ),
        ]

        for text in digital_texts:
            empty_template.add_text(text)

        empty_template.pdf_file.save(digital_path)
        empty_template.pdf_file.close()

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
