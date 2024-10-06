import os
import PyPDF2
from dotenv import load_dotenv
from celery import Celery
import fitz
import requests
from io import BytesIO
from text_utils import add_all_text_to_pdf
from image_utils import add_png_to_pdf, add_pdf_to_pdf_bottom_left
from reportlab.lib.pagesizes import A4
import dropbox
import datetime

load_dotenv(".env.local")

# Get Redis URL from environment or use default
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY", "")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET", "")
DROPBOX_REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN", "")

# Initialize Celery app
app = Celery("tasks", broker=redis_url, backend=redis_url)
dbx = dropbox.Dropbox(
    app_key=DROPBOX_APP_KEY,
    app_secret=DROPBOX_APP_SECRET,
    oauth2_refresh_token=DROPBOX_REFRESH_TOKEN,
)


@app.task
def generate_flyer(
    flyer_id,
    suburb,
    address,
    lot,
    price,
    land_size,
    house_size,
    lot_width,
    land_price,
    rego,
    facade,
    floorplan,
    facade_file_url,
    floorplan_file_url,
    bedroom,
    bathroom,
    parking_slot,
):
    print(f"Generating flyer: {flyer_id}")

    # Load the template PDF
    template_pdf = "./flyer/FlyerTemplate.pdf"
    temp_pdf = f"./flyer/temp_{flyer_id}.pdf"
    output_pdf = f"./flyer/flyer_{flyer_id}.pdf"

    # Create a new PDF document
    pdf_document = fitz.open(template_pdf)

    # Fetch the facade image from the URL
    facade_response = requests.get(facade_file_url)
    facade_image = BytesIO(facade_response.content)
    add_png_to_pdf(pdf_document, 0, facade_image)

    floorplan_response = requests.get(floorplan_file_url)
    floorplan_pdf = BytesIO(floorplan_response.content)
    add_pdf_to_pdf_bottom_left(pdf_document, floorplan_pdf, 0)

    pdf_document.save(temp_pdf)
    pdf_document.close()

    reader = PyPDF2.PdfReader(temp_pdf)
    writer = PyPDF2.PdfWriter()

    text_data = {
        "suburb": (suburb, 21, (11.2 / 210 * A4[0], 20.8 / 297 * A4[1]), "Inter-Bold"),
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
            f"{land_price}",
            10,
            (36.05 / 210 * A4[0], 88.76 / 297 * A4[1]),
            "Inter-Light",
        ),
        "rego": (rego, 10, (11.744 / 210 * A4[0], 108.0 / 297 * A4[1]), "Inter-Light"),
        "facade": (
            facade,
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

    upload_path = f"/flyer/flyer_{flyer_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

    with open(output_pdf, "rb") as f:
        dbx.files_upload(
            f.read(),
            upload_path,
        )

    print("Uploaded to Dropbox, cleaning up...")
    os.remove(temp_pdf)
    os.remove(output_pdf)

    print("Cleaned up, task complete")
    return upload_path
