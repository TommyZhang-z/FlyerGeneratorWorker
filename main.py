from io import BytesIO
import fitz
from helper import convert_to_currency, convert_to_syd_time
from image_utils import add_facade
from models import Image, PDF, Text, Font
import config as cfg

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


pdf_document = fitz.open("./flyer/Empty_Screen.pdf")
digital_pdf = PDF(pdf_document)

# register fonts
digital_pdf.insert_font(Font.INTER_LIGHT)
digital_pdf.insert_font(Font.INTER_REGULAR)
digital_pdf.insert_font(Font.INTER_BOLD)
digital_pdf.insert_font(Font.INTER_SEMIBOLD)


with open("./flyer/facade.png", "rb") as facade_file, open("./flyer/banner.png", "rb") as banner_file, open("./flyer/fp.pdf", "rb") as fp_file, open("./flyer/logo.png", "rb") as logo_file:
    facade = Image(facade_file.read())
    banner = Image(banner_file.read())
    logo = Image(logo_file.read())
    fp = PDF(fitz.open(fp_file))

# To add an image without stretching (using original dimensions)
digital_pdf.add_image(facade, position=(0, 0), stretch=True)
digital_pdf.add_image(banner, position=(841.8900146484375-179.2, 44), image_size=(179.2, 56))
digital_pdf.add_pdf(fp, position=(35, 632), size=(175/297*841.8900146484375, 125/420*1190.550048828125))

digital_texts = [
    # Lot info
    Text(text="Leppington", size=27, position=(58.88, 513.90), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="16A Bannister Ave", size=14, position=(60.5, 541.3), font=Font.INTER_REGULAR, color=(1, 1, 1)),
    Text(text="LOT 124", size=9, position=(300.5, 503), font=Font.INTER_SEMIBOLD, color=(1, 1, 1), align="center"),
    Text(text="11 Oct 2024", size=10, position=(267, 544), font=Font.INTER_LIGHT, color=(1, 1, 1)),
    Text(text="100m²", size=10, position=(499, 500.3), font=Font.INTER_BOLD, color=(1, 1, 1)),
    # Text(text="100m²", size=10, position=(510, 500.3), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="100m²", size=10, position=(510, 522.9), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="10m", size=10, position=(502.4, 545.2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    # Text(text="10m", size=10, position=(510, 545.2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="$8,000,000", size=10, position=(698, 500.0), font=Font.INTER_BOLD, color=(1, 1, 1)),
    # Text(text="$8,000,000", size=10, position=(714.2, 500.0), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="$8,000,000", size=10, position=(704.3, 522.4), font=Font.INTER_BOLD, color=(1, 1, 1)),
    # Text(text="$8,000,000", size=10, position=(714.2, 522.4), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="$10,000,000", size=10, position=(714.2, 545.0), font=Font.INTER_BOLD, color=(1, 1, 1)),

    # Banner text
    Text(text="Package Price", size=17, position=(841.8900146484375-179.2+38, 67.2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="$10,000,000", size=17, position=(841.8900146484375-179.2+38, 88.0), font=Font.INTER_BOLD, color=(1, 1, 1)),

    # Floorplan info
    Text(text="PALM 21 ND", size=15, position=(589.5, 675.7), font=Font.INTER_BOLD, color=(0, 0, 0)),
    Text(text="3", size=13, position=(617.8, 719.4), font=Font.INTER_REGULAR, color=(0, 0, 0)),
    Text(text="3", size=13, position=(702.55, 719.4), font=Font.INTER_REGULAR, color=(0, 0, 0)),
    Text(text="3", size=13, position=(786.9, 719.4), font=Font.INTER_REGULAR, color=(0, 0, 0)),
]

for text in digital_texts:
    digital_pdf.add_text(text)


digital_pdf.pdf_file.save("./flyer/Digital.pdf")
digital_pdf.pdf_file.close()


pdf_document = fitz.open("./flyer/Empty_Print.pdf")
printable_pdf = PDF(pdf_document)

printable_pdf.insert_font(Font.INTER_LIGHT)
printable_pdf.insert_font(Font.INTER_REGULAR)
printable_pdf.insert_font(Font.INTER_BOLD)
printable_pdf.insert_font(Font.INTER_SEMIBOLD)

# To add an image without stretching (using original dimensions)
printable_pdf.add_image(facade, position=(0, 0), stretch=True)
printable_pdf.add_image(logo, position=(10, 10), image_size=(79/2, 15/2))
printable_pdf.add_image(banner, position=(841.8900146484375-179.2, 44), image_size=(179.2, 56))
printable_pdf.add_pdf(fp, position=(35, 47), size=(175/297*841.8900146484375, 125/420*1190.550048828125), page_number=1)


printable_texts_1 = [
    Text(text="Leppington", size=27, position=(37.14, 513.90-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="16A Bannister Ave", size=14, position=(38.16, 541.3-2), font=Font.INTER_REGULAR, color=(1, 1, 1)),
    Text(text="LOT 124", size=9, position=(300.5-38, 503-2), font=Font.INTER_SEMIBOLD, color=(1, 1, 1), align="center"),
    Text(text="11 Oct 2024", size=10, position=(267-38, 544-2), font=Font.INTER_LIGHT, color=(1, 1, 1)),
    Text(text="100m²", size=10, position=(499-63.80, 500.3-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    # Text(text="100m²", size=10, position=(510-63.80, 500.3-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="100m²", size=10, position=(510-63.80, 522.9-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="10m", size=10, position=(502.4-63.80, 545.2-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    # Text(text="10m", size=10, position=(510-63.80, 545.2-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="$8,000,000", size=10, position=(698-115.8, 500.0-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    # Text(text="$8,000,000", size=10, position=(714.2-115.8, 500.0-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="$8,000,000", size=10, position=(704.3-115.8, 522.4-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    # Text(text="$8,000,000", size=10, position=(714.2-115.8, 522.4-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="$10,000,000", size=10, position=(714.2-115.8, 545.0-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="3", size=10, position=(780.2-2, 500.0-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="3", size=10, position=(780.2, 523.4-2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="2", size=10, position=(780.2-9, 545.5-2), font=Font.INTER_BOLD, color=(1, 1, 1)),

    # Banner text
    Text(text="Package Price", size=17, position=(841.8900146484375-179.2+38, 67.2), font=Font.INTER_BOLD, color=(1, 1, 1)),
    Text(text="$10,000,000", size=17, position=(841.8900146484375-179.2+38, 88.0), font=Font.INTER_BOLD, color=(1, 1, 1)),
]

for text in printable_texts_1:
    printable_pdf.add_text(text, 0)

printable_texts_2 = [
    Text(text="PALM 21 ND", size=15, position=(589.5, 675.7), font=Font.INTER_BOLD, color=(0, 0, 0)),
    Text(text="3", size=13, position=(617.8, 719.4), font=Font.INTER_REGULAR, color=(0, 0, 0)),
    Text(text="3", size=13, position=(702.55, 719.4), font=Font.INTER_REGULAR, color=(0, 0, 0)),
    Text(text="3", size=13, position=(786.9, 719.4), font=Font.INTER_REGULAR, color=(0, 0, 0)),
]

for text in printable_texts_2:
    printable_pdf.add_text(text, 1)

printable_pdf.pdf_file.save("./flyer/Printable.pdf")
printable_pdf.pdf_file.close()
