import stepic
from PIL import Image
from utils import read_key_from_file, verify_hmac, KEY_PATH

def extract_signature(image_path: str):
    img = Image.open(image_path)
    data = stepic.decode(img).decode("utf-8")

    # Chuỗi có dạng: "Data: ... | Signature: ..."
    parts = data.split(" | ")
    data_value = parts[0].replace("Data: ", "")
    signature = parts[1].replace("Signature: ", "")
    return data_value, signature

def verify_image_signature(image_path: str, original_data: bytes, key_path=KEY_PATH) -> bool:
    # Trích dữ liệu & chữ ký từ ảnh
    data_value, signature = extract_signature(image_path)
    print(f"📌 Data trong ảnh: {data_value}")
    print(f"📌 Signature trong ảnh: {signature}")

    # Đọc secret key
    key = read_key_from_file(key_path)

    # Kiểm chứng chữ ký dựa trên dữ liệu gốc
    return verify_hmac(original_data, key, signature)