import os
import shutil
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import schedule
import time
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Thông tin email
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Thư mục chứa backup
DB_FOLDER = "path/to/database"
BACKUP_FOLDER = "path/to/backup"

def backup_database():
    try:
        #vòng lặp
        for filename in os.listdir(DB_FOLDER):
            if filename.endswith(".sql") or filename.endswith(".sqlite3"):
                file_path = os.path.join(DB_FOLDER, filename)
                backup_path = os.path.join(BACKUP_FOLDER, filename)
                shutil.copy(file_path, backup_path)
        
        # Gửi email thông báo thành công
        send_email("Backup thành công", "Backup các file cơ sở dữ liệu đã thành công.")
    except Exception as e:
        # Gửi email thông báo thất bại
        send_email("Backup thất bại", f"Có lỗi xảy ra: {e}")

def send_email(subject, body):
    msg = MIMEText(body)
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Không thể gửi email: {e}")

# Lên lịch chạy lúc 00:00 AM (12H ĐÊM) hàng ngày
schedule.every().day.at("00:00").do(backup_database)

while True:
    schedule.run_pending()
    time.sleep(60)