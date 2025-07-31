from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import re
from IPython.display import display
import os

def card_extracting(input_pdf, first_page,last_page):
    poppler_path=r".venv\poppler-24.08.0\Library\bin"
    
    pages = convert_from_path(input_pdf, first_page=first_page, last_page=last_page,poppler_path=poppler_path)
    cards = []

    for page_image in pages:
        width, height = page_image.size
        y_crop = 100
        x_crop = 50

        cropped = page_image.crop((y_crop, x_crop, width-y_crop, height-x_crop))

        cropped_width, cropped_height = cropped.size

        number_of_horizontal_cards = 3
        number_of_vertical_cards = 3

        x_crop_rate = cropped_width // number_of_horizontal_cards
        y_crop_rate = cropped_height // number_of_vertical_cards

        for x in range(number_of_horizontal_cards):
            for y in range(number_of_vertical_cards):
                left = x * x_crop_rate
                upper = y * y_crop_rate
                right = left + x_crop_rate
                lower = upper + y_crop_rate
                card = cropped.crop((left, upper, right, lower))
                cards.append(card)

    return cards

def extract_title_regex(text):
    # 1) Try to find full‐line titles (may include spaces or hyphens)
    candidates = []
    for line in text.splitlines():
        m = re.match(r'^[^A-Za-z\n]*([A-ZÁÀÂÃÉÈÊÍÓÔÕÚÇ’\'\-\s]+?)[^A-Za-z\n]*$', line)
        if m:
            title = m.group(1).strip()
            title = re.sub(r'\bANCESTRY$', '', title).strip()
            if len(title.replace(" ", "").replace("-", "")) >= 2 and title.upper() != "ANCESTRY":
                candidates.append(title)
    # 2) Prefer multi‐word titles
    multi = [c for c in candidates if " " in c]
    if multi:
        return max(multi, key=len)
    # 3) Then single‐word full‐line titles
    if candidates:
        return candidates[-1]
    # 4) Fallback: longest uppercase token (at least 2 letters)
    tokens = re.findall(r'[A-ZÁÀÂÃÉÈÊÍÓÔÕÚÇ’\-]{2,}', text)
    tokens = [t for t in tokens if t.upper() != "ANCESTRY"]
    return tokens[0] if tokens else "UNKNOWN"

def extract_title(card):
    card_width, card_height = card.size
    title_height = 250
    title_crop = card.crop((0, title_height, card_width, title_height+200))

    gray = title_crop.convert("L")
    bw = gray.point(lambda x: 0 if x < 180 else 255, "1")

    cfg = (
    r"--oem 3 --psm 6 "
    r"-c preserve_interword_spaces=1"
    r"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    r"-c tessedit_char_blacklist=|0123456789"
    )

    text = pytesseract.image_to_string(bw, config=cfg, lang="eng")

    title = extract_title_regex(text)

    # print(f"text: {text} - extracted title: {title}")
    return title.strip()

def make_safe_filename(title):
    safe = re.sub(r'[\\/*?:"<>|]', "", title).strip()
    safe = re.sub(r'\s+', '_', safe)
    return safe

def save_all_cards(cards):
    output_dir = "new_cards"
    os.makedirs(output_dir, exist_ok=True)

    for idx, card in enumerate(cards, start=1):
        # Assume extract_title(card) returns a clean title string
        title = extract_title(card)
        base_name = make_safe_filename(title) or f"card_{idx}"
        filename = f"{base_name}.png"
        filepath = os.path.join(output_dir, filename)
        
        counter = 1
        while os.path.exists(filepath):
            filename = f"{base_name}_{counter}.png"
            filepath = os.path.join(output_dir, filename)
            counter += 1
        
        card.save(filepath)
        print(f"Saved: {filepath}")