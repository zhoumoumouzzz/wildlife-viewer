import os
import sys
import subprocess
from pathlib import Path

def main():
    """主函数，启动应用"""
    print("正在启动野生动物图片查看器...")

    # 获取当前脚本所在目录作为应用目录
    app_dir = Path(__file__).parent.resolve()
    os.chdir(app_dir)
    print(f"切换到应用目录: {app_dir}")

    # 启动Streamlit应用
    print("启动Streamlit应用...")
    try:
        subprocess.run(["streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"启动应用失败: {e}")
        input("按Enter键退出...")
        sys.exit(1)
    except FileNotFoundError:
        print("找不到streamlit命令，请确保已安装streamlit")
        input("按Enter键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
