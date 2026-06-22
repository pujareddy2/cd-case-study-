from pdf2docx import Converter

pdf_file = "Cd case study chapter 2.pdf"
docx_file = "Converted_Case_Study.docx"

cv = Converter(pdf_file)
cv.convert(docx_file)
cv.close()
print("Conversion completed.")
