import streamlit as st
import os
from PIL import Image
from utils import make_secret_key, read_key_from_file
from sign import sign_image
from verify import verify_image_signature, extract_data_and_signature

# Tạo thư mục lưu ảnh nếu chưa có
os.makedirs("images", exist_ok=True)

# Giao diện chính
st.title("🔐 WATERMARK & HMAC (Metadata)")

# Tabs điều hướng
tab1, tab2, tab3 = st.tabs(["✍️ Tạo chữ ký", "🔍 Xác minh ảnh", "👀 Xem watermark"])

# --- TAB 1: TẠO CHỮ KÝ ---
with tab1:
    st.header("✍️ Tạo chữ ký và nhúng vào ảnh")

    uploaded_file = st.file_uploader("Chọn ảnh để ký (PNG/JPG)", type=["png", "jpg", "jpeg"], key="sign")
    owner_input = st.text_input("Tên chủ sở hữu (Owner)", key="owner_sign")
    logo_input = st.text_input("Mã logo/ID", key="logo_sign")

    if st.button("Ký ảnh"):
        if uploaded_file and owner_input and logo_input:
            # Luôn lưu tạm thành PNG
            img_path = "images/uploaded.png"
            img = Image.open(uploaded_file)
            img.save(img_path, "PNG")

            # Tạo/đọc khóa bí mật
            make_secret_key()
            read_key_from_file()

            # Nhúng chữ ký + metadata vào ảnh
            signed_path = "images/signed.png"
            sign_image(img_path, signed_path, owner_input, logo_input)

            st.success("✅ Ảnh đã được ký thành công!")
            st.image(signed_path, caption=f"Ảnh đã ký bởi {owner_input}")
            with open(signed_path, "rb") as f:
                st.download_button("⬇️ Tải ảnh đã ký", f, file_name="signed.png")
        else:
            st.warning("⚠️ Hãy chọn ảnh và nhập đầy đủ thông tin.")

# --- TAB 2: XÁC MINH ---
with tab2:
    st.header("🔍 Xác minh chữ ký trong ảnh")

    uploaded_signed = st.file_uploader("Chọn ảnh đã ký (PNG/JPG)", type=["png", "jpg", "jpeg"], key="verify")

    if st.button("Xác minh ảnh"):
        if uploaded_signed:
            # Lưu tạm ảnh để đọc metadata
            img_path = "images/to_verify.png"
            img = Image.open(uploaded_signed)
            img.save(img_path, "PNG")

            result = verify_image_signature(img_path)

            if result:
                st.success("✅ Chữ ký hợp lệ: Ảnh chưa bị chỉnh sửa!")
            else:
                st.error("❌ Chữ ký KHÔNG hợp lệ: Ảnh bị chỉnh sửa hoặc dữ liệu sai.")
        else:
            st.warning("⚠️ Hãy tải ảnh đã ký để xác minh.")

# --- TAB 3: XEM WATERMARK ---
with tab3:
    st.header("👀 Xem nội dung watermark trong ảnh")

    uploaded_view = st.file_uploader("Chọn ảnh đã ký (PNG/JPG)", type=["png", "jpg", "jpeg"], key="view")

    if st.button("Xem watermark"):
        if uploaded_view:
            # Lưu tạm ảnh để đọc metadata
            img_path = "images/to_view.png"
            img = Image.open(uploaded_view)
            img.save(img_path, "PNG")

            try:
                data, signature, owner, logo_id, ts = extract_data_and_signature(img_path)
                st.text_area("Watermark (Data)", data, height=80)
                st.text_area("Watermark (Signature)", signature, height=80)
                st.text_input("Chủ sở hữu", owner)
                st.text_input("Logo/ID", logo_id)
                st.text_input("Thời gian ký", ts)
            except Exception as e:
                st.error(f"❌ Không đọc được watermark: {e}")
        else:
            st.warning("⚠️ Hãy chọn ảnh để xem watermark.")


