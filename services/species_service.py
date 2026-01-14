import sqlite3
try:
    from .db import get_db_connection
except ImportError:
    from services.db import get_db_connection

def get_species_list():
    conn = get_db_connection()
    
    # 兼容性处理：判断数据库类型
    if isinstance(conn, sqlite3.Connection):
        # SQLite 模式：不支持 dictionary 参数
        # 依靠 services/db.py 中的 conn.row_factory = sqlite3.Row 实现字典功能
        cursor = conn.cursor()
    else:
        # MySQL 模式：保持原有的字典游标
        cursor = conn.cursor(dictionary=True)

    # 执行 SQL 查询（该查询语句在两种数据库中通用，无需修改占位符）
    cursor.execute("""
        SELECT species_id, 学名, 中文名
        FROM species
        ORDER BY 中文名
    """)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data