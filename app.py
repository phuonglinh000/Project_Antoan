from signer import hide_watermark
from verifier import read_watermark, verify_image_signature

def menu():
    print("\n===== WATERMARK APP =====")
    print("1. Nhúng watermark vào ảnh")
    print("2. Đọc watermark trong ảnh")
    print("3. Verify chữ ký trong ảnh")
    print("0. Thoát")
    print("=========================")

if __name__ == "__main__":
    while True:
        menu()
        choice = input("👉 Chọn chức năng: ")

        if choice == "1":
            input_img = input("Nhập đường dẫn ảnh gốc (vd: images/original.png): ")
            output_img = input("Nhập đường dẫn lưu ảnh đã nhúng (vd: images/anh1.png): ")
            author = input("Tên tác giả: ")
            hide_watermark(input_img, output_img, author)

        elif choice == "2":
            img_path = input("Nhập đường dẫn ảnh cần đọc watermark: ")
            try:
                wm = read_watermark(img_path)
                print("\n🔎 Watermark trong ảnh:")
                print(wm)
            except Exception as e:
                print(f"❌ Lỗi đọc watermark: {e}")

        elif choice == "3":
            img_path = input("Nhập đường dẫn ảnh cần verify: ")
            data = input("Nhập dữ liệu gốc (text): ").encode("utf-8")
            try:
                result = verify_image_signature(img_path, data)
                if result:
                    print("✅ Chữ ký hợp lệ: Ảnh chưa bị chỉnh sửa, đúng người ký.")
                else:
                    print("❌ Chữ ký KHÔNG hợp lệ: Ảnh đã bị chỉnh sửa hoặc sai khóa.")
            except Exception as e:
                print(f"❌ Lỗi verify: {e}")

        elif choice == "0":
            print("👋 Thoát chương trình.")
            break
        else:
            print("❌ Lựa chọn không hợp lệ. Hãy thử lại!")
