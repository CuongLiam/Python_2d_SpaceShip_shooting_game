"""
Settings and configuration for Alien Invasion Ultimate.
Handles screen, difficulty, speed, and audio settings.
"""
import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Settings:
    """
    Stores all game settings and handles difficulty changes.
    """
    """Lưu trữ mọi cài đặt của game"""

    def __init__(self):
        # --- CÀI ĐẶT MÀN HÌNH ---
        self.screen_width = 1200
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # --- CÀI ĐẶT TÀU ---
        self.ship_limit = 3

        # --- CÀI ĐẶT ĐẠN ---
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # --- CÀI ĐẶT ALIEN ---
        self.fleet_drop_speed = 10

        # --- CÀI ĐẶT ÂM THANH (MỚI) ---
        # Chỉnh số nhỏ hơn để giảm âm (0.0 đến 1.0)
        self.music_volume = 0.2  # Nhạc nền (20%)
        self.sfx_volume = 0.3    # Tiếng súng/nổ (30%)

        # --- TỈ LỆ TĂNG TỐC ---
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.difficulty_level = 'normal' # Mặc định
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Khởi tạo cài đặt dựa trên độ khó hiện tại."""
        # Tốc độ cơ bản
        if self.difficulty_level == 'easy':
            self.ship_speed = 2.0
            self.bullet_speed = 3.0
            self.alien_speed = 0.1   # Alien đi chậm
            self.alien_points = 50
        elif self.difficulty_level == 'normal':
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.alien_speed = 0.1
            self.alien_points = 50
        elif self.difficulty_level == 'hard':
            self.ship_speed = 3.0    # Tàu chạy nhanh để né
            self.bullet_speed = 4.0
            self.alien_speed = 0.5  # Alien chạy rất nhanh
            self.alien_points = 100  # Điểm thưởng cao hơn

        self.fleet_direction = 1

    def set_difficulty(self, difficulty):
        """Hàm thay đổi độ khó."""
        self.difficulty_level = difficulty
        self.initialize_dynamic_settings()

    def increase_speed(self):
        """Tăng tốc độ game sau mỗi màn."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)