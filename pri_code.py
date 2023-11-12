import fitz
from PIL import Image
import pytesseract

class PDFTextExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text_from_pdf(self):
        doc = fitz.open(self.pdf_path)

        for page_number in range(doc.page_count):
            page = doc[page_number]
            if page.get_text("text"):
                text = page.get_text("text")
                print(f"Text from Page {page_number + 1}:\n{text}")
            else:
                image = page.get_pixmap()
                image_path = f"page_{page_number + 1}.jpeg"
                self.save_image(image, image_path)
                ocr_text = self.perform_ocr(image_path)
                print(f"OCR Text from Page {page_number + 1}:\n{ocr_text}")

    def save_image(self, pixmap, image_path):
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        image.save(image_path)

    def perform_ocr(self, image_path):
        image = Image.open(image_path)
        ocr_text = pytesseract.image_to_string(image)
        return ocr_text

if __name__ == "__main__":
    pdf_extractor = PDFTextExtractor("Introduction to Text Processing.pdf")
    pdf_extractor.extract_text_from_pdf()
