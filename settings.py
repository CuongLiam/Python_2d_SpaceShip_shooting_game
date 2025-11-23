import os
import sys

def get_resource_path(relative_path):
    """Hàm tìm đường dẫn file, dùng được cho cả lúc code và lúc chạy .exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Settings:
    """Lưu trữ mọi cài đặt của game"""

    def __init__(self):
        # Cài đặt màn hình
        self.screen_width = 1200
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # Cài đặt Tàu
        self.ship_speed = 1.5

        # --- THÊM ĐOẠN NÀY ---
        # Cài đặt Đạn
        self.bullet_speed = 2.0  # Tốc độ đạn (nhanh hơn tàu chút)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)  # Màu xám đậm
        self.bullets_allowed = 3  # Giới hạn số đạn trên màn hình (để không spam nút bắn)