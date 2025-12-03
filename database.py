import sqlite3
from datetime import datetime

# مسیر فایل دیتابیس - اطمینان حاصل کنید که این مسیر در پروژه‌تان صحیح است.
# این فایل database.db در کنار فایل database.py ساخته خواهد شد.
DATABASE_URL = "database.db"

def create_tables():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # --- جدول users (جدولی که قبلاً با موفقیت ازش استفاده کردیم) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    # نکته: created_at و updated_at رو برای جدول users هم اضافه کردم تا یکپارچگی بیشتری داشته باشه.
    # اگه دیتابیس فعلی‌تون (database.db) رو حذف کنید، این فیلدها برای کاربران جدید هم اعمال میشن.

    # --- جدول readings (جدول جدید برای "فنجان‌خوان دیجیتال حنا") ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type_of_reading TEXT NOT NULL, -- جدید: برای تعیین نوع فال (مثلا 'coffee', 'intention')
            image_url TEXT,               -- آدرس عکس فنجان یا هر تصویر مرتبط با فال
            request_date TEXT NOT NULL,   -- تاریخ و زمان درخواست فال
            interpretation_text TEXT,     -- متن تفسیر فال
            status TEXT NOT NULL,         -- وضعیت فعلی فال (مثلا 'pending', 'completed')
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully with users and readings tables.")

if __name__ == "__main__":
    create_tables()
