# 野生动物监测数据集管理系统

## 简介

这是一个基于 Streamlit 的野生动物监测数据集管理系统，用于浏览、标注和分析野生动物监测数据。

## 系统要求

- Python 3.7 或更高版本
- MySQL 数据库
- 网络连接（用于安装依赖）

## 安装步骤

1. **克隆或下载项目**

   将整个项目文件夹复制到您选择的目录。

2. **安装依赖**

   打开命令行工具（Windows上的命令提示符或PowerShell），导航到项目目录，然后运行：

   ```
   pip install -r requirements.txt
   ```

3. **配置数据库连接**

   编辑 `config/db_config.py` 文件，设置您的MySQL数据库连接信息：

   ```python
   DB_CONFIG = {
       'host': 'localhost',      # 数据库服务器地址
       'user': 'your_username',  # 数据库用户名
       'password': 'your_password', # 数据库密码
       'database': 'your_database'  # 数据库名称
   }
   ```

4. **启动应用**

   有两种方式启动应用：

   - **方式一：使用 start_app.py**
     ```
     python start_app.py
     ```

   - **方式二：直接使用 Streamlit**
     ```
     streamlit run app.py
     ```

5. **访问应用**

   启动后，应用会在默认浏览器中打开，或访问 http://localhost:8501

## 功能模块

- 📊 数据库结构：查看数据库表结构
- 🗂️ 数据浏览：浏览野生动物监测数据
- ✏️ 人工标注：对数据进行人工标注
- 📈 数据分析：分析监测数据
- 📥 数据导入：导入新数据

