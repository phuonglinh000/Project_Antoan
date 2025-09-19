from PIL import Image, PngImagePlugin
import time, os
from utils import make_secret_key, read_key_from_file, create_hmac, KEY_PATH

def sign_image(input_image: str, output_image: str, owner: str, logo_id: str):
    """Ký ảnh bằng cách nhúng watermark (metadata PNG)."""

    # Tạo thư mục nếu chưa có
    os.makedirs(os.path.dirname(output_image) or ".", exist_ok=True)

    # Tạo hoặc đọc khóa bí mật
    make_secret_key()
    key = read_key_from_file(KEY_PATH)

    # Tạo dữ liệu cần ký
    ts = int(time.time())
    data_field = f"Owner:{owner} | LogoID:{logo_id} | Timestamp:{ts}"
    signature = create_hmac(data_field, key)
    payload = f"{data_field} | Signature:{signature}"

    # Load ảnh gốc
    img = Image.open(input_image)

    # Thêm metadata
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Watermark", payload)

    # Lưu ảnh với metadata
    img.save(output_image, "PNG", pnginfo=meta)

    print(f"✅ Ảnh đã ký và lưu vào {output_image}")
    return output_image

