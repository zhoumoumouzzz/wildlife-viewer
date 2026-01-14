import sqlite3
# 建议使用绝对导入以确保稳定性，例如 from services.db ...
try:
    from .db import get_db_connection
except ImportError:
    from services.db import get_db_connection

def get_images(limit=50, only_unconfirmed=False):
    conn = get_db_connection()
    
    # 1. 兼容性处理：判断数据库类型并设置占位符
    if isinstance(conn, sqlite3.Connection):
        # SQLite 游标不支持 dictionary 参数
        # 依靠 db.py 中设置的 conn.row_factory = sqlite3.Row 实现字典访问
        cursor = conn.cursor()
        placeholder = "?"  # SQLite 使用 ?
    else:
        # MySQL 保持原有的连接池字典模式
        cursor = conn.cursor(dictionary=True)
        placeholder = "%s" # MySQL 使用 %s

    # 2. 编写 SQL 语句（注意占位符使用变量控制）
    sql = f"""
    SELECT i.image_id, i.文件路径, i.拍摄时间, c.相机编号,
           a.annotation_id, a.是否人工确认
    FROM images i
    LEFT JOIN camera_deployments cd ON i.deployment_id = cd.deployment_id
    LEFT JOIN cameras c ON cd.camera_id = c.camera_id
    LEFT JOIN annotations a ON i.image_id = a.image_id
    """

    if only_unconfirmed:
        # SQLite 和 MySQL 都支持 IS NULL 和 = 0 的判断
        sql += " WHERE a.是否人工确认 IS NULL OR a.是否人工确认 = 0"

    # 将 %s 替换为动态占位符变量
    sql += f" ORDER BY i.拍摄时间 DESC LIMIT {placeholder}"

    # 3. 执行查询
    cursor.execute(sql, (limit,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows