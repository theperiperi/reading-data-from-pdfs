from image_reader import ImageProcessor
from PIL import Image
import numpy as np

reader = ImageProcessor("tesseract", "/usr/local/Cellar/tesseract/5.3.3/share/tessdata")
text = reader.ocr_image(np.array(Image.open("screenshot.jpeg")))
print(text)