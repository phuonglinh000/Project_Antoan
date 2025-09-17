import os
import hmac
import hashlib

KEY_PATH = "keys/secret.key"

def generate_key():
    """Sinh secret key nếu chưa có"""
    os.makedirs("keys", exist_ok=True)  # tạo thư mục 'keys' nếu chưa có
    if not os.path.exists(KEY_PATH):
        key = os.urandom(32)  # 256-bit key
        with open(KEY_PATH, "wb") as f:
            f.write(key)
        print("✅ Đã tạo secret key.")

def load_key():
    """Đọc secret key từ file"""
    with open(KEY_PATH, "rb") as f:
        return f.read()

def create_hmac(data: bytes, key: bytes) -> str:
    """Tạo chữ ký HMAC-SHA256"""
    return hmac.new(key, data, hashlib.sha256).hexdigest()

def verify_hmac(data: bytes, key: bytes, signature: str) -> bool:
    """Kiểm tra chữ ký HMAC-SHA256"""
    expected = create_hmac(data, key)
    return hmac.compare_digest(expected, signature)


# ================== DEMO ==================
if __name__ == "__main__":
    generate_key()               # tạo key nếu chưa có
    key = load_key()             # đọc key từ file

    message = b"hello world"     # dữ liệu gốc (bytes)
    sig = create_hmac(message, key)

    print(f"🔑 Key (ẩn trong file, không in ra)!")
    print(f"✍️  Dữ liệu: {message}")
    print(f"🖊️  Chữ ký tạo ra: {sig}")

    # Kiểm tra đúng
    print("✅ Kiểm tra đúng:", verify_hmac(message, key, sig))

    # Kiểm tra sai (dữ liệu thay đổi)
    print("❌ Kiểm tra sai:", verify_hmac(b"hello hacker", key, sig))
