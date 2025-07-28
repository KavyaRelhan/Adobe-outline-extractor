import re
from collections import defaultdict

def clean_text(text):
    return re.sub(r'[.\s●•]+$', '', text.strip())

def detect_title(blocks):
    # Look only on the first page
    first_page_blocks = [b for b in blocks if b['page'] == 0]
    if not first_page_blocks:
        return "Untitled Document"

    # Sort by font size
    sorted_blocks = sorted(first_page_blocks, key=lambda x: -x['size'])
    title_size = sorted_blocks[0]['size']
    title_parts = [b['text'].strip() for b in sorted_blocks if abs(b['size'] - title_size) <= 1.5]
    return "  ".join(title_parts).strip()


def detect_headings(blocks):
    headings = []
    seen_texts = set()

    # Count how many times each font+size appears
    font_usage = defaultdict(int)
    for b in blocks:
        key = (b['font'], round(b['size'], 1))
        font_usage[key] += 1

    # Most used font+size is likely body text → ignore
    body_font = max(font_usage.items(), key=lambda x: x[1])[0]

    font_to_level = {}  # map from (font, size) → H1/H2...
    heading_levels = []  # stack of previous levels

    for b in blocks:
        raw_text = b['text'].strip()
        text = clean_text(raw_text)
        font = b['font']
        size = round(b['size'], 1)
        page = b['page']

        if not text or text in seen_texts:
            continue
        seen_texts.add(text)

        # Skip if it's TOC, header/footer, page info
        if re.search(r'(page \d+ of \d+|version \d{4})', text.lower()):
            continue

        # Skip single-digit or symbol-only lines
        if re.fullmatch(r'[\W\d\s]{1,5}', text):
            continue

        # Skip if it's same as title
        if text == detect_title(blocks):
            continue

        # Skip body text
        if (font, size) == body_font:
            continue

        # Numbered heading
        if re.match(r'^\d+(\.\d+)*\s+', text):
            depth = text.split()[0].count('.') + 1
            level = f"H{depth}"
        elif (font, size) in font_to_level:
            level = font_to_level[(font, size)]
        else:
            if not heading_levels:
                level = "H1"
            else:
                last_size = heading_levels[-1]['size']
                last_level = int(heading_levels[-1]['level'][1:])
                level = f"H{last_level + 1}" if size < last_size else heading_levels[-1]['level']
            font_to_level[(font, size)] = level

        headings.append({
            "level": level,
            "text": text,
            "page": page
        })
        heading_levels.append({
            "level": level,
            "size": size,
            "font": font
        })

    return headings
