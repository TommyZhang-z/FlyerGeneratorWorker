from io import BytesIO
import PyPDF2
import fitz
from image_utils import add_facade, add_floorplan, add_banner
from text_utils import add_all_text_to_pdf
from helper import convert_to_currency, convert_to_syd_time
from reportlab.lib.pagesizes import A4
import requests

# Test variables
flyer_id = "TEST002"
suburb = "Austral"
address = "10 Circinus St"
lot = "565"
price = 750000
land_size = 100
house_size = 100
lot_width = 100
land_price = 500000
rego = "Registered"
facade = "OCEAN I"
floorplan = "PALM 21 ND"
facade_file_url = (
    "https://drive.google.com/uc?id=10T_oSsXE3zw_e6np0Z9jKd9atwBytfQ4&export=download"
)
floorplan_file_url = (
    "https://drive.google.com/uc?export=download&id=1QU6PpSOG-KODKFaGoOdCnJMoiH4fXGbH"
)
bedroom = 6
bathroom = 4
parking_slot = 2

# template_pdf = "./flyer/FlyerTemplate.pdf"
template_pdf = "./flyer/7Star_FlyerTemplate.pdf"
pdf_document = fitz.open(template_pdf)

# Fetch the facade image from the URL
facade_response = requests.get(facade_file_url)
facade_image = BytesIO(facade_response.content)
add_facade(pdf_document, 0, facade_image)


add_banner(pdf_document, 0, "./flyer/banner_new.png")
floorplan_response = requests.get(floorplan_file_url)
floorplan_pdf = BytesIO(floorplan_response.content)
add_floorplan(pdf_document, floorplan_pdf, 0)

# pdf_document.save("./flyer/test.pdf")
pdf_document.save("./flyer/7Star_FlyerTemplate_WithBanner.pdf")
pdf_document.close()


reader = PyPDF2.PdfReader("./flyer/7Star_FlyerTemplate_WithBanner.pdf")
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
with open("./flyer/test01.pdf", "wb") as f_out:
    writer.write(f_out)
