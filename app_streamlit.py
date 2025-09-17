import streamlit as st
from utils import make_secret_key, read_key_from_file, create_hmac, verify_hmac
from sign import sign_image
from verifier import verify_image_signature, extract_signature

# Giao diện Streamlit
st.title("WATETMARK & HMAC")

# Tab điều hướng
tab1, tab2, tab3 = st.tabs(["Tạo chữ ký", "Xác minh ảnh", "Xem watermark"])

with tab1:
    st.header("✍️ Tạo chữ ký và nhúng vào ảnh")
    uploaded_file = st.file_uploader("Chọn ảnh để ký", type=["png", "jpg", "jpeg"])
    data_text = st.text_input("Nhập dữ liệu gốc (Data)")

    if st.button("Ký ảnh"):
        if uploaded_file and data_text:
            # Lưu ảnh tạm
            img_path = "images/uploaded.png"
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Tạo key nếu chưa có
            make_secret_key()
            key = read_key_from_file()
            signature = create_hmac(data_text, key)

            # Nhúng chữ ký
            signed_path = "images/signed.png"
            sign_image(img_path, signature, signed_path)

            st.success("✅ Ảnh đã được ký!")
            st.image(signed_path, caption="Ảnh đã ký")
        else:
            st.warning("⚠️ Hãy chọn ảnh và nhập dữ liệu.")

with tab2:
    st.header("🔍 Xác minh chữ ký trong ảnh")
    uploaded_signed = st.file_uploader("Chọn ảnh đã ký", type=["png"], key="verify")
    data_input = st.text_input("Nhập dữ liệu gốc để xác minh")

    if st.button("Xác minh"):
        if uploaded_signed and data_input:
            img_path = "images/to_verify.png"
            with open(img_path, "wb") as f:
                f.write(uploaded_signed.getbuffer())

            result = verify_image_signature(img_path, data_input.encode("utf-8"))
            if result:
                st.success("✅ Chữ ký hợp lệ: Ảnh chưa bị chỉnh sửa!")
            else:
                st.error("❌ Chữ ký KHÔNG hợp lệ: Ảnh bị chỉnh sửa hoặc sai khóa.")
        else:
            st.warning("⚠️ Hãy tải ảnh và nhập dữ liệu.")

with tab3:
    st.header("👀 Xem nội dung watermark")
    uploaded_view = st.file_uploader("Chọn ảnh đã nhúng watermark", type=["png"], key="view")

    if st.button("Xem watermark"):
        if uploaded_view:
            img_path = "images/to_view.png"
            with open(img_path, "wb") as f:
                f.write(uploaded_view.getbuffer())

            extracted = extract_signature(img_path)
            st.text_area("Watermark (Signature)", extracted, height=100)
        else:
            st.warning("⚠️ Hãy chọn ảnh.")
