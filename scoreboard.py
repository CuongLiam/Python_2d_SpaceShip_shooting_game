import pygame.font
from pygame.sprite import Group
from sprites.ship import Ship

"""
Scoreboard UI for Alien Invasion Ultimate.
Displays score, high score, level, and lives.
"""

class Scoreboard:
    """
    Handles rendering of score, high score, level, and lives.
    """
    """Class để báo cáo thông tin điểm số."""

    def __init__(self, ai_game):
        """Khởi tạo các thuộc tính chấm điểm."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Cài đặt font chữ
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Chuẩn bị ảnh điểm số ban đầu
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Biến điểm số thành hình ảnh."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)

        # Hiển thị điểm ở góc phải trên cùng
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Biến điểm cao nhất thành hình ảnh."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)

        # Căn giữa điểm cao ở trên cùng
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Biến level thành hình ảnh."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(f"Lv {level_str}", True,
                self.text_color, self.settings.bg_color)

        # Đặt level bên dưới điểm số
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Hiển thị số tàu còn lại (mạng)."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            # Thu nhỏ tàu một chút để làm biểu tượng mạng
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        """Kiểm tra xem có kỷ lục mới không."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Vẽ điểm số, level và tàu lên màn hình."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)