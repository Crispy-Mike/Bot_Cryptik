import sqlite3
from data_bases import conn, db_lock


class Data_base_user:
    def __init__(self):
        self.database = conn

    def read(self, user_id_r):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id_r,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def write(self, user_id_w, user_nikname_w, user_name_w, user_surname_w, user_is_bot_w):
        with db_lock:
            cursor = self.database.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users
                    (user_id, user_nikname, user_name, user_surname, user_is_bot)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT (user_id) DO NOTHING
                """, (user_id_w, f"@{user_nikname_w}" if user_nikname_w else None, user_name_w, user_surname_w, user_is_bot_w))
                self.database.commit()
            finally:
                cursor.close()

    def clear_db(self):
        with db_lock:
            cursor = self.database.cursor()
            try:
                cursor.execute("DELETE FROM users")
                self.database.commit()
            finally:
                cursor.close()


class Data_base_purchase_and_sale:
    def __init__(self):
        self.database = conn

    def read(self, user_id_r):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM purchase_and_sale WHERE user_id = ?", (user_id_r,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def write(self, user_id_w, operation_type_w, first_currency_w, first_quantity_w,
              second_currency_w, second_quantity_w, timestamp_w=None):
        with db_lock:
            cursor = self.database.cursor()
            try:
                cursor.execute("""
                    INSERT INTO purchase_and_sale
                    (user_id, operation_type, first_currency, first_quantity, second_currency, second_quantity, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, COALESCE(?, CURRENT_TIMESTAMP))
                """, (user_id_w, operation_type_w, first_currency_w, first_quantity_w,
                      second_currency_w, second_quantity_w, timestamp_w))
                self.database.commit()
            finally:
                cursor.close()

    def clear_db(self):
        with db_lock:
            cursor = self.database.cursor()
            try:
                cursor.execute("DELETE FROM purchase_and_sale")
                self.database.commit()
            finally:
                cursor.close()


user_db = Data_base_user()
purchase_db = Data_base_purchase_and_sale()
