from io import BytesIO
import fitz
from models import Image, PDF, Text, Font
from data import TEXT_DATA
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
    "https://drive.google.com/uc?id=1eULTx3pBUxaaW3UsA9Cnbf6RswiAcpMQ&export=download"
)
bedroom = 6
bathroom = 4
parking_slot = 2


pdf_document = fitz.open("./assets/Empty_Digital.pdf")
digital_pdf = PDF(pdf_document)

# register fonts
digital_pdf.insert_font(Font.INTER_LIGHT)
digital_pdf.insert_font(Font.INTER_REGULAR)
digital_pdf.insert_font(Font.INTER_BOLD)
digital_pdf.insert_font(Font.INTER_SEMIBOLD)


with (
    requests.Session() as session,
    open("./assets/banner.png", "rb") as banner_file,
    open("./assets/Empty_Digital.pdf", "rb") as empty_digital_file,
    open("./assets/Empty_Printable.pdf", "rb") as empty_printable_file,
    open("./assets/fc_names/urban1.png", "rb") as png_file,
):
    facade = Image(session.get(facade_file_url).content)
    floorplan = PDF(fitz.open(stream=BytesIO(session.get(floorplan_file_url).content)))
    banner = Image(banner_file.read())
    png_image = Image(png_file.read())
    empty_digital = PDF(fitz.open(empty_digital_file))
    empty_printable = PDF(fitz.open(empty_printable_file))
# To add an image without stretching (using original dimensions)
digital_pdf.add_image(facade, position=(0, 0), stretch=True)
digital_pdf.add_image(
    banner, position=(841.8900146484375 - 179.2, 44), image_size=(179.2, 56)
)
digital_pdf.add_pdf(
    floorplan,
    position=(35, 632),
    size=(175 / 297 * 841.8900146484375, 125 / 420 * 1190.550048828125),
)

# For digital PDF - Add before saving
# Calculate middle right position (adjust x_offset as needed)
page_width = 841.8900146484375
page_height = 1190.550048828125
image_width = 23.52
image_height = 6.34
image_width_pt = 23.52 * 2.8346  # ≈ 66.67 points
image_height_pt = 6.34 * 2.8346  # ≈ 17.98 points
x_pos = page_width - image_width_pt - 10
y_pos = 420

digital_pdf.add_image(
    png_image, position=(x_pos, y_pos), image_size=(image_width_pt, image_height_pt)
)

digital_texts = [
    # Lot info
    Text(text="Leppington", **TEXT_DATA["digital"]["lot_info"]["suburb"]),
    Text(text="16A Bannister Ave", **TEXT_DATA["digital"]["lot_info"]["address"]),
    Text(text="LOT 124", **TEXT_DATA["digital"]["lot_info"]["lot_number"]),
    Text(text="11 Oct 2024", **TEXT_DATA["digital"]["lot_info"]["date"]),
    Text(text="100m²", **TEXT_DATA["digital"]["lot_info"]["land_size"]),
    Text(text="100m²", **TEXT_DATA["digital"]["lot_info"]["house_size"]),
    Text(text="10m", **TEXT_DATA["digital"]["lot_info"]["lot_width"]),
    Text(text="$8,000,000", **TEXT_DATA["digital"]["lot_info"]["land_price"]),
    Text(text="$8,000,000", **TEXT_DATA["digital"]["lot_info"]["house_price"]),
    Text(text="$10,000,000", **TEXT_DATA["digital"]["lot_info"]["package_price"]),
    # Banner text
    Text(
        text="Package Price",
        **TEXT_DATA["digital"]["banner"]["label"],
    ),
    Text(
        text="$10,000,000",
        **TEXT_DATA["digital"]["banner"]["price"],
    ),
    # Floorplan info
    Text(
        text="PALM 21 ND",
        **TEXT_DATA["digital"]["floorplan_info"]["floorplan_model"],
    ),
    Text(
        text="3",
        **TEXT_DATA["digital"]["floorplan_info"]["bedrooms"],
    ),
    Text(
        text="3",
        **TEXT_DATA["digital"]["floorplan_info"]["bathrooms"],
    ),
    Text(
        text="3",
        **TEXT_DATA["digital"]["floorplan_info"]["garages"],
    ),
]

