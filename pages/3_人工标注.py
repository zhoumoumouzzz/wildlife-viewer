import streamlit as st
import os
import sys
import uuid
from pathlib import Path
import sqlite3

st.set_page_config(layout="wide")

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.images_service import get_images
from services.species_service import get_species_list
try:
    from services.behaviors_service import get_behaviors_list
except ImportError:
    def get_behaviors_list():
        return []
from services.annotations_service import insert_annotation
from services.db import get_db_connection

def process_media_path(original_path):
    """处理媒体路径，尝试多种可能的格式和路径转换"""
    if not original_path:
        return None
    path_obj = Path(original_path)
    if path_obj.exists():
        return str(path_obj)
    try:
        normalized_path = os.path.normpath(original_path)
        if os.path.exists(normalized_path):
            return normalized_path
    except Exception:
        pass
    return original_path

def display_image(image_path, caption="", width=None, use_column_width=False):
    """高质量显示图像"""
    try:
        from PIL import Image
        import io
        with open(image_path, "rb") as f:
            image_data = f.read()
        image = Image.open(io.BytesIO(image_data))
        width_orig, height_orig = image.size
        if width and width_orig > width:
            ratio = width / width_orig
            new_height = int(height_orig * ratio)
            image = image.resize((width, new_height), Image.LANCZOS)
        st.image(image, caption=f"{caption} (原始尺寸: {width_orig}x{height_orig})", use_column_width=use_column_width)
        return True
    except Exception as e:
        st.error(f"加载图片失败: {str(e)}")
        st.image(image_path, width=width, caption=caption)
        return False

# 页面标题
st.header("✏️ 人工标注")

# --- 核心修改 1：获取图像并强制转为字典以支持 .get() ---
images_raw = get_images(limit=1000, only_unconfirmed=True)
images = [dict(row) for row in images_raw]

# 获取物种列表
species_list_raw = get_species_list()
species_list = [dict(row) for row in species_list_raw]
species_map = {s['species_id']: f"{s['中文名']} ({s['学名']})" for s in species_list}

if not images:
    st.info("没有找到符合条件的图像")
else:
    st.info(f"找到 {len(images)} 张图像")
    camera_numbers = list(set([img['相机编号'] for img in images]))
    selected_camera = st.selectbox("选择相机编号", camera_numbers)
    camera_images = [img for img in images if img['相机编号'] == selected_camera]

    if 'selected_image_index' not in st.session_state:
        st.session_state.selected_image_index = 0
        st.session_state.selected_camera = selected_camera

    if st.session_state.selected_camera != selected_camera:
        st.session_state.selected_image_index = 0
        st.session_state.selected_camera = selected_camera

    selected_image = camera_images[st.session_state.selected_image_index]

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("上一张") and st.session_state.selected_image_index > 0:
            st.session_state.selected_image_index -= 1
            st.rerun()
    with col3:
        if st.button("下一张") and st.session_state.selected_image_index < len(camera_images) - 1:
            st.session_state.selected_image_index += 1
            st.rerun()

    with col2:
        st.markdown(f"<h5 style='text-align: center'>图像 {st.session_state.selected_image_index + 1} / {len(camera_images)}</h5>", unsafe_allow_html=True)

    st.subheader("图像信息")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"**图像ID:** {selected_image['image_id']}")
        st.markdown(f"**相机编号:** {selected_image['相机编号']}")
        st.markdown(f"**拍摄时间:** {selected_image['拍摄时间']}")

        image_path = selected_image["文件路径"]
        if image_path:
            found_path = process_media_path(image_path)
            if found_path and os.path.exists(found_path):
                st.markdown(f"**图像路径:** `{found_path}`")
            else:
                st.error(f"找不到图像文件: {image_path}")

        # 此处现在支持 .get() 了
        video_path = selected_image.get("视频路径", "")
        if video_path:
            found_video_path = process_media_path(video_path)
            if found_video_path and os.path.exists(found_video_path):
                st.markdown(f"**视频路径:** `{found_video_path}`")
                with open(found_video_path, "rb") as file:
                    st.download_button(label="下载视频", data=file.read(), file_name=os.path.basename(found_video_path), mime="video/mp4")

    with col2:
        if image_path:
            found_path = process_media_path(image_path)
            if found_path and os.path.exists(found_path):
                display_image(found_path, caption=f"图像 {selected_image['image_id']}", width=400)

    st.divider()

    # --- 核心修改 2：已有标注获取（占位符兼容） ---
    conn = get_db_connection()
    if isinstance(conn, sqlite3.Connection):
        cursor = conn.cursor()
        placeholder = "?"
    else:
        cursor = conn.cursor(dictionary=True)
        placeholder = "%s"

    cursor.execute(f"""
        SELECT a.*, s.中文名, s.学名
        FROM annotations a
        LEFT JOIN species s ON a.species_id = s.species_id
        WHERE a.image_id = {placeholder}
    """, (selected_image['image_id'],))
    
    annotations_raw = cursor.fetchall()
    annotations = [dict(row) for row in annotations_raw]
    cursor.close()
    conn.close()

    if annotations:
        st.subheader("已有标注")
        for ann in annotations:
            with st.expander(f"标注 {ann['annotation_id']} - {'已确认' if ann['是否人工确认'] else '待确认'}"):
                st.write(f"**物种:** {ann['中文名']} ({ann['学名']})")
                if ann.get('behavior_name'): st.write(f"**行为:** {ann['behavior_name']}")

    if st.button("添加标注"):
        st.session_state.show_annotation_form = True
        st.session_state.current_image_id = selected_image['image_id']
        st.rerun()

    if st.session_state.get('show_annotation_form', False) and st.session_state.get('current_image_id', -1) == selected_image['image_id']:
        st.subheader("添加新标注")
        with st.form("annotation_form"):
            col1, col2 = st.columns(2)
            with col1:
                selected_species = st.selectbox("选择物种*", ["未识别"] + list(species_map.values()))
                try:
                    behaviors_raw = get_behaviors_list()
                    behaviors = [dict(row) for row in behaviors_raw]
                    behaviors_map = {b['behavior_id']: b['行为名称'] for b in behaviors}
                    selected_behavior = st.selectbox("选择行为", ["无"] + list(behaviors_map.values()))
                except:
                    selected_behavior = "无"; behaviors_map = {}
                animal_count = st.number_input("动物数量", min_value=1, value=1)
            with col2:
                age_group = st.selectbox("年龄组", ["未知", "幼体", "亚成体", "成体", "老年"])
                gender = st.selectbox("性别", ["未知", "雄性", "雌性", "混合"])
                confirmer = st.text_input("确认人*")
            note = st.text_area("备注")
            is_confirmed = st.checkbox("标记为已确认", value=True)

            if st.form_submit_button("保存标注"):
                if not confirmer:
                    st.error("请填写确认人")
                else:
                    species_id = next((k for k, v in species_map.items() if v == selected_species), None) if selected_species != "未识别" else None
                    behavior_id = next((k for k, v in behaviors_map.items() if v == selected_behavior), None) if selected_behavior != "无" else None
                    try:
                        insert_annotation(image_id=selected_image['image_id'], species_id=species_id, behavior_id=behavior_id,
                                          animal_count=animal_count, age_group=age_group, gender=gender,
                                          confirmer=confirmer, note=note, is_confirmed=is_confirmed)
                        st.success("标注已保存")
                        st.session_state.show_annotation_form = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"保存标注失败: {str(e)}")
            if st.form_submit_button("取消"):
                st.session_state.show_annotation_form = False
                st.rerun()