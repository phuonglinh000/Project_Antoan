import os
import secrets
import hmac
import hashlib

KEY_PATH = "keys/secret.key"

def make_secret_key(key_path: str = KEY_PATH):
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    if not os.path.exists(key_path):
        secret = secrets.token_bytes(32)  
        write_key_to_file(key_path, secret)
        print("Da tao secret key .")

def write_key_to_file(key_path: str, secret: bytes):
    with open(key_path, "wb") as f:
        f.write(secret)

def read_key_from_file(key_path: str = KEY_PATH) -> bytes:
    with open(key_path, "rb") as f:
        return f.read()

def create_hmac(data, secret: bytes) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hmac.new(secret, data, hashlib.sha256).hexdigest()

def verify_hmac(data, secret: bytes, signature: str) -> bool:
    expected = create_hmac(data, secret)
    return hmac.compare_digest(expected, signature)