import json
import os
from datetime import datetime
from utils.pdf_parser import parse_pdf
from utils.embedding import get_top_k_sections
from utils.summarizer import refine_section_text

INPUT_PATH = "sample_input.json"
OUTPUT_PATH = "sample_output.json"
DOCUMENTS_DIR = "documents"
K = 5  # number of top sections to extract

def main():
    # Step 1: Load input JSON
    with open(INPUT_PATH, 'r') as f:
        data = json.load(f)

    documents = data['documents']
    persona = data['persona']['role']
    job = data['job_to_be_done']['task']

    # Step 2: Parse all documents into sections
    all_sections = []
    for doc in documents:
        filename = doc['filename']
        title = doc['title']
        filepath = os.path.join(DOCUMENTS_DIR, filename)

        sections = parse_pdf(filepath)
        for section in sections:
            section['document'] = filename
            section['title'] = title
        all_sections.extend(sections)

    # Step 3: Rank top-k sections using updated get_top_k_sections
    query = f"{persona}: {job}"
    top_sections = get_top_k_sections(query, all_sections, k=K)

    # Step 4: Refine selected sections' text
    refined_sections = []
    for sec in top_sections:
        refined = refine_section_text(sec['content'])
        refined_sections.append({
            "document": sec['document'],
            "refined_text": refined,
            "page_number": sec['page_number']
        })

    # Step 5: Prepare output
    output = {
        "metadata": {
            "input_documents": [doc['filename'] for doc in documents],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": [
            {
                "document": sec['document'],
                "page_number": sec['page_number'],
                "section_title": sec['title'],
                "importance_rank": rank + 1
            }
            for rank, sec in enumerate(top_sections)
        ],
        "subsection_analysis": refined_sections
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=4)

    print(f"✅ Processing complete. Output saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
