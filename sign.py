from PIL import Image
import stepic
import os
from utils import make_secret_key, read_key_from_file, create_hmac, KEY_PATH

def hide_watermark(input_image: str, output_image: str, data: bytes):
    # Tạo hoặc đọc secret key
    make_secret_key()
    secret = read_key_from_file(KEY_PATH)

    # Tạo chữ ký từ dữ liệu gốc
    signature = create_hmac(data, secret)

    # Nhúng cả dữ liệu gốc + chữ ký vào ảnh
    watermark_data = f"Data: {data.decode('utf-8')} | Signature: {signature}"

    img = Image.open(input_image)
    encoded_img = stepic.encode(img, watermark_data.encode("utf-8"))

    # Đảm bảo thư mục tồn tại rồi lưu ảnh
    os.makedirs(os.path.dirname(output_image), exist_ok=True)
    encoded_img.save(output_image, "PNG")

    print(f"✅ Đã nhúng watermark vào {output_image}")
