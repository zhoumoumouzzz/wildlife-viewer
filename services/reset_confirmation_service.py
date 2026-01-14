from .db import get_db_connection

def reset_all_confirmations():
    """重置所有图片的确认状态为未确认"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 更新所有标注的确认状态为0（未确认）
        cursor.execute("UPDATE annotations SET 是否人工确认 = 0")
        affected_rows = cursor.rowcount
        
        # 提交事务
        conn.commit()
        cursor.close()
        conn.close()
        
        return affected_rows
    except Exception as e:
        # 发生错误时回滚
        conn.rollback()
        cursor.close()
        conn.close()
        raise e