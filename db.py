import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        ssl_ca="certs/ca.pem"
    )

def save_image_history(filename, owner=None, logo_id=None, thoi_gian=None, signature=None, description=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO image_history (filename, owner, logo_id, thoi_gian, signature, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (filename, owner, logo_id, thoi_gian, signature, description))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_history():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM image_history ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows