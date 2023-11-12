import json

from pdf_reader import PDFTextExtractor

pdf_text_extractor = PDFTextExtractor("Introduction to Text Processing.pdf")

results = pdf_text_extractor.extract_text()

print(json.dumps(results, indent=2))