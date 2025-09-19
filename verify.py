from PIL import Image
import stepic
from utils import read_key_from_file, create_hmac, KEY_PATH

def extract_data_and_signature(image_path: str):
    """Giải mã dữ liệu watermark ẩn trong ảnh."""
    img = Image.open(image_path)
    try:
        decoded = stepic.decode(img).decode("utf-8")
    except Exception:
        return None, None

    if "Signature:" not in decoded:
        return decoded, None

    data, signature = decoded.rsplit("Signature:", 1)
    return data.strip(), signature.strip()


def verify_image_signature(image_path: str):
    """Kiểm tra tính toàn vẹn chữ ký trong ảnh."""
    key = read_key_from_file(KEY_PATH)
    data, signature = extract_data_and_signature(image_path)

    if data is None or signature is None:
        return False, None

    # Tạo lại chữ ký từ dữ liệu
    expected_signature = create_hmac(data, key)

    # Kiểm tra
    valid = (expected_signature == signature)

    # Format đẹp: tách Owner, LogoID, Timestamp
    fields = {}
    try:
        for part in data.split("|"):
            if ":" in part:
                k, v = part.split(":", 1)
                fields[k.strip()] = v.strip()
    except Exception:
        pass

    result = {
        "valid": valid,
        "owner": fields.get("Owner", ""),
        "logo_id": fields.get("LogoID", ""),
        "timestamp": fields.get("Timestamp", ""),
        "signature": signature
    }

    return valid, result

