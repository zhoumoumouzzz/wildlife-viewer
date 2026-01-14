import sqlite3
try:
    from .db import get_db_connection
except ImportError:
    from services.db import get_db_connection

def get_behaviors_list():
    """获取所有行为列表，兼容 MySQL 和 SQLite"""
    conn = get_db_connection()
    
    # 兼容性处理：根据连接类型创建游标
    if isinstance(conn, sqlite3.Connection):
        # SQLite 模式：不需要 dictionary 参数
        cursor = conn.cursor()
    else:
        # MySQL 模式：保留字典游标
        cursor = conn.cursor(dictionary=True)
    
    try:
        # 静态 SQL 语句在两种数据库中通用
        cursor.execute("SELECT behavior_id, 行为名称 FROM behaviors ORDER BY 行为名称")
        behaviors = cursor.fetchall()
        cursor.close()
        conn.close()
        return behaviors
    except Exception as e:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        raise e