for text in digital_texts:
    digital_pdf.add_text(text)


digital_pdf.pdf_file.save("./flyer/Digital.pdf")
digital_pdf.pdf_file.close()


pdf_document = fitz.open("./assets/Empty_Printable.pdf")
printable_pdf = PDF(pdf_document)

printable_pdf.insert_font(Font.INTER_LIGHT)
printable_pdf.insert_font(Font.INTER_REGULAR)
printable_pdf.insert_font(Font.INTER_BOLD)
printable_pdf.insert_font(Font.INTER_SEMIBOLD)

# To add an image without stretching (using original dimensions)
printable_pdf.add_image(facade, position=(0, 0), stretch=True)
# printable_pdf.add_image(logo, position=(10, 10), image_size=(79, 15))
printable_pdf.add_image(
    banner, position=(841.8900146484375 - 179.2, 44), image_size=(179.2, 56)
)
printable_pdf.add_pdf(
    floorplan,
    position=(33, 47),
    size=(175 / 297 * 841.8900146484375, 125 / 420 * 1190.550048828125),
    page_number=1,
)

# For printable PDF - Add before saving
printable_pdf.add_image(
    png_image,
    position=(x_pos, y_pos),
    image_size=(image_width, image_height),
    page_number=0,  # Add to first page
)

printable_texts_1 = [
    Text(
        text="Leppington",
        **TEXT_DATA["print"]["lot_info"]["suburb"],
    ),
    Text(
        text="16A Bannister Ave",
        **TEXT_DATA["print"]["lot_info"]["address"],
    ),
    Text(
        text="LOT 124",
        **TEXT_DATA["print"]["lot_info"]["lot_number"],
    ),
    Text(
        text="11 Oct 2024",
        **TEXT_DATA["print"]["lot_info"]["date"],
    ),
    Text(
        text="100m²",
        **TEXT_DATA["print"]["lot_info"]["land_size"],
    ),
    Text(
        text="100m²",
        **TEXT_DATA["print"]["lot_info"]["house_size"],
    ),
    Text(
        text="10m",
        **TEXT_DATA["print"]["lot_info"]["lot_width"],
    ),
    Text(
        text="$8,000,000",
        **TEXT_DATA["print"]["lot_info"]["land_price"],
    ),
    Text(
        text="$8,000,000",
        **TEXT_DATA["print"]["lot_info"]["house_price"],
    ),
    Text(
        text="$10,000,000",
        **TEXT_DATA["print"]["lot_info"]["package_price"],
    ),
    Text(
        text="3",
        **TEXT_DATA["print"]["lot_info"]["bedrooms"],
    ),
    Text(
        text="3",
        **TEXT_DATA["print"]["lot_info"]["bathrooms"],
    ),
    Text(
        text="2",
        **TEXT_DATA["print"]["lot_info"]["garages"],
    ),
    # Banner text
    Text(
        text="Package Price",
        **TEXT_DATA["print"]["banner"]["label"],
    ),
    Text(
        text="$10,000,000",
        **TEXT_DATA["print"]["banner"]["price"],
    ),
]

for text in printable_texts_1:
    printable_pdf.add_text(text, 0)

printable_texts_2 = [
    Text(
        text="PALM 21 ND",
        **TEXT_DATA["print"]["floorplan_info"]["floorplan_model"],
    ),
    Text(
        text="3",
        **TEXT_DATA["print"]["floorplan_info"]["bedrooms"],
    ),
    Text(
        text="3",
        **TEXT_DATA["print"]["floorplan_info"]["bathrooms"],
    ),
    Text(
        text="3",
        **TEXT_DATA["print"]["floorplan_info"]["garages"],
    ),
]

for text in printable_texts_2:
    printable_pdf.add_text(text, 1)

printable_pdf.pdf_file.save("./flyer/Printable.pdf")
printable_pdf.pdf_file.close()
