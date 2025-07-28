# 📄 Intelligent Document Section Extractor

This project extracts and prioritizes relevant sections from PDFs based on a defined **persona** and **job-to-be-done**. It processes multiple PDFs offline and outputs a clean, structured JSON format. Ideal for intelligent document understanding, search indexing, and summarization tasks.

---

## 🚀 Features

- ✅ **Extracts Title & Hierarchical Headings** (H1, H2, H3)
- ✅ **Filters Relevant Sections** based on persona + task
- ✅ **Summarizes Sections** using transformer-based models
- ✅ **Fully Offline** execution (no internet or GPU needed)
- ✅ **Dockerized** (for AMD64 CPUs, portable)
- ✅ Processes **multiple PDFs** in one go

---

## 🧱 Project Structure

```
.
├── main.py                      # Pipeline entry point
├── sample_input.json           # Input JSON: PDF paths + persona/task
├── output.json                 # Final output JSON
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Offline build environment
├── README.md                   # Project documentation
└── utils/
    ├── pdf_parser.py           # Extracts title and section headings
    ├── filter.py               # Filters sections based on relevance
    ├── summarizer.py           # Summarizes selected sections
```

---

## 📥 Sample Input (sample_input.json)

```json
{
  "persona": "Product Manager",
  "task": "Wants to understand how the product roadmap is structured",
  "pdf_paths": ["docs/product_strategy.pdf", "docs/internal_roadmap.pdf"]
}
```

---

## 📤 Output Format (output.json)

```json
{
  "docs/product_strategy.pdf": [
    {
      "heading": "Product Roadmap Overview",
      "page": 5,
      "content": "Summarized or filtered content based on the persona and task..."
    },
    ...
  ]
}
```

---

## 🐳 Run with Docker

### Step 1: Build the Docker image

```bash
docker build -t pdf-extractor .
```

### Step 2: Run the extractor

```bash
docker run --rm -v $(pwd):/app pdf-extractor
```

> This mounts your current directory inside the container to read input and write output.

---

## 🛠️ Tech Stack

| Library               | Purpose                          |
|----------------------|----------------------------------|
| **pdfplumber==0.10.2**         | Extracts text + structured layout from PDF |
| **PyMuPDF==1.23.4**            | Fine-grained PDF parsing (e.g., fonts, layout) |
| **sentence-transformers==2.2.2** | Semantic similarity & summaries |
| **scikit-learn==1.3.2**        | Cosine similarity, preprocessing |
| **nltk==3.8.1**                | Tokenization, text cleaning |
| **numpy==1.26.4**              | Numerical operations |
| **pandas==2.2.2**              | Data manipulation |
| **jsonlines==4.0.0**           | JSONL file support |
| **python-dotenv==1.0.1**       | Load environment variables |
| **huggingface_hub==0.14.1**    | Model loading (runs offline) |

---

## ⚙️ Requirements

- Docker (preferred)
- Or install manually with:

```bash
pip install -r requirements.txt
```

---

## 📌 Constraints & Performance

- 🧠 **CPU-only**, No GPU needed
- 🚫 **Offline-first** (no internet calls)
- ⏱️ **< 10 seconds** per PDF (~50 pages)
- 📦 **Model & dependencies under 200MB**

---

## 🧠 How It Works (Pipeline)

1. `main.py` reads `sample_input.json`
2. For each PDF:
   - `pdf_parser.py` extracts section headings and text
   - `filter.py` ranks sections based on persona/task relevance
   - `summarizer.py` optionally condenses content
3. Outputs structured sections to `output.json`

---

## 📃 License

For hackathon/demo purposes only. Not production-ready.
