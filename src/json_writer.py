import json

def write_output(path, title, outline):
    data = {
        "title": title,
        "outline": outline
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
