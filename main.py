import sys
import pygame
"""
Alien Invasion Ultimate - Main Game File
This file contains the main game loop, event handling, menu logic, and core gameplay mechanics.
"""
from time import sleep

from settings import Settings, get_resource_path
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from slider import Slider
from sprites.ship import Ship
from sprites.bullet import Bullet
from sprites.alien import Alien


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion Ultimate")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # --- MENU CHÍNH ---
        self.btn_play = Button(self, "Play Game")
        self.btn_settings = Button(self, "Settings")
        self.btn_settings.rect.top = self.btn_play.rect.bottom + 20
        self.btn_settings.msg_image_rect.center = self.btn_settings.rect.center

        # --- MENU SETTINGS (ĐỘ KHÓ) ---
        center_x = self.screen.get_rect().centerx
        self.btn_easy = Button(self, "Easy")
        self.btn_normal = Button(self, "Normal")
        self.btn_hard = Button(self, "Hard")
        self.btn_back = Button(self, "< Back")

        self.btn_easy.rect.center = (center_x, 300)
        self.btn_easy.msg_image_rect.center = self.btn_easy.rect.center
        self.btn_normal.rect.center = (center_x, 400)
        self.btn_normal.msg_image_rect.center = self.btn_normal.rect.center
        self.btn_hard.rect.center = (center_x, 500)
        self.btn_hard.msg_image_rect.center = self.btn_hard.rect.center
        self.btn_back.rect.center = (center_x, 600)
        self.btn_back.msg_image_rect.center = self.btn_back.rect.center

        # --- MENU PAUSE (MỚI) ---
        self.paused = False  # Trạng thái Pause
        self.btn_resume = Button(self, "Resume")
        self.btn_reset = Button(self, "Reset Level")

        # Đặt vị trí nút Pause
        self.btn_resume.rect.center = (center_x, 300)
        self.btn_resume.msg_image_rect.center = self.btn_resume.rect.center

        self.btn_reset.rect.center = (center_x, 400)
        self.btn_reset.msg_image_rect.center = self.btn_reset.rect.center

        # Thanh Slider Âm lượng (x, y, width, height, value)
        self.volume_slider = Slider(self, center_x - 100, 500, 200, 30, self.settings.music_volume)

        self.menu_state = 'main'

        # --- LOAD ÂM THANH ---
        try:
            self.sound_laser = pygame.mixer.Sound(get_resource_path('assets/sounds/laser.wav'))
            self.sound_explosion = pygame.mixer.Sound(get_resource_path('assets/sounds/explosion.wav'))
            pygame.mixer.music.load(get_resource_path('assets/sounds/background_music.mp3'))

            # Cập nhật volume ban đầu
            self._update_volume(self.settings.music_volume)

        except Exception as e:
            print(f"Warning: Audio error ({e})")
            self.sound_laser = None
            self.sound_explosion = None

    def _update_volume(self, volume):
        """Cập nhật âm lượng cho nhạc và sfx."""
        # Cập nhật biến settings
        self.settings.music_volume = volume
        self.settings.sfx_volume = volume  # Giả sử sfx volume bằng nhạc nền cho đơn giản

        # Cập nhật Mixer
        pygame.mixer.music.set_volume(volume)
        if self.sound_laser: self.sound_laser.set_volume(volume)
        if self.sound_explosion: self.sound_explosion.set_volume(volume)

    def run_game(self):
        while True:
            self._check_events()

            # Logic: Nếu đang chơi VÀ KHÔNG PAUSE thì mới cập nhật chuyển động
            if self.stats.game_active and not self.paused:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_click_buttons(mouse_pos)

            # --- XỬ LÝ KÉO THẢ THANH SLIDER (MỚI) ---
            elif event.type == pygame.MOUSEMOTION:
                if self.paused and pygame.mouse.get_pressed()[0]:  # Nếu đang giữ chuột trái
                    mouse_pos = pygame.mouse.get_pos()
                    if self.volume_slider.check_click(mouse_pos):
                        self._update_volume(self.volume_slider.current_value)

    def _check_click_buttons(self, mouse_pos):
        # 1. XỬ LÝ KHI ĐANG PAUSE (Ưu tiên cao nhất)
        if self.paused:
            if self.btn_resume.rect.collidepoint(mouse_pos):
                self.paused = False  # Tiếp tục chơi
                pygame.mouse.set_visible(False)
            elif self.btn_reset.rect.collidepoint(mouse_pos):
                self._reset_level()  # Chơi lại level
            elif self.volume_slider.check_click(mouse_pos):
                self._update_volume(self.volume_slider.current_value)
            return  # Dừng hàm, không check các nút khác

        # 2. XỬ LÝ MENU CHÍNH
        if not self.stats.game_active:
            if self.menu_state == 'main':
                if self.btn_play.rect.collidepoint(mouse_pos):
                    self._start_game()
                elif self.btn_settings.rect.collidepoint(mouse_pos):
                    self.menu_state = 'settings'
            elif self.menu_state == 'settings':
                if self.btn_easy.rect.collidepoint(mouse_pos):
                    self.settings.set_difficulty('easy')
                    self._start_game()
                elif self.btn_normal.rect.collidepoint(mouse_pos):
                    self.settings.set_difficulty('normal')
                    self._start_game()
                elif self.btn_hard.rect.collidepoint(mouse_pos):
                    self.settings.set_difficulty('hard')
                    self._start_game()
                elif self.btn_back.rect.collidepoint(mouse_pos):
                    self.menu_state = 'main'

    def _start_game(self):
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self._reset_level()  # Dùng hàm chung để tạo màn
        if pygame.mixer.get_init():
            pygame.mixer.music.play(-1)

    def _reset_level(self):
        """Reset lại màn chơi (xóa alien, đạn, đặt lại tàu)."""
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        self.paused = False
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            # Chỉ bắn khi không pause
            if not self.paused:
                self._fire_bullet()

        # --- NÚT PAUSE (MỚI) ---
        elif event.key == pygame.K_p:  # Nhấn P để Pause/Resume
            if self.stats.game_active:
                self.paused = not self.paused
                if self.paused:
                    pygame.mouse.set_visible(True)  # Hiện chuột để chỉnh
                else:
                    pygame.mouse.set_visible(False)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            if self.sound_explosion:
                self.sound_explosion.play()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self._reset_level()  # Tái sử dụng hàm reset
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.menu_state = 'main'
            self.paused = False  # Hủy pause nếu game over
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # ... (Giữ nguyên phần fire bullet nếu chưa có) ...
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            if self.sound_laser:
                self.sound_laser.play()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        # --- VẼ GIAO DIỆN ---

        # 1. Vẽ Menu Pause (Khi đang chơi mà bấm P)
        if self.paused:
            # Vẽ màn mờ (Overlay)
            overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
            overlay.set_alpha(128)  # Độ trong suốt
            overlay.fill((0, 0, 0))  # Màu đen
            self.screen.blit(overlay, (0, 0))

            # Vẽ nút
            self.btn_resume.draw_button()
            self.btn_reset.draw_button()

            # Vẽ thanh volume
            self.volume_slider.draw_slider()

        # 2. Vẽ Menu Chính (Khi chưa chơi)
        elif not self.stats.game_active:
            if self.menu_state == 'main':
                self.btn_play.draw_button()
                self.btn_settings.draw_button()
            elif self.menu_state == 'settings':
                self.btn_easy.draw_button()
                self.btn_normal.draw_button()
                self.btn_hard.draw_button()
                self.btn_back.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()