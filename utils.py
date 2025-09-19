# utils.py
import os
import hmac
import hashlib
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
KEY_PATH = str(BASE_DIR / "secret.key")

def make_secret_key(path: str = KEY_PATH) -> str:
    """Tạo secret.key nếu chưa có."""
    if not os.path.exists(path):
        key = os.urandom(32)
        with open(path, "wb") as f:
            f.write(key)
    return path

def read_key_from_file(path: str = KEY_PATH) -> bytes:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Secret key không tồn tại: {path}")
    with open(path, "rb") as f:
        return f.read()

def create_hmac(data: str, key: bytes) -> str:
    """Trả về hexdigest (hex string)."""
    return hmac.new(key, data.encode("utf-8"), hashlib.sha256).hexdigest()

def verify_hmac(data: str, signature: str, key: bytes) -> bool:
    expected = create_hmac(data, key)
    # luôn strip khoảng trắng trước khi so sánh
    return hmac.compare_digest(expected, signature.strip())

# helper debug: in ra metadata PNG để kiểm tra
def print_png_info(path: str):
    img = Image.open(path)
    print("PNG info keys:", img.info.keys())
    for k, v in img.info.items():
        print(k, "=", v)
