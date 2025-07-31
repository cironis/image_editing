from PIL import Image, ImageDraw
import os

# === Config ===
CARD_FOLDER = "cards"
OUTPUT_FOLDER = "a4_to_print"

A4_WIDTH = 2480
A4_HEIGHT = 3508
SPACING = 10  # space between cards (used for dotted lines)
CARDS_PER_ROW = 3

def draw_dotted_line(draw, start, end, dash_length=10, gap=10):
    if start[0] == end[0]:  # vertical
        x = start[0]
        for y in range(start[1], end[1], dash_length + gap):
            draw.line((x, y, x, min(y + dash_length, end[1])), fill="gray", width=1)
    else:  # horizontal
        y = start[1]
        for x in range(start[0], end[0], dash_length + gap):
            draw.line((x, y, min(x + dash_length, end[0]), y), fill="gray", width=1)

def paste_cards(card_filenames, output_file_name="a4_cards_output.jpg"):
    first_card = Image.open(os.path.join(CARD_FOLDER, card_filenames[0]))
    orig_w, orig_h = first_card.size

    total_spacing = SPACING * (CARDS_PER_ROW - 1)
    resized_w = (A4_WIDTH - total_spacing) // CARDS_PER_ROW
    resized_h = int(orig_h * (resized_w / orig_w))

    total_cards = len(card_filenames)
    rows = (total_cards + CARDS_PER_ROW - 1) // CARDS_PER_ROW

    canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
    draw = ImageDraw.Draw(canvas)

    for idx, filename in enumerate(card_filenames):
        row = idx // CARDS_PER_ROW
        col = idx % CARDS_PER_ROW
        x = col * (resized_w + SPACING)
        y = row * (resized_h + SPACING)
        card = Image.open(os.path.join(CARD_FOLDER, filename))
        # use LANCZOS instead of ANTIALIAS
        card = card.resize((resized_w, resized_h), resample=Image.LANCZOS)
        canvas.paste(card, (x, y))

    # vertical separators
    for c in range(1, CARDS_PER_ROW):
        x = c * resized_w + (c - 1) * SPACING + SPACING // 2
        draw_dotted_line(draw, (x, 0), (x, rows * (resized_h + SPACING) - SPACING))

    # horizontal separators
    for r in range(1, rows):
        y = r * resized_h + (r - 1) * SPACING + SPACING // 2
        draw_dotted_line(draw, (0, y), (CARDS_PER_ROW * (resized_w + SPACING) - SPACING, y))

    OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, output_file_name)
    canvas.save(OUTPUT_FILE)
    print(f"Saved to {OUTPUT_FILE} ({A4_WIDTH}x{A4_HEIGHT})")
