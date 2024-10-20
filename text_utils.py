import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

# Register the Inter font
pdfmetrics.registerFont(TTFont("Inter-Light", "./fonts/Inter-Light.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Regular", "./fonts/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "./fonts/Inter-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-SemiBold", "./fonts/Inter-SemiBold.ttf"))


# Function to add text to existing PDF
def add_text_to_pdf(text, size, position, style, color=(1, 1, 1), align="left"):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    _, height = A4

    can.setFont(style, size)
    can.setFillColorRGB(color[0], color[1], color[2])

    text_width = can.stringWidth(text, style, size)
    if align == "center":
        x = position[0] - (text_width / 2)
    elif align == "right":
        x = position[0] - text_width
    else:  # left alignment
        x = position[0]

    can.drawString(x, height - position[1], text)

    can.save()
    packet.seek(0)
    new_pdf = PyPDF2.PdfReader(packet)
    return new_pdf.pages[0]


def add_all_text_to_pdf(writer, page, text_data):
    for _, data in text_data.items():
        page.merge_page(add_text_to_pdf(*data))
    writer.add_page(page)


# # Specify your input and output PDF files
# input_pdf = "./flyer/FlyerTemplate.pdf"
# output_pdf = "./flyer/modified_existing_v2.pdf"

# # Read the existing PDF
# reader = PyPDF2.PdfReader(input_pdf)
# writer = PyPDF2.PdfWriter()

# # Create overlays for each text addition
# suburb = add_text_to_pdf(
#     input_pdf,
#     "Austral",
#     21,
#     (11.2 / 210 * A4[0], 20.8 / 297 * A4[1]),
#     "Inter-Bold",
# )

# address = add_text_to_pdf(
#     input_pdf,
#     "10 Circinus St",
#     12,
#     (11.2 / 210 * A4[0], 28.9 / 297 * A4[1]),
#     "Inter-Regular",
# )

# char4 = 16.763
# char3 = char4 + 0.8
# char2 = char3 + 0.8
# char1 = char2 + 0.8

# lot_number = add_text_to_pdf(
#     input_pdf,
#     "LOT 566",
#     8,
#     (22.64 / 210 * A4[0], 37.5 / 297 * A4[1]),
#     "Inter-SemiBold",
#     align="center",
# )

# land_size = add_text_to_pdf(
#     input_pdf,
#     "100m²",
#     10,
#     (32.0 / 210 * A4[0], 53.30 / 297 * A4[1]),
#     "Inter-Light",
# )

# house_size = add_text_to_pdf(
#     input_pdf,
#     "100m²",
#     10,
#     (35.0 / 210 * A4[0], 62.56 / 297 * A4[1]),
#     "Inter-Light",
# )

# lot_width = add_text_to_pdf(
#     input_pdf,
#     "100m",
#     10,
#     (41.45 / 210 * A4[0], 72.12 / 297 * A4[1]),
#     "Inter-Light",
# )

# land_price = add_text_to_pdf(
#     input_pdf,
#     "$1,000,000",
#     10,
#     (36.05 / 210 * A4[0], 88.76 / 297 * A4[1]),
#     "Inter-Light",
# )

# rego = add_text_to_pdf(
#     input_pdf,
#     "Registered",
#     10,
#     (11.744 / 210 * A4[0], 108.0 / 297 * A4[1]),
#     "Inter-Light",
# )

# facade = add_text_to_pdf(
#     input_pdf,
#     "PALM 21 ND",
#     14,
#     (98.844 / 210 * A4[0], 119.0 / 297 * A4[1]),
#     "Inter-Bold",
#     color=(0, 0, 0),
#     align="center",
# )

# beds = add_text_to_pdf(
#     input_pdf,
#     "6",
#     12,
#     (136.744 / 210 * A4[0], 119.3 / 297 * A4[1]),
#     "Inter-Regular",
#     color=(0, 0, 0),
# )

# baths = add_text_to_pdf(
#     input_pdf,
#     "4",
#     12,
#     (165.744 / 210 * A4[0], 119.3 / 297 * A4[1]),
#     "Inter-Regular",
#     color=(0, 0, 0),
# )

# car_spaces = add_text_to_pdf(
#     input_pdf,
#     "2",
#     12,
#     (194.744 / 210 * A4[0], 119.3 / 297 * A4[1]),
#     "Inter-Regular",
#     color=(0, 0, 0),
# )


# # Add all overlays to each page of the original PDF
# for i in range(len(reader.pages)):
#     page = reader.pages[i]
#     page.merge_page(suburb)
#     page.merge_page(address)
#     page.merge_page(lot_number)
#     page.merge_page(land_size)
#     page.merge_page(house_size)
#     page.merge_page(lot_width)
#     page.merge_page(land_price)
#     page.merge_page(rego)
#     page.merge_page(facade)
#     page.merge_page(beds)
#     page.merge_page(baths)
#     page.merge_page(car_spaces)
#     writer.add_page(page)

# # Write the result to the output PDF
# with open(output_pdf, "wb") as f_out:
#     writer.write(f_out
