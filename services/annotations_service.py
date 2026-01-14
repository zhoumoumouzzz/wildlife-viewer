import sqlite3
try:
    from .db import get_db_connection
except ImportError:
    from services.db import get_db_connection

def insert_annotation(image_id, species_id, behavior_id,
                      animal_count, age_group, gender,
                      confirmer, note, is_confirmed=True):
    conn = get_db_connection()
    
    # 1. 兼容性处理：确定占位符
    if isinstance(conn, sqlite3.Connection):
        cursor = conn.cursor()
        placeholder = "?"  # SQLite 语法
    else:
        # MySQL 默认游标即可，如果不确定其他地方是否需要字典，也可以不传
        cursor = conn.cursor()
        placeholder = "%s" # MySQL 语法

    # 2. 动态构造 SQL 语句，使用对应的占位符
    # 构造 9 个占位符，例如 (?, ?, ?, ?, ?, ?, ?, ?, ?) 或 (%s, %s, ...)
    placeholders_str = ", ".join([placeholder] * 9)
    
    sql = f"""
    INSERT INTO annotations
    (image_id, species_id, behavior_id, animal_count, age_group, gender,
     是否人工确认, 确认人, 备注)
    VALUES ({placeholders_str})
    """

    try:
        cursor.execute(sql, (
            image_id,
            species_id,
            behavior_id,
            animal_count,
            age_group,
            gender,
            1 if is_confirmed else 0,
            confirmer,
            note
        ))

        conn.commit()
    except Exception as e:
        conn.rollback() # 出错时回滚
        raise e
    finally:
        cursor.close()
        conn.close()