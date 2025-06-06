import json


def solution(txt_file):
    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]

    with open(json_file := "article_for_json_practice3.json", "w", encoding="utf-8") as f:
        json.dump({"paragraphs": paragraphs}, f)
    return json_file
