import os
import sys


# Bạn có thể bỏ import pygame ở đây nếu muốn, vì file này chỉ chứa số liệu

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

        # Cài đặt Đạn
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Cài đặt Alien
        self.alien_speed = 0.1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        # --- KHÔNG ĐƯỢC CÓ self.bullets, self.aliens HAY self._create_fleet() Ở ĐÂY ---