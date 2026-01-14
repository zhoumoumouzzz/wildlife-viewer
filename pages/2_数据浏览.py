import streamlit as st
import pandas as pd
from services.db import get_db_connection  # 你自己的 DB 连接方法

st.set_page_config(layout="wide")

st.header("🗂️ 数据浏览")

# 所有表
tables = [
    "annotations", "behaviors", "camera_deployments", "cameras", "images", "info_sources",
    "plant_species", "site_plant_species", "site_vegetation_types", "sites",
    "species", "vegetation_types", "vegetation_zones", "water_types"
]

# 下拉框选择表
selected_table = st.selectbox("选择数据表", tables)

# 获取数据库连接
conn = get_db_connection()

# 读取前200条数据
df = pd.read_sql(f"SELECT * FROM {selected_table} LIMIT 200", conn)

# sites 表编码说明
if selected_table == "sites":
    with st.expander("📖 sites表编码说明"):
        st.markdown("""
        ### 乔木层特征
        - **乔木密度**: 0-开阔, 1-稀疏, 2-密
        - **乔木高度**: 0-5-9m, 1-10-19m, 2-20-29m, 3->30m

        ### 灌木层特征
        - **灌木高度**: 0-0-1m, 1-1-3m, 2-3-5m, 3->5m
        - **灌木盖度**: 0-0-24%, 1-25-49%, 2-50-74%, 3-75-100%
        - **灌木类型**: 0-常绿, 1-落叶, 2-竹丛, 3-混合, 4-其他

        ### 草本层特征
        - **草本盖度**: 0-0-24%, 1-25-49%, 2-50-74%, 3-75-100%
        - **草本类型**: 0-禾本为主, 1-非禾本为主

        ### 生境特点
        - 0-人路, 1-兽道, 2-山坡, 3-山脊, 4-垭口, 5-林间开阔地, 6-溪边, 7-水塘, 8-石洞旁, 9-倒木, 10-其他
        """)

# 显示数据
st.dataframe(df, use_container_width=True)

# 关闭数据库连接
conn.close()
