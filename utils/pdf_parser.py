import pdfplumber
import re

def parse_pdf(pdf_path):
    sections = []
    current_section = {
        "title": "Introduction",
        "content": "",
        "page_number": 1
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            try:
                words = page.extract_words(extra_attrs=["fontname", "size"])
                lines = group_words_to_lines(words)

                for line in lines:
                    line_text = line['text'].strip()
                    font_size = line['size']

                    if is_heading(line_text, font_size):
                        # Save the current section if it has content
                        if current_section['content'].strip():
                            sections.append(current_section)

                        current_section = {
                            "title": line_text,
                            "content": "",
                            "page_number": page_num
                        }
                    else:
                        current_section["content"] += line_text + " "

            except Exception as e:
                print(f"[!] Error reading page {page_num}: {e}")

    # Append last section
    if current_section['content'].strip():
        sections.append(current_section)

    return sections


def group_words_to_lines(words):
    """
    Groups PDF words into lines based on vertical position.
    Assumes words on the same line are within close y-coordinate distance.
    """
    lines = []
    if not words:
        return lines

    words = sorted(words, key=lambda x: (x['top'], x['x0']))
    current_line = []
    last_top = None
    for word in words:
        if last_top is None or abs(word['top'] - last_top) < 3:
            current_line.append(word)
        else:
            line_text = " ".join(w['text'] for w in current_line)
            avg_size = sum(w['size'] for w in current_line) / len(current_line)
            lines.append({'text': line_text, 'size': avg_size})
            current_line = [word]
        last_top = word['top']

    # Add last line
    if current_line:
        line_text = " ".join(w['text'] for w in current_line)
        avg_size = sum(w['size'] for w in current_line) / len(current_line)
        lines.append({'text': line_text, 'size': avg_size})

    return lines

def is_heading(text, font_size, threshold=11):
    """
    Returns True if line is likely to be a heading:
    - Font size is bigger than typical paragraph text
    - Line is short and starts with a capital letter
    """
    return (
        font_size > threshold and
        len(text) < 120 and
        re.match(r'^[A-Z][A-Za-z0-9\s\-,:]*$', text)
    )
