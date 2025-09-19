from PIL import Image, ImageDraw, ImageFont
import stepic
import os
from datetime import datetime
from utils import make_secret_key, read_key_from_file, create_hmac, KEY_PATH

def embed_visible_watermark(input_path: str, output_path: str, text: str, font_size=32):
    """Thêm watermark chữ hiển thị lên ảnh (góc phải dưới)."""
    img = Image.open(input_path).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    w, h = img.size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = (w - text_w - 10, h - text_h - 10)

    draw.text(pos, text, fill=(255, 255, 255, 150), font=font)

    watermarked = Image.alpha_composite(img, txt_layer).convert("RGB")
    temp_png = output_path + ".tmp.png"
    watermarked.save(temp_png, format="PNG")
    return temp_png


def sign_image(input_image: str, output_image: str, owner: str, logo_id: str):
    """
    Tạo và nhúng watermark (ẩn + hiện) vào ảnh.
    - input_image: đường dẫn ảnh gốc
    - output_image: nơi lưu ảnh đã ký
    - owner: tên/chủ sở hữu (do bạn nhập tay)
    - logo_id: mã logo / định danh
    """
    os.makedirs(os.path.dirname(output_image) or ".", exist_ok=True)

    # Tạo khóa bí mật nếu chưa có
    make_secret_key()
    key = read_key_from_file(KEY_PATH)

    # Data để ký (thời gian ở dạng YYYY-MM-DD HH:MM:SS)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_field = f"Owner:{owner} | LogoID:{logo_id} | Timestamp:{ts}"
    signature = create_hmac(data_field, key)
    payload = f"{data_field} | Signature:{signature}"

    # Bước 1: thêm visible watermark
    visible_text = f"{owner} ©"
    temp_png = embed_visible_watermark(input_image, output_image, visible_text)

    # Bước 2: nhúng invisible watermark
    img = Image.open(temp_png).convert("RGBA")
    encoded_img = stepic.encode(img, payload.encode("utf-8"))
    encoded_img.save(output_image, "PNG")

    # Xóa file tạm
    try:
        os.remove(temp_png)
    except Exception:
        pass

    print(f"✅ Ảnh đã được ký và lưu vào {output_image}")
    return output_image


