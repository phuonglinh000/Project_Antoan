import streamlit as st
import os
import pandas as pd
from PIL import Image
from utils import make_secret_key, read_key_from_file, create_hmac, KEY_PATH
from sign import sign_image
from verify import verify_image_signature, extract_data_and_signature
from db import save_image_history, get_all_history   # kết nối MySQL

# Tạo thư mục lưu ảnh
os.makedirs("images", exist_ok=True)

st.title("🔐 WATERMARK & HMAC (Metadata + Lưu DB)")

# Tabs chức năng
tab1, tab2, tab3, tab4 = st.tabs([
    "✍️ Tạo chữ ký",
    "🔍 Xác minh ảnh",
    "👀 Xem watermark",
    "📜 Lịch sử"
])

# TAB 1: Ký ảnh
with tab1:
    st.header("✍️ Tạo chữ ký và nhúng vào ảnh")
    uploaded_file = st.file_uploader("Chọn ảnh để ký (PNG/JPG)", type=["png","jpg","jpeg"], key="sign")
    owner_input = st.text_input("Tên chủ sở hữu (Owner)", key="owner_sign")
    logo_input = st.text_input("Mã logo/ID", key="logo_sign")

    if st.button("Ký ảnh"):
        if uploaded_file and owner_input and logo_input:
            in_path = "images/uploaded.png"
            # lưu ảnh gốc tạm
            with open(in_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            signed_path = "images/signed.png"
            sign_image(in_path, signed_path, owner_input, logo_input)

            # lấy metadata vừa nhúng để lưu DB
            try:
                data_field, signature, owner, logo_id, ts, ts_vn = extract_data_and_signature(signed_path)
                filename = os.path.basename(signed_path)
                save_image_history(filename, owner, logo_id, ts_vn, signature, description="Ảnh đã ký")
            except Exception as e:
                st.error(f"⚠️ Không lưu được vào DB: {e}")

            st.success("✅ Ảnh đã được ký và lưu lịch sử vào DB!")
            st.image(signed_path, caption=f"Ảnh đã ký bởi {owner_input}")
            with open(signed_path, "rb") as f:
                st.download_button("⬇️ Tải ảnh đã ký", f, file_name="signed.png")
        else:
            st.warning("⚠️ Hãy chọn ảnh và nhập đầy đủ thông tin.")

# TAB 2: Xác minh
with tab2:
    st.header("🔍 Xác minh chữ ký trong ảnh")
    uploaded_signed = st.file_uploader("Chọn ảnh đã ký (PNG/JPG)", type=["png","jpg","jpeg"], key="verify")

    if st.button("Xác minh ảnh"):
        if uploaded_signed:
            tmp = "images/to_verify.png"
            with open(tmp, "wb") as f:
                f.write(uploaded_signed.getbuffer())

            result = verify_image_signature(tmp)
            if result:
                st.success("✅ Chữ ký hợp lệ: Ảnh chưa bị chỉnh sửa!")
            else:
                st.error("❌ Chữ ký KHÔNG hợp lệ: Ảnh đã bị chỉnh sửa.")
                try:
                    data_field, signature, owner, logo_id, ts, ts_vn = extract_data_and_signature(tmp)
                    st.write("**Debug metadata:**")
                    st.write("Owner:", owner)
                    st.write("LogoID:", logo_id)
                    st.write("Thời gian ký:", ts_vn)
                    st.write("Signature:", signature)
                    # so sánh với chữ ký mong đợi
                    key = read_key_from_file(KEY_PATH)
                    expected = create_hmac(data_field, key)
                    st.write("Expected hexdigest:", expected)
                except Exception as ex:
                    st.write("Không đọc được:", ex)
        else:
            st.warning("⚠️ Hãy tải ảnh đã ký để xác minh.")

# TAB 3: Xem watermark
with tab3:
    st.header("👀 Xem nội dung watermark trong ảnh")
    uploaded_view = st.file_uploader("Chọn ảnh đã ký (PNG/JPG)", type=["png","jpg","jpeg"], key="view")

    if st.button("Xem watermark"):
        if uploaded_view:
            tmpv = "images/to_view.png"
            with open(tmpv, "wb") as f:
                f.write(uploaded_view.getbuffer())

            try:
                data, signature, owner, logo_id, ts, ts_vn = extract_data_and_signature(tmpv)
                st.text_area("Watermark (Data)", data, height=80)
                st.text_area("Watermark (Signature)", signature, height=80)
                st.text_input("Chủ sở hữu", owner)
                st.text_input("Logo/ID", logo_id)
                st.text_input("Thời gian ký", ts_vn)
            except Exception as e:
                st.error(f"❌ Không đọc được watermark: {e}")
        else:
            st.warning("⚠️ Hãy chọn ảnh để xem watermark.")

# TAB 4: Lịch sử
with tab4:
    st.header("📜 Lịch sử ký ảnh")
    try:
        rows = get_all_history()
        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df)
        else:
            st.info("Chưa có dữ liệu trong lịch sử.")
    except Exception as e:
        st.error(f"⚠️ Không lấy được lịch sử: {e}")
