# sign.py
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
import os, time
from utils import read_key_from_file, create_hmac, make_secret_key, KEY_PATH

def embed_visible_watermark_image(img: Image.Image, owner: str, font_size: int = 32) -> Image.Image:
    """Trả về Image có watermark chữ (góc phải dưới)."""
    if img.mode != "RGBA":
        base = img.convert("RGBA")
    else:
        base = img.copy()
    w, h = base.size
    txt_layer = Image.new("RGBA", base.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), owner + " ©", font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pos = (w - text_w - 10, h - text_h - 10)
    draw.text(pos, owner + " ©", fill=(255,255,255,150), font=font)
    composed = Image.alpha_composite(base, txt_layer).convert("RGB")
    return composed

def sign_image(input_path: str, output_path: str, owner: str, logo_id: str) -> str:
    """
    Ký ảnh: tạo metadata PNG gồm Owner, LogoID, Timestamp, Signature.
    Trả về đường dẫn output.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # ensure key exists
    make_secret_key()
    key = read_key_from_file(KEY_PATH)

    ts = str(int(time.time()))
    data_field = f"Owner:{owner} | LogoID:{logo_id} | Timestamp:{ts}"
    signature = create_hmac(data_field, key)

    # load image (KHÔNG convert ở bước mở ban đầu)
    img = Image.open(input_path)

    # add visible watermark (tùy chọn)
    img_with_text = embed_visible_watermark_image(img, owner)

    # create PNG metadata and save
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Owner", owner)
    meta.add_text("LogoID", logo_id)
    meta.add_text("Timestamp", ts)
    meta.add_text("Signature", signature)

    img_with_text.save(output_path, "PNG", pnginfo=meta)

    print(f"✅ Ảnh đã ký: {output_path}")
    return output_path




