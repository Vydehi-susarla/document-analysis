import os
import fitz  # PyMuPDF

def extract_text_from_pdfs(pdf_dir, pdf_files):
    pdf_pages = {}
    for pdf in pdf_files:
        path = os.path.join(pdf_dir, pdf)
        if not os.path.exists(path):
            continue
        doc = fitz.open(path)
        pages = []
        for i, page in enumerate(doc):
            pages.append({
                "page_number": i + 1,
                "text": page.get_text()
            })
        pdf_pages[pdf] = pages
    return pdf_pages

def extract_sections(pages, filename):
    sections = []
    current_title = "Introduction"
    current_content = []
    current_page_number = pages[0]["page_number"] if pages else 1

    for page in pages:
        lines = page["text"].split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.istitle() or line.isupper():
                if current_content:
                    sections.append({
                        "document": filename,
                        "section_title": current_title,
                        "content": "\n".join(current_content).strip(),
                        "page_number": current_page_number
                    })
                current_title = line
                current_content = []
                current_page_number = page["page_number"]
            else:
                current_content.append(line)

    if current_content:
        sections.append({
            "document": filename,
            "section_title": current_title,
            "content": "\n".join(current_content).strip(),
            "page_number": current_page_number
        })

    return sections
