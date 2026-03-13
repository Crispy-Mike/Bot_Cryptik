import sqlite3

conn = sqlite3.connect("cryptik.db")
cursor = conn.cursor()

print("=== ТАБЛИЦА users ===")
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)

print("\n=== ТАБЛИЦА purchase_and_sale ===")
cursor.execute("SELECT * FROM purchase_and_sale")
for row in cursor.fetchall():
    print(row)

conn.close()
