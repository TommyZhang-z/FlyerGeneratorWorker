import fitz
from io import BytesIO


def add_facade(pdf_document, page_number, png_file):
    page = pdf_document[page_number]
    page_rect = page.rect

    image_width = 139 / 210 * page_rect.width
    image_height = 110 / 297 * page_rect.height

    x1 = page_rect.width - image_width
    y1 = 0
    x2 = page_rect.width
    y2 = image_height

    page.insert_image(
        fitz.Rect(x1, y1, x2, y2),
        stream=png_file,
    )


def add_floorplan(target_pdf, source_pdf, page_number):
    source_doc = fitz.open(stream=source_pdf)
    target_page = target_pdf[page_number]
    target_rect = target_page.rect

    insert_width = 89 / 210 * target_rect.width
    insert_height = 172 / 297 * target_rect.height

    insert_rect = fitz.Rect(
        0, target_rect.height - insert_height, insert_width, target_rect.height
    )

    target_page.show_pdf_page(insert_rect, source_doc, 0)
    source_doc.close()


def add_banner(pdf_document, page_number, png_file):
    page = pdf_document[page_number]
    page_rect = page.rect

    image_width = 61.8 / 210 * page_rect.width
    image_height = 21.3 / 297 * page_rect.height

    x1 = page_rect.width - image_width
    # Position the banner 20 units from the bottom (in 297-unit scale)
    y1 = page_rect.height - image_height - (267.5 / 297 * page_rect.height)
    x2 = page_rect.width
    y2 = y1 + image_height

    page.insert_image(
        fitz.Rect(x1, y1, x2, y2),
        filename=png_file,
    )
