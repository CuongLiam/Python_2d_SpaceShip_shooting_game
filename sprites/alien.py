import pygame
from pygame.sprite import Sprite
from settings import get_resource_path

class Alien(Sprite):
    """Lớp đại diện cho một con alien đơn lẻ"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load ảnh alien
        image_path = get_resource_path('assets/images/alien.png') # Hoặc .bmp tùy bạn
        self.image = pygame.image.load(image_path).convert_alpha()

        # --- THÊM ĐOẠN NÀY ĐỂ THU NHỎ ẢNH ---
        # Thu nhỏ alien về kích thước chuẩn (ví dụ: 60x60 pixels)
        # Nếu không có dòng này, ảnh gốc quá to sẽ khiến hạm đội không xuất hiện
        self.image = pygame.transform.scale(self.image, (60, 60))
        # -------------------------------------

        self.rect = self.image.get_rect()

        # Đặt alien ở góc trái trên cùng
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        """Trả về True nếu alien chạm mép màn hình"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self):
        """Di chuyển alien sang phải hoặc trái"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x