import sqlite3
import os
import streamlit as st

def get_db_connection():
    # 获取根目录下的 wildlife.db
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sqlite_path = os.path.join(base_path, "wildlife.db")

    if os.path.exists(sqlite_path):
        # --- SQLite 模式 ---
        conn = sqlite3.connect(sqlite_path, check_same_thread=False)
        # 关键：让 SQLite 返回类似字典的行对象，兼容 MySQL 的 dictionary=True
        conn.row_factory = sqlite3.Row 
        return conn
    else:
        # --- MySQL 模式 ---
        import mysql.connector
        from config.db_config import DB_CONFIG
        return mysql.connector.connect(**DB_CONFIG)