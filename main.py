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
    # requests.Session() as session,
    open("./assets/LOT401.pdf", "rb") as flyer,
    # open("./assets/Empty_Digital.pdf", "rb") as empty_digital_file,
    # open("./assets/Empty_Printable.pdf", "rb") as empty_printable_file,
    open("./assets/fc_names/Urban I.png", "rb") as png_file,
):
    # facade = Image(session.get(facade_file_url).content)
    # floorplan = PDF(fitz.open(stream=BytesIO(session.get(floorplan_file_url).content)))
    # banner = Image(banner_file.read())
    png_image = Image(png_file.read())
    empty_flyer = PDF(fitz.open(flyer))

page_width = 595.2760009765625
page_height = 841.8900146484375
image_width = 23.52
image_height = 6.34
image_width_pt = image_width * 2.8346  # ≈ 66.67 points
image_height_pt = image_height * 2.8346  # ≈ 17.98 points
x_pos = page_width - image_width_pt - 20
y_pos = 350

empty_flyer.add_image(
    png_image,
    position=(x_pos, y_pos),
    image_size=(image_width_pt, image_height_pt),
)

empty_flyer.pdf_file.save("./assets/LOT401_test.pdf")
empty_flyer.pdf_file.close()
