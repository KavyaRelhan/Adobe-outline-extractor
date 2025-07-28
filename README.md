# 📝 Adobe PDF Outline Extractor

This project extracts structured outlines (headings) and the title from PDF documents using logical heuristics based on font size, font style, and layout structure — **no machine learning used**.

---

## 📌 Features

- Detects the document title based on largest font text on the first page.
- Extracts a hierarchical heading structure (H1, H2, H3...) based on:
  - Font size/style transitions
  - Numbered heading patterns (e.g., `1.`, `2.1`)
  - Layout and visual grouping (via bounding boxes)
- Ignores false positives like:
  - Short symbols-only lines (`●`, `...`, `-`)
  - Repeating paragraph identifiers (`1.`, `2.`, etc. in forms)

---

## 📂 Folder Structure

.
├── input/                # PDF files to process
├── output/               # JSON outputs
└── src/
    ├── extract_outline.py    # Main runner script
    ├── pdf_utils.py          # Extracts raw spans from PDF using PyMuPDF
    ├── heading_detector.py   # Title and heading detection logic
    └── json_writer.py        # Writes structured output to JSON


---

## 🚀 Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/adobe-outline-extractor.git
   cd adobe-outline-extractor
2. Set up a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
4. 
