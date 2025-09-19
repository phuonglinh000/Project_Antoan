from PIL import Image
from utils import read_key_from_file, verify_hmac, KEY_PATH
import datetime  # thêm import

def extract_data_and_signature(image_path: str):
    """Trả về: (data_field, signature, owner, logo_id, timestamp, timestamp_vn)"""
    img = Image.open(image_path)   # KHÔNG convert
    meta = img.info

    owner = meta.get("Owner", "").strip()
    logo_id = meta.get("LogoID", "").strip()
    ts = meta.get("Timestamp", "").strip()
    signature = meta.get("Signature", "").strip()

    # --- chuyển đổi timestamp sang giờ VN ---
    timestamp_vn = ""
    if ts.isdigit():
        try:
            ts_int = int(ts)
            dt_utc = datetime.datetime.utcfromtimestamp(ts_int)
            dt_vn = dt_utc + datetime.timedelta(hours=7)
            timestamp_vn = dt_vn.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            timestamp_vn = "(không hợp lệ)"

    data_field = f"Owner:{owner} | LogoID:{logo_id} | Timestamp:{ts}"
    return data_field, signature, owner, logo_id, ts, timestamp_vn

def verify_image_signature(image_path: str) -> bool:
    """True nếu hợp lệ, False nếu sai. In debug khi sai."""
    try:
        data_field, signature, owner, logo_id, ts, timestamp_vn = extract_data_and_signature(image_path)
        if not signature:
            print("❌ Không tìm thấy trường Signature trong metadata.")
            return False
        key = read_key_from_file(KEY_PATH)
        ok = verify_hmac(data_field, signature, key)
        if not ok:
            print("❌ Verify thất bại.")
            print("  Data field:", data_field)
            print("  Signature(from image):", signature)
            print("  Expected (hexdigest):", __import__("utils").create_hmac(data_field, key))
        else:
            print(f"✅ Verify thành công cho Owner={owner}, LogoID={logo_id}")
            print(f"  Timestamp raw : {ts}")
            print(f"  Timestamp VN  : {timestamp_vn}")
        return ok
    except Exception as e:
        print("❌ Lỗi verify:", e)
        return False

