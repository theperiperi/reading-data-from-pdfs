import os
from typing import Any

import pytesseract
from PIL import Image
import numpy as np
import cv2
import re


class ImageProcessor:
    def __init__(self, exec_path: str = None, tessdata_path: str = None):
        self.exec_path = exec_path
        self.tessdata_path = tessdata_path
        if exec_path:
            pytesseract.pytesseract.tesseract_cmd = exec_path
        if tessdata_path:
            os.environ["TESSDATA_PREFIX"] = tessdata_path
            pytesseract.pytesseract.tessdata_path = tessdata_path

    def read_image(self, file_path) -> np.array:
        img_to_ocr = Image.open(file_path)
        return np.array(img_to_ocr)

    def preprocess_image(self, img_to_ocr: np.array) -> np.array:
        norm_img = np.zeros((img_to_ocr.shape[0], img_to_ocr.shape[1]))
        img_to_ocr = cv2.normalize(img_to_ocr, norm_img, 0, 255, cv2.NORM_MINMAX)
        img_to_ocr = cv2.threshold(img_to_ocr, 100, 255, cv2.THRESH_BINARY)[1]
        img_to_ocr = cv2.GaussianBlur(img_to_ocr, (1, 1), 0)
        return img_to_ocr

    def ocr_image(self, img_to_ocr: np.array, lang: str = None) -> str:
        # preprocessed = self.preprocess_image(img_to_ocr)
        preprocessed = img_to_ocr
        if lang is None:
            detected = self.detect_lang(preprocessed)
            lang = detected.get("script", "eng")
        f"Script Detected: {lang}"
        return pytesseract.image_to_string(img_to_ocr, lang="eng")

    def detect_lang(self, image_to_ocr: np.array) -> dict[str, Any]:
        lang = pytesseract.image_to_osd(image_to_ocr)
        script_regex = r"(?<=Script:\s)(.*)(?=\n)"
        script_confidence_regex = r"(?<=Script confidence:\s)(.*)(?=\n)?"
        orientation_regex = r"(?<=Orientation in degrees:\s)(.*)(?=\n)?"
        orientation_confidence_regex = r"(?<=Orientation confidence:\s)(.*)(?=\n)?"
        script = re.search(script_regex, lang).group(0)
        script_confidence = re.search(script_confidence_regex, lang).group(0)
        orientation = re.search(orientation_regex, lang).group(0)
        orientation_confidence = re.search(orientation_confidence_regex, lang).group(0)
        return {
            "script": script,
            "script_confidence": script_confidence,
            "orientation": orientation,
            "orientation_confidence": orientation_confidence
        }
