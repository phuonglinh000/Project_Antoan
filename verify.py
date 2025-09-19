from PIL import Image
from utils import read_key_from_file, verify_hmac, KEY_PATH

def extract_data_and_signature(image_path: str):
    """
    Đọc watermark từ metadata PNG.
    Trả về: (data_field, signature, owner, logo_id, timestamp)
    """
    img = Image.open(image_path)
    watermark = img.info.get("Watermark", "")
    parts = watermark.split(" | ")

    data_field = " | ".join(parts[:-1])
    sig_field = parts[-1].replace("Signature:", "")
    owner = parts[0].replace("Owner:", "")
    logo_id = parts[1].replace("LogoID:", "")
    ts = parts[2].replace("Timestamp:", "")

    return data_field, sig_field, owner, logo_id, ts


def verify_image_signature(image_path: str) -> bool:
    """Xác minh chữ ký HMAC từ ảnh."""
    try:
        data_field, signature, _, _, _ = extract_data_and_signature(image_path)
        key = read_key_from_file(KEY_PATH)
        return verify_hmac(data_field, signature, key)
    except Exception as e:
        print(f"❌ Lỗi xác minh: {e}")
        return False

