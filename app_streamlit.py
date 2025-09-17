import streamlit as st
import os
from utils import make_secret_key, read_key_from_file, create_hmac, verify_hmac
from sign import sign_image           # từ file sign.py
from verify import verify_image_signature, extract_signature

# Tạo thư mục lưu ảnh nếu chưa có
os.makedirs("images", exist_ok=True)

# Giao diện chính
st.title("🔐 WATERMARK & HMAC")

# Tabs điều hướng
tab1, tab2, tab3 = st.tabs(["✍️ Tạo chữ ký", "🔍 Xác minh ảnh", "👀 Xem watermark"])

# --- TAB 1: TẠO CHỮ KÝ ---
with tab1:
    st.header("✍️ Tạo chữ ký và nhúng vào ảnh")

    uploaded_file = st.file_uploader("Chọn ảnh để ký", type=["png", "jpg", "jpeg"], key="sign")
    data_text = st.text_input("Nhập dữ liệu gốc (Data)", key="data_sign")

    if st.button("Ký ảnh"):
        if uploaded_file and data_text:
            # Lưu ảnh gốc (giữ đúng định dạng tải lên)
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            img_path = f"images/uploaded{ext}"
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Tạo/đọc khóa bí mật
            make_secret_key()
            key = read_key_from_file()

            # Sinh chữ ký HMAC
            signature = create_hmac(data_text, key)

            # Nhúng chữ ký vào ảnh
            signed_path = f"images/signed{ext}"
            sign_image(img_path, signature, signed_path)

            st.success("✅ Ảnh đã được ký thành công!")
            st.image(signed_path, caption="Ảnh đã ký")
        else:
            st.warning("⚠️ Hãy chọn ảnh và nhập dữ liệu.")

# --- TAB 2: XÁC MINH ---
with tab2:
    st.header("🔍 Xác minh chữ ký trong ảnh")

    uploaded_signed = st.file_uploader("Chọn ảnh đã ký", type=["png", "jpg", "jpeg"], key="verify")
    data_input = st.text_input("Nhập dữ liệu gốc để xác minh", key="data_verify")

    if st.button("Xác minh ảnh"):
        if uploaded_signed and data_input:
            ext = os.path.splitext(uploaded_signed.name)[1].lower()
            img_path = f"images/to_verify{ext}"
            with open(img_path, "wb") as f:
                f.write(uploaded_signed.getbuffer())

            result = verify_image_signature(img_path, data_input.encode("utf-8"))

            if result:
                st.success("✅ Chữ ký hợp lệ: Ảnh chưa bị chỉnh sửa!")
            else:
                st.error("❌ Chữ ký KHÔNG hợp lệ: Ảnh bị chỉnh sửa hoặc dữ liệu sai.")
        else:
            st.warning("⚠️ Hãy tải ảnh đã ký và nhập dữ liệu gốc.")

# --- TAB 3: XEM WATERMARK ---
with tab3:
    st.header("👀 Xem nội dung watermark trong ảnh")

    uploaded_view = st.file_uploader("Chọn ảnh đã ký", type=["png", "jpg", "jpeg"], key="view")

    if st.button("Xem watermark"):
        if uploaded_view:
            ext = os.path.splitext(uploaded_view.name)[1].lower()
            img_path = f"images/to_view{ext}"
            with open(img_path, "wb") as f:
                f.write(uploaded_view.getbuffer())

            extracted = extract_signature(img_path)

            if extracted:
                st.text_area("Watermark (Signature)", extracted, height=100)
            else:
                st.error("❌ Không tìm thấy watermark trong ảnh.")
        else:
            st.warning("⚠️ Hãy chọn ảnh để xem watermark.")