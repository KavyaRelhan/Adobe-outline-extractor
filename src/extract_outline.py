from pdf_utils import extract_text_data
from heading_detector import detect_title, detect_headings
from json_writer import write_output
import os

INPUT_DIR = "./input"
OUTPUT_DIR = "./output"

def main():
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, file)
            base_name = os.path.splitext(file)[0]
            output_path = os.path.join(OUTPUT_DIR, base_name + ".json")

            blocks = extract_text_data(pdf_path)  # Already grouped
            title = detect_title(blocks)
            outline = detect_headings(blocks)

            write_output(output_path, title, outline)

if __name__ == "__main__":
    main()
