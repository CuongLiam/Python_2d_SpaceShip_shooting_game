"""
Game statistics tracking for Alien Invasion Ultimate.
Tracks score, level, lives, and high score.
"""

class GameStats:
    """
    Tracks game statistics: score, level, lives, high score.
    """
    """Theo dõi các thống kê của game Alien Invasion."""

    def __init__(self, ai_game):
        """Khởi tạo các thống kê."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Bắt đầu game ở trạng thái không hoạt động (để hiện Menu)
        self.game_active = False

        # Điểm cao nhất (High Score) - Không reset khi chết
        self.high_score = 0

    def reset_stats(self):
        """Khởi tạo lại các thống kê thay đổi trong quá trình chơi."""
        self.score = 0
        self.level = 1
        self.ships_left = self.settings.ship_limit