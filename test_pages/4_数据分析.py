import streamlit as st
import pandas as pd
import plotly.express as px
from services.db import get_connection

st.header("📊 数据分析")

# 获取数据
conn = get_connection()

# 标签页
tab1, tab2, tab3, tab4, tab5 = st.tabs(["物种分布", "时间分析", "地点分析", "植被类型分析", "水源类型分析"])

with tab1:
    st.subheader("物种分布")

    # 物种数量统计
    species_df = pd.read_sql("""
        SELECT s.中文名, s.学名, COUNT(a.annotation_id) as 数量
        FROM species s
        LEFT JOIN annotations a ON s.species_id = a.species_id
        GROUP BY s.species_id
        ORDER BY 数量 DESC
    """, conn)

    # 饼图
    fig = px.pie(
        species_df.head(10), 
        values='数量', 
        names='中文名',
        title='前10种最常见动物'
    )
    st.plotly_chart(fig, use_container_width=True)

    # 表格
    st.dataframe(species_df, use_container_width=True)

with tab2:
    st.subheader("活动时间分析")

    # 按月统计
    monthly_df = pd.read_sql("""
        SELECT MONTH(拍摄时间) as 月份, COUNT(*) as 数量
        FROM images i
        WHERE 拍摄时间 IS NOT NULL
        GROUP BY MONTH(拍摄时间)
        ORDER BY 月份
    """, conn)

    # 柱状图
    fig = px.bar(
        monthly_df, 
        x='月份', 
        y='数量',
        title='每月活动数量'
    )
    st.plotly_chart(fig, use_container_width=True)

    # 按小时统计
    hourly_df = pd.read_sql("""
        SELECT HOUR(拍摄时间) as 小时, COUNT(*) as 数量
        FROM images i
        WHERE 拍摄时间 IS NOT NULL
        GROUP BY HOUR(拍摄时间)
        ORDER BY 小时
    """, conn)

    # 柱状图
    fig = px.bar(
        hourly_df, 
        x='小时', 
        y='数量',
        title='每小时活动数量'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("地点分析")

    # 布设点统计
    deployment_df = pd.read_sql("""
        SELECT c.相机编号, s.样区名称, COUNT(i.image_id) as 图像数量
        FROM camera_deployments cd
        JOIN cameras c ON cd.camera_id = c.camera_id
        JOIN sites s ON cd.site_id = s.site_id
        LEFT JOIN images i ON cd.deployment_id = i.deployment_id
        GROUP BY cd.deployment_id
        ORDER BY 图像数量 DESC
    """, conn)

    # 表格
    st.dataframe(deployment_df, use_container_width=True)

    # 地图（如果有经纬度数据）
    if '纬度' in deployment_df.columns and '经度' in deployment_df.columns:
        fig = px.scatter_mapbox(
            deployment_df,
            lat="纬度",
            lon="经度",
            hover_name="相机编号",
            hover_data=["图像数量"],
            color="图像数量",
            size="图像数量",
            zoom=10,
            mapbox_style="open-street-map"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("植被类型分析")

    # 植被类型统计
    vegetation_df = pd.read_sql("""
        SELECT vt.植被类型, COUNT(s.site_id) as 布设点数量
        FROM vegetation_types vt
        LEFT JOIN site_vegetation_types svt ON vt.vegetation_id = svt.vegetation_id
        LEFT JOIN sites s ON svt.site_id = s.site_id
        GROUP BY vt.vegetation_id
        ORDER BY 布设点数量 DESC
    """, conn)

    # 饼图
    fig = px.pie(
        vegetation_df,
        values='布设点数量',
        names='植被类型',
        title='各植被类型布设点分布'
    )
    st.plotly_chart(fig, use_container_width=True)

    # 表格
    st.dataframe(vegetation_df, use_container_width=True)

with tab5:
    st.subheader("水源类型分析")

    # 水源类型统计
    water_source_df = pd.read_sql("""
        SELECT ws.水源类型, COUNT(s.site_id) as 布设点数量
        FROM water_source_types ws
        LEFT JOIN site_water_source_types swst ON ws.water_source_id = swst.water_source_id
        LEFT JOIN sites s ON swst.site_id = s.site_id
        GROUP BY ws.water_source_id
        ORDER BY 布设点数量 DESC
    """, conn)

    # 饼图
    fig = px.pie(
        water_source_df,
        values='布设点数量',
        names='水源类型',
        title='各水源类型布设点分布'
    )
    st.plotly_chart(fig, use_container_width=True)

    # 表格
    st.dataframe(water_source_df, use_container_width=True)

conn.close()
