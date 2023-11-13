import io

import PIL
import PyPDF2
import pytesseract
from PIL import Image

from image_processor import ImageProcessor


class PDFTextExtractor:
    def __init__(self, pdf_path=None, pdf_stream=None):
        self.pdf_path = pdf_path
        self.pdf_stream = pdf_stream
        self.image_processor = ImageProcessor()
        self.results = []

    def extract_text(self):

        if self.pdf_stream:
            rep = io.BytesIO(self.pdf_stream)
            pdf = PyPDF2.PdfReader(rep)
        else:
            pdf = PyPDF2.PdfReader(self.pdf_path)

        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]
            page_content = page.extract_text()
            if page_content:
                self.results.append({
                    "page_number": page_number + 1,
                    "method": "extract",
                    "content": page_content
                })
            else:
                page_content = pytesseract.image_to_string(PIL.Image.open(self.pdf_path), lang="lat")
                self.results.append(
                    {
                        "page_number": page_number + 1,
                        "method": "ocr",
                        "content": page_content
                    }
                )
        return self.results
