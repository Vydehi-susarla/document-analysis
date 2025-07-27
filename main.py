import os
import json
from datetime import datetime
from utils import extract_text_from_pdfs, extract_sections
from analyzer import rank_sections, refine_subsections

def main():
    with open("input.json", "r") as f:
        config = json.load(f)

    persona = config["persona"]
    job_to_be_done = config["job_to_be_done"]
    pdf_files = config["pdfs"]

    all_sections = []
    full_text_map = {}

    for file in pdf_files:
        pages = extract_text_from_pdfs("pdfs", [file])[file]
        full_text_map[file] = "\n".join(p["text"] for p in pages)

        sections = extract_sections(pages, file)
        all_sections.extend(sections)

    if not all_sections:
        print("⚠️ No sections extracted from any documents.")
        return

    ranked = rank_sections(all_sections, persona, job_to_be_done)
    top_sections = ranked[:7]

    refined = refine_subsections(top_sections, persona, job_to_be_done)

    output = {
        "metadata": {
            "input_documents": pdf_files,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "section_title": sec["section_title"],
                "importance_rank": idx + 1,
                "page_number": sec.get("page_number", -1),
                "content": sec["content"]
            }
            for idx, sec in enumerate(top_sections)
        ],
        "subsection_analysis": refined
    }

    os.makedirs("output", exist_ok=True)
    with open("output/output.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
