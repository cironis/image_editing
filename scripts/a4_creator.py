from PIL import Image, ImageDraw
import os

# === Config ===
CARD_FOLDER = "cards"
OUTPUT_FOLDER = "a4_to_print"

A4_WIDTH = 2480
A4_HEIGHT = 3508
SPACING = 10  # space between cards (used for dotted lines)

def draw_dotted_line(draw, start, end, dash_length=10, gap=10):
    if start[0] == end[0]:  # vertical
        x = start[0]
        for y in range(start[1], end[1], dash_length + gap):
            draw.line((x, y, x, min(y + dash_length, end[1])), fill="gray", width=1)
    else:  # horizontal
        y = start[1]
        for x in range(start[0], end[0], dash_length + gap):
            draw.line((x, y, min(x + dash_length, end[0]), y), fill="gray", width=1)

def paste_cards(card_filenames,output_file_name="a4_cards_output.jpg"):
    first_card = Image.open(os.path.join(CARD_FOLDER, card_filenames[0]))
    card_w, card_h = first_card.size

    # Max cards per row and column
    max_cols = (A4_WIDTH + SPACING) // (card_w + SPACING)
    max_rows = (A4_HEIGHT + SPACING) // (card_h + SPACING)
    total_cards = len(card_filenames)

    cols = min(max_cols, total_cards)
    rows = (total_cards + cols - 1) // cols

    # Calculate final canvas size
    canvas_width = cols * card_w + (cols - 1) * SPACING
    canvas_height = rows * card_h + (rows - 1) * SPACING
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    for idx, filename in enumerate(card_filenames):
        row = idx // cols
        col = idx % cols
        x = col * (card_w + SPACING)
        y = row * (card_h + SPACING)
        card_path = os.path.join(CARD_FOLDER, filename)
        card = Image.open(card_path)
        canvas.paste(card, (x, y))

    # Draw vertical dotted lines between columns
    for c in range(1, cols):
        x = c * card_w + (c - 1) * SPACING + SPACING // 2
        draw_dotted_line(draw, (x, 0), (x, canvas_height))

    # Draw horizontal dotted lines between rows
    for r in range(1, rows):
        y = r * card_h + (r - 1) * SPACING + SPACING // 2
        draw_dotted_line(draw, (0, y), (canvas_width, y))

    OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, output_file_name)
    canvas.save(OUTPUT_FILE)
    
    print(f"Saved to {OUTPUT_FILE} ({canvas_width}x{canvas_height})")