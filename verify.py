import stepic
from PIL import Image
from utils import read_key_from_file, create_hmac, verify_hmac

def read_watermark(image_path: str) -> str:
    """Đọc nội dung watermark trong ảnh (không verify)."""
    img = Image.open(image_path)
    data = stepic.decode(img)  # stepic.decode trả về str rồi
    return data  # không cần decode nữa

def extract_signature(image_path: str) -> str:
    """Trích riêng chữ ký từ watermark."""
    watermark = read_watermark(image_path)
    # Ví dụ watermark có dạng: "Author: Alice | Signature: abc123..."
    if "Signature:" in watermark:
        return watermark.split("Signature:")[1].strip()
    return ""

def verify_image_signature(image_path: str, data: bytes, key_path="keys/secret.key") -> bool:
    """Kiểm tra chữ ký trong ảnh có khớp với dữ liệu gốc không."""
    # Trích chữ ký ra
    signature = extract_signature(image_path)

    # Load secret key
    key = read_key_from_file(key_path)

    # Kiểm chứng
    return verify_hmac(data, key, signature)


if __name__ == "__main__":
    signed_image = "images/anh1.png"

    # 1. Đọc watermark từ ảnh
    print("🔎 Watermark trong ảnh:")
    print(read_watermark(signed_image))

    # 2. Verify chữ ký
    original_data = b"Day la du lieu goc can bao ve"
    result = verify_image_signature(signed_image, original_data)

    if result:
        print("✅ Chữ ký hợp lệ: Ảnh chưa bị chỉnh sửa, đúng người ký.")
    else:
        print("❌ Chữ ký KHÔNG hợp lệ: Ảnh đã bị chỉnh sửa hoặc sai khóa.")