from dataclasses import dataclass
from io import BytesIO
import fitz
from enum import Enum
import config as cfg
import os


class Font(Enum):
    INTER_LIGHT = ("Inter-Light", os.path.join(cfg.FONT_FOLDER, "Inter-Light.ttf"))
    INTER_REGULAR = ("Inter-Regular", os.path.join(cfg.FONT_FOLDER, "Inter-Regular.ttf"))
    INTER_BOLD = ("Inter-Bold", os.path.join(cfg.FONT_FOLDER, "Inter-Bold.ttf"))
    INTER_SEMIBOLD = ("Inter-SemiBold", os.path.join(cfg.FONT_FOLDER, "Inter-SemiBold.ttf"))

    def __init__(self, font_name: str, font_path: str):
        self.font_name = font_name
        self.font_path = font_path
        self.font_obj = fitz.Font(font_name, font_path)

    def get_font_name(self):
        return self.value[0]
    
    def get_font_path(self):
        return self.value[1]
    
    def get_font_obj(self):
        return self.font_obj
    


@dataclass
class Text:
    text: str
    size: int
    position: tuple[int, int]
    font: Font
    color: tuple[int, int, int]
    align: str = "left"


class Image(BytesIO):
    pass

@dataclass
class PDF:
    pdf_file: fitz.Document

    def insert_font(self, font: Font):
        for page in self.pdf_file:
            page.insert_font(font.get_font_name(), font.get_font_path())

    def add_image(self, image: Image, position: tuple[float, float] = (0, 0), page_number: int = 0, stretch: bool = False, image_size: tuple[float, float]|None = None):
        page = self.pdf_file[page_number]
        img = fitz.Pixmap(image.getvalue())
        
        if stretch:
            # Calculate the aspect ratio of the image
            aspect_ratio = img.width / img.height
            
            # Set the image width to match the page width
            img_width = page.rect.width
            img_height = img_width / aspect_ratio
        elif image_size:
            img_width = image_size[0]
            img_height = image_size[1]
        else:
            # Use the original image dimensions
            img_width = img.width
            img_height = img.height
        
        # Create the image rectangle
        img_rect = fitz.Rect(position[0], position[1], position[0] + img_width, position[1] + img_height)
        
        # Insert the image
        page.insert_image(img_rect, stream=image.getvalue())
        
        # Clean up
        img = None

    def add_text(self, text: Text, page_number: int = 0):
        page = self.pdf_file[page_number]
        # text_width = page.get_text_length(text.text, fontsize=text.size, fontname=text.font.get_font_name())
        font = text.font
        
        # Calculate the text width using fitz.get_text_length
        text_width = text.font.get_font_obj().text_length(text.text, text.size)
        
        # Adjust the x-coordinate based on the alignment
        x, y = text.position
        if text.align == "center":
            x = x - text_width / 2
        elif text.align == "right":
            x = x - text_width
        
        # Insert the text with the adjusted position
        page.insert_text(
            point=(x, y),
            text=text.text,
            fontsize=text.size,
            fontname=font.get_font_name(),
            color=text.color,
        )

    def add_pdf(self, pdf: "PDF", position: tuple[float, float] = (0, 0), size: tuple[float, float] | None = None, page_number: int = 0):
        page = self.pdf_file[page_number]
        rect = page.rect
        print(rect)

        # Calculate insert dimensions
        if size:
            insert_width, insert_height = size
        else:
            # Default to full width and height if size is not provided
            insert_width, insert_height = rect.width, rect.height

        # Calculate position
        x, y = position

        # Create the insert rectangle
        insert_rect = fitz.Rect(x, y, x + insert_width, y + insert_height)

        # Insert the PDF
        page.show_pdf_page(insert_rect, pdf.pdf_file, 0)
    




