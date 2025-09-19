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

def save_image_history(filename, action, status):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO image_history (filename, action, status) VALUES (%s, %s, %s)"
    cursor.execute(sql, (filename, action, status))
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
