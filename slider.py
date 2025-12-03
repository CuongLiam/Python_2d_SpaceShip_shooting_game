"""
Slider UI class for Alien Invasion Ultimate.
Handles volume control in menus.
"""
import pygame


class Slider:
    """
    UI Slider for volume control.
    """
    def __init__(self, ai_game, x, y, width, height, initial_value):
        """Khởi tạo thanh trượt."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Hình chữ nhật nền (màu xám)
        self.rect = pygame.Rect(x, y, width, height)
        self.color_bg = (100, 100, 100)

        # Hình chữ nhật hiển thị mức độ (màu xanh)
        self.color_fill = (0, 200, 200)
        self.current_value = initial_value  # Giá trị từ 0.0 đến 1.0

        # Label (Chữ hiển thị bên cạnh)
        self.font = pygame.font.SysFont(None, 36)
        self.text_image = self.font.render("Volume", True, (50, 50, 50))
        self.text_rect = self.text_image.get_rect()
        self.text_rect.right = self.rect.left - 20
        self.text_rect.centery = self.rect.centery

    def draw_slider(self):
        """Vẽ thanh trượt lên màn hình."""
        # Vẽ chữ "Volume"
        self.screen.blit(self.text_image, self.text_rect)

        # Vẽ nền
        pygame.draw.rect(self.screen, self.color_bg, self.rect)

        # Tính toán độ dài phần fill dựa trên giá trị hiện tại
        fill_width = self.rect.width * self.current_value
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)

        # Vẽ phần fill
        pygame.draw.rect(self.screen, self.color_fill, fill_rect)

        # Vẽ viền
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)

    def check_click(self, mouse_pos):
        """Nếu click vào thanh trượt, cập nhật giá trị."""
        if self.rect.collidepoint(mouse_pos):
            # Tính tỉ lệ vị trí click so với chiều rộng thanh
            relative_x = mouse_pos[0] - self.rect.x
            self.current_value = relative_x / self.rect.width

            # Giới hạn giá trị trong khoảng 0.0 - 1.0
            if self.current_value < 0: self.current_value = 0
            if self.current_value > 1: self.current_value = 1

            return True  # Đã thay đổi
        return False