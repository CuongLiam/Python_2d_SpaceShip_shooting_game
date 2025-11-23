import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Lớp quản lý đạn được bắn từ tàu"""

    def __init__(self, ai_game):
        """Tạo một viên đạn tại vị trí hiện tại của tàu"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Tạo hình chữ nhật cho đạn tại (0, 0) rồi thiết lập vị trí đúng
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)

        # Đặt đạn ở giữa-trên của con tàu
        self.rect.midtop = ai_game.ship.rect.midtop

        # Lưu vị trí y dưới dạng số thực để chỉnh tốc độ mượt hơn
        self.y = float(self.rect.y)

    def update(self):
        """Di chuyển đạn lên trên màn hình"""
        # Cập nhật vị trí thập phân
        # Trong Pygame, tọa độ (0,0) là góc trên cùng bên trái.
        # Muốn đi lên thì phải GIẢM giá trị y.
        self.y -= self.settings.bullet_speed

        # Cập nhật lại rect
        self.rect.y = self.y

    def draw_bullet(self):
        """Vẽ đạn lên màn hình"""
        pygame.draw.rect(self.screen, self.color, self.rect)