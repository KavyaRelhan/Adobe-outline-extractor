import fitz  # PyMuPDF

def extract_text_data(pdf_path):
    doc = fitz.open(pdf_path)
    spans = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if text:
                        spans.append({
                            "text": text,
                            "size": span["size"],
                            "font": span["font"],
                            "flags": span["flags"],
                            "page": page_num,
                            "x0": span["bbox"][0],
                            "y0": span["bbox"][1],
                            "x1": span["bbox"][2],
                            "y1": span["bbox"][3]
                        })
    return group_blocks(spans)


def group_blocks(spans, line_gap_thresh=3.0):
    spans = sorted(spans, key=lambda x: (x['page'], x['y0'], x['x0']))
    blocks = []
    current_block = []
    prev = None

    for span in spans:
        if prev:
            same_font = span['font'] == prev['font']
            same_size = abs(span['size'] - prev['size']) < 0.5
            close_y = abs(span['y0'] - prev['y1']) < line_gap_thresh
            same_page = span['page'] == prev['page']

            if same_font and same_size and close_y and same_page:
                current_block.append(span)
            else:
                blocks.append(merge_block(current_block))
                current_block = [span]
        else:
            current_block = [span]
        prev = span

    if current_block:
        blocks.append(merge_block(current_block))

    return blocks


def merge_block(spans):
    if not spans:
        return None
    text = ' '.join(s['text'] for s in spans)
    return {
        "text": text,
        "size": spans[0]["size"],
        "font": spans[0]["font"],
        "flags": spans[0]["flags"],
        "page": spans[0]["page"]
    }
