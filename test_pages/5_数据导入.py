import streamlit as st
import os
import pandas as pd
from services.db import get_connection

st.header("📥 数据导入")

# 标签页
tab1, tab2, tab3, tab4, tab5 = st.tabs(["图像导入", "物种导入", "植物物种导入", "植被类型导入", "水源类型导入"])

with tab1:
    st.subheader("图像数据导入")

    # 文件上传
    uploaded_file = st.file_uploader("选择图像元数据文件", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # 显示上传的文件
        st.write("文件已上传:")
        st.write(uploaded_file.name)

        # 预览数据
        df = pd.read_excel(uploaded_file)
        st.write("数据预览:")
        st.dataframe(df.head())

        # 导入按钮
        if st.button("导入图像数据"):
            with st.spinner("正在导入数据..."):
                conn = get_connection()
                cursor = conn.cursor()

                success_count = 0
                error_count = 0

                for index, row in df.iterrows():
                    try:
                        # 插入图像记录
                        sql = """
                        INSERT INTO images (
                            deployment_id, 文件路径, 视频路径, 拍摄时间,
                            分辨率, 文件哈希, 文件格式, 文件大小
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """

                        cursor.execute(sql, (
                            row.get('deployment_id'),
                            row.get('文件路径'),
                            row.get('视频路径'),
                            row.get('拍摄时间'),
                            row.get('分辨率'),
                            row.get('文件哈希'),
                            row.get('文件格式'),
                            row.get('文件大小')
                        ))

                        success_count += 1
                    except Exception as e:
                        st.error(f"导入第 {index+1} 行数据出错: {e}")
                        error_count += 1

                conn.commit()
                cursor.close()
                conn.close()

                st.success(f"导入完成! 成功: {success_count}, 失败: {error_count}")

with tab2:
    st.subheader("物种数据导入")

    # 文件上传
    uploaded_file = st.file_uploader("选择物种数据文件", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # 显示上传的文件
        st.write("文件已上传:")
        st.write(uploaded_file.name)

        # 预览数据
        df = pd.read_excel(uploaded_file)
        st.write("数据预览:")
        st.dataframe(df.head())

        # 导入按钮
        if st.button("导入物种数据"):
            with st.spinner("正在导入数据..."):
                conn = get_connection()
                cursor = conn.cursor()

                success_count = 0
                error_count = 0

                for index, row in df.iterrows():
                    try:
                        # 插入物种记录
                        sql = """
                        INSERT INTO species (
                            学名, 中文名, 保护等级, 纲, 目, 科, 备注
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            中文名 = VALUES(中文名),
                            保护等级 = VALUES(保护等级),
                            纲 = VALUES(纲),
                            目 = VALUES(目),
                            科 = VALUES(科)
                        """

                        cursor.execute(sql, (
                            row.get('学名'),
                            row.get('中文名'),
                            row.get('保护等级'),
                            row.get('纲'),
                            row.get('目'),
                            row.get('科'),
                            row.get('备注')
                        ))

                        success_count += 1
                    except Exception as e:
                        st.error(f"导入第 {index+1} 行数据出错: {e}")
                        error_count += 1

                conn.commit()
                cursor.close()
                conn.close()

                st.success(f"导入完成! 成功: {success_count}, 失败: {error_count}")

with tab3:
    st.subheader("植物物种数据导入")

    # 文件上传
    uploaded_file = st.file_uploader("选择植物物种数据文件", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # 显示上传的文件
        st.write("文件已上传:")
        st.write(uploaded_file.name)

        # 预览数据
        df = pd.read_excel(uploaded_file)
        st.write("数据预览:")
        st.dataframe(df.head())

        # 导入按钮
        if st.button("导入植物物种数据"):
            with st.spinner("正在导入数据..."):
                conn = get_connection()
                cursor = conn.cursor()

                success_count = 0
                error_count = 0

                for index, row in df.iterrows():
                    try:
                        # 插入植物物种记录
                        sql = """
                        INSERT INTO plant_species (
                            中文名, 拉丁名, 保护级别
                        ) VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            拉丁名 = VALUES(拉丁名),
                            保护级别 = VALUES(保护级别)
                        """

                        cursor.execute(sql, (
                            row.get('中文名'),
                            row.get('拉丁名'),
                            row.get('保护级别')
                        ))

                        success_count += 1
                    except Exception as e:
                        st.error(f"导入第 {index+1} 行数据出错: {e}")
                        error_count += 1

                conn.commit()
                cursor.close()
                conn.close()

                st.success(f"导入完成! 成功: {success_count}, 失败: {error_count}")

with tab4:
    st.subheader("植被类型数据导入")

    # 文件上传
    uploaded_file = st.file_uploader("选择植被类型数据文件", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # 显示上传的文件
        st.write("文件已上传:")
        st.write(uploaded_file.name)

        # 预览数据
        df = pd.read_excel(uploaded_file)
        st.write("数据预览:")
        st.dataframe(df.head())

        # 导入按钮
        if st.button("导入植被类型数据"):
            with st.spinner("正在导入数据..."):
                conn = get_connection()
                cursor = conn.cursor()

                success_count = 0
                error_count = 0

                for index, row in df.iterrows():
                    try:
                        # 插入植被类型记录
                        sql = """
                        INSERT INTO vegetation_types (
                            植被类型
                        ) VALUES (%s)
                        ON DUPLICATE KEY UPDATE
                            植被类型 = VALUES(植被类型)
                        """

                        cursor.execute(sql, (
                            row.get('植被类型'),
                        ))

                        success_count += 1
                    except Exception as e:
                        st.error(f"导入第 {index+1} 行数据出错: {e}")
                        error_count += 1

                conn.commit()
                cursor.close()
                conn.close()

                st.success(f"导入完成! 成功: {success_count}, 失败: {error_count}")

with tab5:
    st.subheader("水源类型数据导入")

    # 文件上传
    uploaded_file = st.file_uploader("选择水源类型数据文件", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # 显示上传的文件
        st.write("文件已上传:")
        st.write(uploaded_file.name)

        # 预览数据
        df = pd.read_excel(uploaded_file)
        st.write("数据预览:")
        st.dataframe(df.head())

        # 导入按钮
        if st.button("导入水源类型数据"):
            with st.spinner("正在导入数据..."):
                conn = get_connection()
                cursor = conn.cursor()

                success_count = 0
                error_count = 0

                for index, row in df.iterrows():
                    try:
                        # 插入水源类型记录
                        sql = """
                        INSERT INTO water_types (
                            水源类型
                        ) VALUES (%s)
                        ON DUPLICATE KEY UPDATE
                            水源类型 = VALUES(水源类型)
                        """

                        cursor.execute(sql, (
                            row.get('水源类型'),
                        ))

                        success_count += 1
                    except Exception as e:
                        st.error(f"导入第 {index+1} 行数据出错: {e}")
                        error_count += 1

                conn.commit()
                cursor.close()
                conn.close()

                st.success(f"导入完成! 成功: {success_count}, 失败: {error_count}")
