import os
from pdf_utils import extract_text_data

def test_pdf():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(root_dir, "input", "file04.pdf")

    if not os.path.exists(pdf_path):
        print("❌ PDF not found at:", pdf_path)
        return

    data = extract_text_data(pdf_path)
    print(f"✅ Extracted {len(data)} text blocks.\n")

    for block in data[:70]:
        print(f"{block['page']} | {block['size']} | {block['font']} | {block['text']}")

if __name__ == "__main__":
    test_pdf()
