import os
import PyPDF2
from dotenv import load_dotenv
from celery import Celery
import fitz
import requests
from io import BytesIO
from text_utils import add_all_text_to_pdf
from image_utils import add_banner, add_facade, add_floorplan
from reportlab.lib.pagesizes import A4
import dropbox
import datetime
from helper import convert_to_currency, convert_to_syd_time

load_dotenv(".env.local")

# Get Redis URL from environment or use default
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY", "")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET", "")
DROPBOX_REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN", "")

# Initialize Celery app
app = Celery("tasks", broker=redis_url, backend=redis_url)
app.conf.broker_connection_retry_on_startup = True
dbx = dropbox.Dropbox(
    app_key=DROPBOX_APP_KEY,
    app_secret=DROPBOX_APP_SECRET,
    oauth2_refresh_token=DROPBOX_REFRESH_TOKEN,
)


@app.task
def generate_flyer(
    flyer_id,
    property_id,
    facade,
    floorplan,
    price,
    suburb,
    address,
    lot,
    land_price,
    land_size,
    house_size,
    lot_width,
    rego,
    bedroom,
    bathroom,
    parking_slot,
    facade_file_url,
    floorplan_file_url,
    generate,
):
    print(f"Generating flyer: {flyer_id}")
    template_pdf = "./flyer/FlyerTemplate.pdf"
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    temp_pdf = f"./flyer/temp_{flyer_id}_{now}.pdf"
    output_pdf = f"./flyer/{flyer_id}_{now}.pdf"

    try:
        # Load the template PDF
        template_pdf = "./flyer/7Star_FlyerTemplate.pdf"

        # Create a new PDF document
        pdf_document = fitz.open(template_pdf)

        # Fetch the facade image from the URL
        facade_response = requests.get(facade_file_url)
        facade_image = BytesIO(facade_response.content)
        add_facade(pdf_document, 0, facade_image)

        add_banner(pdf_document, 0, "./flyer/banner_new.png")

        floorplan_response = requests.get(floorplan_file_url)
        floorplan_pdf = BytesIO(floorplan_response.content)
        add_floorplan(pdf_document, floorplan_pdf, 0)

        pdf_document.save(temp_pdf)
        pdf_document.close()

        reader = PyPDF2.PdfReader(temp_pdf)
        writer = PyPDF2.PdfWriter()

        text_data = {
            "suburb": (
                suburb,
                21,
                (11.2 / 210 * A4[0], 20.8 / 297 * A4[1]),
                "Inter-Bold",
            ),
            "address": (
                address,
                12,
                (11.2 / 210 * A4[0], 28.9 / 297 * A4[1]),
                "Inter-Regular",
            ),
            "lot_number": (
                f"LOT {lot}",
                8,
                (22.64 / 210 * A4[0], 37.5 / 297 * A4[1]),
                "Inter-SemiBold",
                (1, 1, 1),
                "center",
            ),
            "package_price": (
                f"Package Price",
                16,
                (161 / 210 * A4[0], 17.30 / 297 * A4[1]),
                "Inter-Bold",
            ),
            "price": (
                convert_to_currency(price),
                16,
                (161 / 210 * A4[0], 24.30 / 297 * A4[1]),
                "Inter-Bold",
                # (0, 0, 0),
            ),
            "land_size": (
                f"{land_size}m²",
                10,
                (32.0 / 210 * A4[0], 53.30 / 297 * A4[1]),
                "Inter-Light",
            ),
            "house_size": (
                f"{house_size}m²",
                10,
                (35.0 / 210 * A4[0], 62.56 / 297 * A4[1]),
                "Inter-Light",
            ),
            "lot_width": (
                f"{lot_width}m",
                10,
                (41.45 / 210 * A4[0], 72.12 / 297 * A4[1]),
                "Inter-Light",
            ),
            "land_price": (
                convert_to_currency(land_price),
                10,
                (36.05 / 210 * A4[0], 88.76 / 297 * A4[1]),
                "Inter-Light",
            ),
            "rego": (
                convert_to_syd_time(rego),
                10,
                (11.744 / 210 * A4[0], 108.0 / 297 * A4[1]),
                "Inter-Light",
            ),
            "floorplan": (
                floorplan,
                14,
                (98.844 / 210 * A4[0], 119.0 / 297 * A4[1]),
                "Inter-Bold",
                (0, 0, 0),
                "center",
            ),
            "beds": (
                str(bedroom),
                12,
                (136.744 / 210 * A4[0], 119.3 / 297 * A4[1]),
                "Inter-Regular",
                (0, 0, 0),
            ),
            "baths": (
                str(bathroom),
                12,
                (165.744 / 210 * A4[0], 119.3 / 297 * A4[1]),
                "Inter-Regular",
                (0, 0, 0),
            ),
            "car_spaces": (
                str(parking_slot),
                12,
                (194.744 / 210 * A4[0], 119.3 / 297 * A4[1]),
                "Inter-Regular",
                (0, 0, 0),
            ),
        }
        add_all_text_to_pdf(writer, reader.pages[0], text_data)

        with open(output_pdf, "wb") as f_out:
            writer.write(f_out)

        print(f"Flyer generated: {output_pdf}")

        upload_path = f"/flyer/{flyer_id}_{now}.pdf"

        with open(output_pdf, "rb") as f:
            dbx.files_upload(
                f.read(),
                upload_path,
            )

        print("Uploaded to Dropbox")
        return upload_path

    except Exception as e:
        print(f"Error generating flyer: {str(e)}")
        raise

    finally:
        print("Cleaning up...")
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)
        if os.path.exists(output_pdf):
            os.remove(output_pdf)
        print("Cleaned up, task complete")
