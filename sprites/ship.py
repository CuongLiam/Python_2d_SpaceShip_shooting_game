import pygame
from settings import get_resource_path  # Import hàm tìm đường dẫn

class Ship:
    def __init__(self, ai_game):
        """Khởi tạo tàu và vị trí ban đầu"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load ảnh tàu (Dùng hàm get_resource_path để không lỗi khi build exe)
        image_path = get_resource_path('assets/images/ship.bmp')
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        # Đặt tàu ở giữa đáy màn hình
        self.rect.midbottom = self.screen_rect.midbottom

        # Lưu vị trí dưới dạng số thực (float) để di chuyển mượt hơn
        self.x = float(self.rect.x)

        # Cờ di chuyển
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Cập nhật vị trí tàu dựa trên cờ di chuyển"""
        # Cập nhật giá trị x (float)
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Cập nhật lại rect từ giá trị x
        self.rect.x = self.x

    def blitme(self):
        """Vẽ tàu tại vị trí hiện tại"""
        self.screen.blit(self.image, self.rect)