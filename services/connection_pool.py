from mysql.connector import pooling
from config.db_config import DB_CONFIG

# 创建连接池
connection_pool = pooling.MySQLConnectionPool(
    pool_name="wildlife_pool",
    pool_size=5,
    pool_reset_session=True,
    **DB_CONFIG
)

def get_connection():
    """从连接池获取连接"""
    return connection_pool.get_connection()
