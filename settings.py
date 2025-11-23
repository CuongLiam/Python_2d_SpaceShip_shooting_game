import os
import sys

def get_resource_path(relative_path):
    """Hàm tìm đường dẫn file, dùng được cho cả lúc code và lúc chạy .exe"""
    try:
        base_path = sys._MEIPASS  # PyInstaller tạo ra cái này
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)