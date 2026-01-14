import streamlit as st
import pandas as pd
from services.db import get_db_connection
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

st.header("🌿 生境特征筛选")

# 添加编码说明折叠框
with st.expander("📖 编码说明"):
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

# 数字编码到文本的映射
TREE_DENSITY_MAP = {0: '开阔', 1: '稀疏', 2: '密'}
TREE_HEIGHT_MAP = {0: '5-9', 1: '10-19', 2: '20-29', 3: '>30'}
SHRUB_HEIGHT_MAP = {0: '0-1', 1: '1-3', 2: '3-5', 3: '>5'}
COVERAGE_MAP = {0: '0-24', 1: '25-49', 2: '50-74', 3: '75-100'}
SHRUB_TYPE_MAP = {0: '常绿', 1: '落叶', 2: '竹丛', 3: '混合', 4: '其他'}
HERB_TYPE_MAP = {0: '禾本为主', 1: '非禾本为主'}
HABITAT_FEATURE_MAP = {
    0: '人路', 1: '兽道', 2: '山坡', 3: '山脊', 4: '垭口',
    5: '林间开阔地', 6: '溪边', 7: '水塘', 8: '石洞旁', 9: '倒木', 10: '其他'
}

# 添加切换选项
display_mode = st.radio(
    "显示模式",
    ["编码 + 说明", "仅编码", "仅说明"],
    index=0,
    help="选择如何显示编码字段"
)

# 获取数据库连接
conn = get_db_connection()

# 构建查询 - 更新列名以匹配新的sites表结构
query = """
SELECT
    s.site_id,
    s.调查样区,
    s.省份,
    s.城市,
    s.县区,
    s.纬度,
    s.经度,
    s.海拔,
    s.生境特点,
    s.坡位,
    s.坡向,
    s.坡度,
    s.water_id,
    s.zone_id,
    s.乔木密度,
    s.乔木高度,
    s.灌木高度,
    s.灌木盖度,
    s.灌木类型,
    s.草本盖度,
    s.草本类型,
    s.人为干扰类型,
    s.备注,
    wt.类型 AS 水源类型,
    vz.带名 AS 植被带类型
FROM sites s
LEFT JOIN water_types wt ON s.water_id = wt.water_id
LEFT JOIN vegetation_zones vz ON s.zone_id = vz.zone_id
"""

# 执行查询
df = pd.read_sql(query, conn)
conn.close()

# 根据选择的显示模式处理数据
if display_mode == "编码 + 说明":
    # 创建新列显示编码和说明
    df['乔木密度'] = df['乔木密度'].apply(lambda x: f"{x} ({TREE_DENSITY_MAP.get(x, '未知')})" if pd.notna(x) else None)
    df['乔木高度'] = df['乔木高度'].apply(lambda x: f"{x} ({TREE_HEIGHT_MAP.get(x, '未知')})" if pd.notna(x) else None)
    df['灌木高度'] = df['灌木高度'].apply(lambda x: f"{x} ({SHRUB_HEIGHT_MAP.get(x, '未知')})" if pd.notna(x) else None)
    df['灌木盖度'] = df['灌木盖度'].apply(lambda x: f"{x} ({COVERAGE_MAP.get(x, '未知')})" if pd.notna(x) else None)
    df['灌木类型'] = df['灌木类型'].apply(lambda x: f"{x} ({SHRUB_TYPE_MAP.get(x, '未知')})" if pd.notna(x) else None)
    df['草本盖度'] = df['草本盖度'].apply(lambda x: f"{x} ({COVERAGE_MAP.get(x, '未知')})" if pd.notna(x) else None)
    df['草本类型'] = df['草本类型'].apply(lambda x: f"{x} ({HERB_TYPE_MAP.get(x, '未知')})" if pd.notna(x) else None)
    df['生境特点'] = df['生境特点'].apply(lambda x: f"{x} ({HABITAT_FEATURE_MAP.get(x, '未知')})" if pd.notna(x) else None)
elif display_mode == "仅说明":
    # 只显示说明
    df['乔木密度'] = df['乔木密度'].map(TREE_DENSITY_MAP)
    df['乔木高度'] = df['乔木高度'].map(TREE_HEIGHT_MAP)
    df['灌木高度'] = df['灌木高度'].map(SHRUB_HEIGHT_MAP)
    df['灌木盖度'] = df['灌木盖度'].map(COVERAGE_MAP)
    df['灌木类型'] = df['灌木类型'].map(SHRUB_TYPE_MAP)
    df['草本盖度'] = df['草本盖度'].map(COVERAGE_MAP)
    df['草本类型'] = df['草本类型'].map(HERB_TYPE_MAP)
    df['生境特点'] = df['生境特点'].map(HABITAT_FEATURE_MAP)
# "仅编码"模式保持原样，不需要转换

# 显示结果
st.markdown(f"### 查询结果 ({len(df)} 条记录)")

# 配置AgGrid选项
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True,
                          resizable=True, sortable=True, filterable=True)
gb.configure_selection(selection_mode='multiple', use_checkbox=True)
gb.configure_side_bar()
gridOptions = gb.build()

# 显示可筛选的表格
grid_response = AgGrid(
    df,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT',
    update_mode=GridUpdateMode.MODEL_CHANGED,
    fit_columns_on_grid_load=False,
    enable_enterprise_modules=True,
    height=500,
    width='100%',
    reload_data=True,
    theme='streamlit'
)

# 获取选中的行
selected_rows = grid_response['selected_rows']

# 如果有选中的行，显示地图
if selected_rows:
    st.markdown("### 地图展示 - 选中布设点")

    # 转换为DataFrame
    selected_df = pd.DataFrame(selected_rows)

    # 检查是否有经纬度数据
    has_coords = (~selected_df['纬度'].isna()) & (~selected_df['经度'].isna())

    if has_coords.any():
        # 过滤出有经纬度的数据
        map_df = selected_df[has_coords].copy()

        # 创建地图数据
        map_data = map_df[['纬度', '经度', 'site_id', '调查样区', '省份', '城市', '县区']]

        # 显示地图
        st.map(map_data, latitude='纬度', longitude='经度', size=10, color='#00aaff')
    else:
        st.warning("选中的布设点没有可用的经纬度数据来显示地图")

# 显示筛选后的数据统计
if grid_response['filter_model']:
    st.markdown("### 筛选统计")
    st.write(f"当前筛选条件下共有 {len(grid_response['data'])} 条记录")
