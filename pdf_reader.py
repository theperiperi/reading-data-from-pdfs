import json

import fitz
from PIL import Image
import pytesseract

import numpy as np
import PIL

from image_processor import ImageProcessor


class PDFTextExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.image_processor = ImageProcessor()
        self.results = []

    def extract_text(self):
        doc = fitz.open(self.pdf_path)
        self.results = []
        for page_number in range(doc.page_count):
            page = doc[page_number]
            if page.get_text("text"):
                text = page.get_text("text")
                self.results.append({
                    "page_number": page_number + 1,
                    "method": "extract",
                    "content": text
                })
            else:
                pixmap = page.get_pixmap()
                image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
                ocr_text = self.image_processor.ocr_image(np.array(image))
                self.results.append({
                    "page_number": page_number + 1,
                    "method": "ocr",
                    "content": ocr_text
                })
        return self.results
