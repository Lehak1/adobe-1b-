# Approach Explanation

## Objective
The goal of this solution is to extract and prioritize relevant sections from a collection of PDFs based on a specific persona and job-to-be-done, all while adhering to strict resource constraints: CPU-only execution, ≤1GB model size, ≤60 seconds processing time, and no internet access during inference.

---

## 1. PDF Parsing and Section Detection
We use `pdfminer.six` to parse PDF content. It allows fine-grained access to page-wise structured text. Using heuristics such as font size, spacing, and indentation, we extract potential section headings (e.g., H1, H2, H3) and associate them with their page numbers. This allows a basic document structure tree to be created.

---

## 2. Section Embedding and Relevance Scoring
To match sections to the user's intent, we generate vector embeddings using a compact sentence-transformer model (`paraphrase-MiniLM-L6-v2`), which is lightweight and effective. Each section's heading and content is embedded and compared against the combined persona + job description text via cosine similarity. The top N most relevant sections are selected based on similarity scores.

---

## 3. Text Refinement
For each top section, we generate a concise summary using extractive summarization. We tokenize the section into sentences and rank them using similarity to the section heading and job context, ensuring the result captures core meaning without requiring a large generative model.

---

## 4. Output Formatting
The final output is structured into:
- **Metadata**: input PDFs, persona, job description, and timestamp.
- **Top Sections**: section title, page number, importance rank.
- **Subsection Summaries**: summaries of key sections for quick review.

---

## 5. Resource-Conscious Implementation
- All operations are run locally on CPU.
- The model is under 100MB.
- Multi-threaded but synchronous processing avoids memory spikes.
- Total processing time for 3–5 PDFs is under 60 seconds.

---

## Advantages
- Works offline (ideal for air-gapped environments)
- Supports batch processing of document collections
- Prioritizes task-specific relevance via semantic matching

---

## Limitations & Next Steps
- Heading detection relies on formatting consistency
- Extractive summaries may miss deep contextual insight
- Future improvements could integrate layout-aware models or fine-tuned transformers if resources permit

---

## Conclusion
This solution balances performance, accuracy, and resource limits to enable intelligent document understanding for a defined user context.
