# import json
#
# from pdf_reader import PDFTextExtractor
#
# pdf_text_extractor = PDFTextExtractor("Introduction to Text Processing.pdf")
#
# results = pdf_text_extractor.extract_text()
#
# print(json.dumps(results, indent=2))


from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import UploadFile
from fastapi.params import File

from pydantic import BaseModel

from pdf_reader import PDFTextExtractor

app = FastAPI()


class PDFFile(BaseModel):
    file: UploadFile


@app.get("/")
async def read_root():
    return JSONResponse({"message": "I am alive"})


@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    pdf_text_extractor = PDFTextExtractor(pdf_stream=file.file)
    results = pdf_text_extractor.extract_text()
    return JSONResponse(results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

