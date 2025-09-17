# sign.py
from PIL import Image
import stepic
import os
from utils import make_secret_key, read_key_from_file, create_hmac, KEY_PATH

def sign_image(input_image: str, signature: str, output_image: str):
    """
    Nhúng chữ ký (signature) vào ảnh input_image và lưu ra output_image
    """
    # Đảm bảo folder tồn tại
    os.makedirs(os.path.dirname(output_image), exist_ok=True)

    # Mở ảnh
    img = Image.open(input_image)

    # Nhúng chữ ký vào ảnh
    encoded_img = stepic.encode(img, signature.encode("utf-8"))

    # Lưu ảnh đã ký
    encoded_img.save(output_image, "PNG")
    print(f"✅ Ảnh đã được ký và lưu vào {output_image}")
