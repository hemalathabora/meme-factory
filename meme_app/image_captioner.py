from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import textwrap

def create_meme(image_path, caption, output_path):
    meme_size = (600, 600)
    image = Image.open(image_path).convert("RGB")
    image.thumbnail(meme_size, Image.Resampling.LANCZOS)

    # Pad image to meme_size if needed
    padded_image = Image.new("RGB", meme_size, (255, 255, 255))
    x_offset = (meme_size[0] - image.width) // 2
    y_offset = (meme_size[1] - image.height) // 2
    padded_image.paste(image, (x_offset, y_offset))
    image = padded_image

    draw = ImageDraw.Draw(image)

    # Try to use Impact font, fallback to Arial
    def get_font(font_size):
        try:
            return ImageFont.truetype("impact.ttf", font_size)
        except:
            try:
                return ImageFont.truetype("arialbd.ttf", font_size)
            except:
                return ImageFont.load_default()

    # Dynamic font sizing and wrapping
    def fit_text(text, max_width, start_size=60, min_size=20):
        font_size = start_size
        while font_size >= min_size:
            font = get_font(font_size)
            wrapped = textwrap.fill(text, width=25)
            bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)
            if bbox[2] - bbox[0] <= max_width:
                return font, wrapped
            font_size -= 2
        return font, wrapped

    # Prepare caption
    text = caption.upper()
    font, wrapped_text = fit_text(text, meme_size[0] - 40)

    # Position at bottom center
    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (meme_size[0] - text_width) // 2
    y = meme_size[1] - text_height - 30  # 30 px from bottom

    # Draw thick black outline for meme style
    outline_range = 4
    for dx in range(-outline_range, outline_range + 1):
        for dy in range(-outline_range, outline_range + 1):
            if dx != 0 or dy != 0:
                draw.multiline_text((x + dx, y + dy), wrapped_text, font=font, fill="black")

    # Draw white text
    draw.multiline_text((x, y), wrapped_text, font=font, fill="white")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
