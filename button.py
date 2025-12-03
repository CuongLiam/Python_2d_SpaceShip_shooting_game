"""
Button UI class for Alien Invasion Ultimate.
Handles rendering and interaction for menu and game buttons.
"""
import pygame.font

class Button:
    """
    UI Button for menus and game controls.
    """
    def __init__(self, ai_game, msg):
        """Khởi tạo các thuộc tính của nút bấm."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Kích thước và thuộc tính của nút
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0) # Màu xanh lá
        self.text_color = (255, 255, 255) # Chữ trắng
        self.font = pygame.font.SysFont(None, 48) # Font mặc định, cỡ 48

        # Tạo rect của nút và căn giữa màn hình
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Chuẩn bị thông điệp (msg) cần hiển thị
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Biến text thành ảnh (rendered image) và căn giữa nút."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Vẽ nút trống xong rồi vẽ text lên trên."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)