import os
from pdf2docx import Converter

pdf_path = "CD case study chapter 3.pdf"
docx_path = "temp_converted.docx"

if os.path.exists(pdf_path):
    print("Converting PDF to DOCX...")
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()
    print("Conversion complete.")
else:
    print("PDF not found!")
