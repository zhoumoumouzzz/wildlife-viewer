import streamlit as st
from services.db import get_db_connection
import sqlite3

st.set_page_config(layout="wide")
st.header("📊 数据库结构说明")

st.markdown("""本系统支持 MySQL 和 SQLite 存储，包含以下主要数据表：""")

conn = get_db_connection()
cursor = conn.cursor()

# 兼容性处理：获取所有表名
if isinstance(conn, sqlite3.Connection):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall() if not table[0].startswith('sqlite_')]
else:
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]

for table in tables:
    with st.expander(f"表: {table}"):
        # 兼容性处理：获取表结构
        df_data = []
        if isinstance(conn, sqlite3.Connection):
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            for col in columns:
                df_data.append({
                    "字段名": col[1],
                    "数据类型": col[2],
                    "允许NULL": "是" if col[3] == 0 else "否",
                    "键": "PRI" if col[5] == 1 else "",
                    "默认值": col[4] if col[4] else "",
                    "额外信息": ""
                })
        else:
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()
            for col in columns:
                df_data.append({
                    "字段名": col[0],
                    "数据类型": col[1],
                    "允许NULL": "是" if col[2] == "YES" else "否",
                    "键": col[3] if col[3] else "",
                    "默认值": col[4] if col[4] else "",
                    "额外信息": col[5] if col[5] else ""
                })

        st.write("**字段信息:**")
        st.dataframe(df_data, use_container_width=True)


        # 如果是特定表，添加额外说明
        if table == "species":
            st.write("**说明:** 存储物种信息，包括学名、中文名、分类信息等")
        elif table == "deployments":
            st.write("**说明:** 存储相机布设点信息，包括位置、布设时间等")
        elif table == "images":
            st.write("**说明:** 存储图像信息，包括文件路径、拍摄时间、分辨率等")
        elif table == "annotations":
            st.write("**说明:** 存储图像标注信息，包括物种识别、行为标注等")
        elif table == "habitat":
            st.write("**说明:** 存储布设点生境信息，包括植被类型、地形特征等")
        elif table == "behaviors":
            st.write("**说明:** 存储动物行为编码和描述")
        elif table == "plant_species":
            st.write("**说明:** 存储植物物种信息，包括中文名、拉丁名、保护级别等")
        elif table == "vegetation_types":
            st.write("**说明:** 存储植被类型信息，如常绿阔叶林、针叶林等")
        elif table == "water_types":
            st.write("**说明:** 存储水源类型信息，如溪流、蓄水塘、河流等")
        elif table == "vegetation_zones":
            st.write("**说明:** 存储植被带信息，如亚热带常绿阔叶林带、热带雨林带等")
        elif table == "site_vegetation_types":
            st.write("**说明:** 存储布设点与植被类型的关联关系")
            
cursor.close()
conn.close()
