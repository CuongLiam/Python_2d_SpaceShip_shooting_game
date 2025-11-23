import pygame
from pygame.sprite import Sprite  # <--- 1. THÊM DÒNG NÀY
from settings import get_resource_path


class Ship(Sprite):  # <--- 2. SỬA THÀNH Ship(Sprite)
    def __init__(self, ai_game):
        """Khởi tạo tàu và vị trí ban đầu"""
        super().__init__()  # <--- 3. THÊM DÒNG NÀY (QUAN TRỌNG)

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load ảnh tàu
        try:
            image_path = get_resource_path('assets/images/ship.bmp')
            # Nếu dùng png thì thêm .convert_alpha()
            self.image = pygame.image.load(image_path)
        except FileNotFoundError:
            # Fallback nếu không có ảnh
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect()

        # Đặt tàu ở giữa đáy màn hình
        self.rect.midbottom = self.screen_rect.midbottom

        # Lưu vị trí dưới dạng số thực
        self.x = float(self.rect.x)

        # Cờ di chuyển
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Cập nhật vị trí tàu dựa trên cờ di chuyển"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """Vẽ tàu tại vị trí hiện tại"""
        self.screen.blit(self.image, self.rect)

    # --- THÊM HÀM NÀY ĐỂ RESET TÀU KHI CHẾT ---
    def center_ship(self):
        """Đặt tàu về giữa màn hình."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)