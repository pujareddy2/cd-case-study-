from docx import Document

doc = Document('temp_converted.docx')
for i, p in enumerate(doc.paragraphs[:30]):
    if p.text.strip():
        print(f"[{i}] {p.text}")
