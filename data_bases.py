import sqlite3
import threading

# Создаём локальное соединение для каждого потока
def get_connection():
    conn = sqlite3.connect("cryptik.db", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")  # Режим WAL для лучшей многопоточности
    return conn

# Глобальная блокировка для записей
db_lock = threading.Lock()

conn = get_connection()
