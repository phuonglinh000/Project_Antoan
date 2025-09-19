from db import get_connection

def main():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT NOW();")
        print("✅ Kết nối thành công! Thời gian server:", cursor.fetchone())
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Lỗi kết nối:", e)

if __name__ == "__main__":
    main()
