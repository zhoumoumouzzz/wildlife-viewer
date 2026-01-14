import sqlite3
import os

# 1. 自动定位数据库（向上跳一级到根目录）
# os.path.dirname(__file__) 是 scripts 文件夹
# 再套一层 os.path.dirname() 就是根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'wildlife.db')

print(f"正在尝试连接数据库: {db_path}")

if not os.path.exists(db_path):
    print(f"❌ 错误：在根目录找不到 wildlife.db 文件！")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 2. 定义前缀
old_prefix = 'F:\\云南天池挑选动物视频文件20230309\\'
new_prefix = 'data/云南天池挑选动物视频文件20230309/'

try:
    # 检查 images 表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='images';")
    if not cursor.fetchone():
        print("❌ 错误：数据库中没有 'images' 表")
        exit()

    print("开始更新路径...")
    
    # 更新图片路径
    sql_images = f"""
        UPDATE images 
        SET 文件路径 = REPLACE(REPLACE(文件路径, '{old_prefix}', '{new_prefix}'), '\\', '/')
        WHERE 文件路径 LIKE '{old_prefix}%'
    """
    cursor.execute(sql_images)
    img_count = cursor.rowcount

    # 更新视频路径
    sql_videos = f"""
        UPDATE images 
        SET 视频路径 = REPLACE(REPLACE(视频路径, '{old_prefix}', '{new_prefix}'), '\\', '/')
        WHERE 视频路径 IS NOT NULL AND 视频路径 LIKE '{old_prefix}%'
    """
    cursor.execute(sql_videos)
    video_count = cursor.rowcount

    conn.commit()
    print(f"✅ 更新成功！")
    print(f"   - 修改图片路径: {img_count} 条")
    print(f"   - 修改视频路径: {video_count} 条")
    
except Exception as e:
    conn.rollback()
    print(f"❌ 发生错误: {e}")
finally:
    conn.close()