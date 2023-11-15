from typing import Annotated

from fastapi import FastAPI
from fastapi.params import File
from fastapi.responses import JSONResponse

from pdf_reader import PDFTextExtractor

app = FastAPI()


@app.get("/")
async def read_root():
    return JSONResponse({"message": "I am alive"})


@app.post("/extract-text")
async def extract_text(file: Annotated[bytes, File()]):
    pdf_text_extractor = PDFTextExtractor(pdf_stream=file)
    results = pdf_text_extractor.extract_text()
    return JSONResponse(results)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
