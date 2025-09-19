# app_streamlit.py (chỉ phần chính, thay file cũ)
import streamlit as st
import os
from PIL import Image
from utils import make_secret_key, read_key_from_file, create_hmac, KEY_PATH
from sign import sign_image
from verify import verify_image_signature, extract_data_and_signature

os.makedirs("images", exist_ok=True)
st.title("🔐 WATERMARK & HMAC (Metadata)")

tab1, tab2, tab3 = st.tabs(["✍️ Tạo chữ ký", "🔍 Xác minh ảnh", "👀 Xem watermark"])

with tab1:
    st.header("✍️ Tạo chữ ký và nhúng vào ảnh")
    uploaded_file = st.file_uploader("Chọn ảnh để ký (PNG/JPG)", type=["png","jpg","jpeg"], key="sign")
    owner_input = st.text_input("Tên chủ sở hữu (Owner)", key="owner_sign")
    logo_input = st.text_input("Mã logo/ID", key="logo_sign")
    if st.button("Ký ảnh"):
        if uploaded_file and owner_input and logo_input:
            in_path = "images/uploaded.png"
            # lưu raw bytes gốc
            with open(in_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            signed_path = "images/signed.png"
            sign_image(in_path, signed_path, owner_input, logo_input)
            st.success("✅ Ảnh đã được ký thành công!")
            st.image(signed_path, caption=f"Ảnh đã ký bởi {owner_input}")
            with open(signed_path, "rb") as f:
                st.download_button("⬇️ Tải ảnh đã ký", f, file_name="signed.png")
        else:
            st.warning("⚠️ Hãy chọn ảnh và nhập đầy đủ thông tin.")

with tab2:
    st.header("🔍 Xác minh chữ ký trong ảnh")
    uploaded_signed = st.file_uploader("Chọn ảnh đã ký (PNG)", type=["png","jpg","jpeg"], key="verify")
    if st.button("Xác minh ảnh"):
        if uploaded_signed:
            tmp = "images/to_verify.png"
            with open(tmp, "wb") as f:
                f.write(uploaded_signed.getbuffer())
            result = verify_image_signature(tmp)
            if result:
                st.success("✅ Chữ ký hợp lệ: Ảnh chưa bị chỉnh sửa!")
            else:
                st.error("❌ Chữ ký KHÔNG hợp lệ: Ảnh bị chỉnh sửa hoặc metadata/key sai.")
                # debug: show metadata fields
                try:
                    data_field, signature, owner, logo_id, ts = extract_data_and_signature(tmp)
                    st.write("**Debug metadata:**")
                    st.write("Owner:", owner)
                    st.write("LogoID:", logo_id)
                    st.write("Timestamp:", ts)
                    st.write("Signature:", signature)
                    # show expected signature computed locally
                    key = read_key_from_file(KEY_PATH)
                    expected = create_hmac(data_field, key)
                    st.write("Expected hexdigest:", expected)
                except Exception as ex:
                    st.write("Không đọc được metadata:", ex)
        else:
            st.warning("⚠️ Hãy tải ảnh đã ký để xác minh.")

with tab3:
    st.header("👀 Xem nội dung watermark trong ảnh (metadata)")
    uploaded_view = st.file_uploader("Chọn ảnh đã ký (PNG/JPG)", type=["png","jpg","jpeg"], key="view")
    if st.button("Xem watermark"):
        if uploaded_view:
            tmpv = "images/to_view.png"
            with open(tmpv, "wb") as f:
                f.write(uploaded_view.getbuffer())
            try:
                data, signature, owner, logo_id, ts = extract_data_and_signature(tmpv)
                st.text_area("Watermark (Data)", data, height=80)
                st.text_area("Watermark (Signature)", signature, height=80)
                st.text_input("Chủ sở hữu", owner)
                st.text_input("Logo/ID", logo_id)
                st.text_input("Thời gian ký", ts)
            except Exception as e:
                st.error(f"❌ Không đọc được watermark: {e}")
        else:
            st.warning("⚠️ Hãy chọn ảnh để xem watermark.")



