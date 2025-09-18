import stepic
from PIL import Image
from utils import read_key_from_file, create_hmac, verify_hmac, KEY_PATH

def read_watermark(image_path: str) -> str:
    """Đọc watermark ẩn trong ảnh."""
    img = Image.open(image_path)
    return stepic.decode(img)

def extract_data_and_signature(image_path: str):
    """
    Trích xuất dữ liệu (Owner, LogoID, Timestamp) và chữ ký từ watermark trong ảnh.
    Watermark dạng: Owner:xxx | LogoID:yyy | Timestamp:zzz | Signature:aaa
    """
    watermark = read_watermark(image_path)
    parts = watermark.split("|")

    owner, logo_id, ts, signature = "", "", "", ""
    for part in parts:
        p = part.strip()
        if p.startswith("Owner:"):
            owner = p.split("Owner:")[1].strip()
        elif p.startswith("LogoID:"):
            logo_id = p.split("LogoID:")[1].strip()
        elif p.startswith("Timestamp:"):
            ts = p.split("Timestamp:")[1].strip()
        elif p.startswith("Signature:"):
            signature = p.split("Signature:")[1].strip()

    # Dữ liệu gốc cần verify
    data = f"Owner:{owner} | LogoID:{logo_id} | Timestamp:{ts}"
    return data, signature, owner, logo_id, ts

def verify_image_signature(image_path: str, key_path=KEY_PATH) -> bool:
    """
    Kiểm tra chữ ký trong ảnh có hợp lệ không (ảnh có bị chỉnh sửa không).
    """
    # Trích xuất data & signature từ ảnh
    data_in_img, signature_in_img, owner, logo_id, ts = extract_data_and_signature(image_path)

    if not data_in_img or not signature_in_img:
        return False  # Không có watermark hoặc thiếu thông tin

    # Đọc key
    key = read_key_from_file(key_path)

    # Sinh chữ ký mong đợi
    expected_signature = create_hmac(data_in_img, key)

    # So sánh chữ ký
    return verify_hmac(data_in_img, key, signature_in_img)
