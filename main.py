import sys
import pygame
from settings import Settings
from sprites.ship import Ship
from sprites.bullet import Bullet
from sprites.alien import Alien


class AlienInvasion:
    """Class chính quản lý game"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion Ultimate")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # --- THÊM 2 DÒNG NÀY VÀO ĐÂY ---
        self.aliens = pygame.sprite.Group()  # Tạo nhóm Alien
        self._create_fleet()  # Gọi hàm tạo hạm đội
        # -------------------------------

    def run_game(self):
        """Vòng lặp chính của game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()  # <--- MỚI: Hàm riêng để cập nhật đạn
            self._update_aliens()  # <--- MỚI: Cập nhật vị trí alien
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:  # <--- MỚI: Nhấn Space để bắn
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):  # <--- MỚI: Logic bắn đạn
        """Tạo viên đạn mới và thêm vào nhóm bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Cập nhật vị trí đạn và xóa đạn cũ"""
        self.bullets.update()

        # Xóa đạn đã biến mất khỏi màn hình
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # --- CODE MỚI: XỬ LÝ VA CHẠM (COLLISION) ---
        self._check_bullet_alien_collisions()
        # -------------------------------------------

    # --- THÊM HÀM MỚI NÀY VÀO DƯỚI CÙNG HOẶC GẦN CÁC HÀM UPDATE ---
    def _check_bullet_alien_collisions(self):
        """Xử lý va chạm giữa đạn và alien"""
        # Hàm groupcollide kiểm tra va chạm giữa 2 nhóm (bullets và aliens)
        # True thứ nhất: Xóa đạn khi va chạm? -> Có (True)
        # True thứ hai: Xóa Alien khi va chạm? -> Có (True)
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        # Nếu hạm đội bị diệt sạch -> Tạo hạm đội mới
        if not self.aliens:
            # Xóa hết đạn đang bay (tùy chọn)
            self.bullets.empty()
            # Tạo hạm đội mới
            self._create_fleet()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # <--- MỚI: Vẽ tất cả các viên đạn
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    # --- CÁC HÀM MỚI TRONG CLASS AlienInvasion ---

    def _create_fleet(self):
        """Tạo hạm đội alien"""
        # Tạo một alien để lấy kích thước
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Tính toán số alien trên 1 hàng
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Tính toán số hàng
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Tạo lưới alien
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Tạo một alien và đặt nó vào hàng"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Kiểm tra chạm mép và cập nhật vị trí toàn hạm đội"""
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """Phản ứng khi có alien chạm mép"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Thả toàn bộ hạm đội xuống và đổi hướng"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()