import pygame
import sys
import random

from Rocket import Rocket
from School import School
from Explosion import Explosion


class Game:
    def __init__(self):
        pygame.init()

        info = pygame.display.Info()

        self.WIDTH = info.current_w
        self.HEIGHT = info.current_h

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT), pygame.FULLSCREEN
        )

        pygame.display.set_caption("Defend the School")

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

        self.school = School(self.WIDTH, self.HEIGHT)

        self.rockets: list[Rocket] = []

        self.rocket_timer = pygame.time.get_ticks()

        self.explosions = pygame.sprite.Group()

        pygame.mixer.init()

        self.school_explosion_sound = pygame.mixer.Sound(
            "./assets/sounds/school_explosion.mp3"
        )
        self.explosion_sound = pygame.mixer.Sound("./assets/sounds/explosion.mp3")
        self.danger_siren = pygame.mixer.Sound("./assets/sounds/Danger_Siren.mp3")

        self.school_explosion_sound.set_volume(3)
        self.explosion_sound.set_volume(1.5)
        self.danger_siren.set_volume(0.4)

        self.danger_siren.play(loops=-1)

        self.first_rocket = True
        self.score = 0
        self.win = False

    def draw_overlay(self, title, subtitle):
        font = pygame.font.SysFont("Arial", 26, bold=True)
        large_font = pygame.font.SysFont("Arial", 54, bold=True)

        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))

        self.screen.blit(overlay, (0, 0))

        title_surface = large_font.render(title, True, (245, 245, 245))

        subtitle_surface = font.render(subtitle, True, (255, 220, 70))

        self.screen.blit(
            title_surface,
            title_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 35)),
        )

        self.screen.blit(
            subtitle_surface,
            subtitle_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 35)),
        )

    def create_explosion(self, position, type):
        self.explosions.add(Explosion(position, type))

        if type == "school":
            self.school_explosion_sound.play()
        elif type == "rocket":
            self.explosion_sound.play()

    def kill_rocket(self, rocket):
        self.rockets.remove(rocket)
        self.score += 1

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if (self.game_over or self.win) and event.key == pygame.K_r:
                    self.running = True
                    self.game_over = False
                    self.first_rocket = True
                    self.win = False
                    self.score = 0
                    self.danger_siren.play()
                    self.school = School(self.WIDTH, self.HEIGHT)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for rocket in self.rockets:
                        rocket_mask = pygame.mask.from_surface(rocket.image)

                        offset = (
                            event.pos[0] - rocket.rect.left,
                            event.pos[1] - rocket.rect.top,
                        )

                        if (
                            0 <= offset[0] < rocket.rect.width
                            and 0 <= offset[1] < rocket.rect.height
                        ):
                            if rocket_mask.get_at(offset):
                                self.create_explosion(event.pos, "rocket")
                                self.kill_rocket(rocket)
                                break

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.score >= 30:
            self.win = True
            
        if self.first_rocket:
            if current_time - self.rocket_timer >= 10000:
                self.rockets.append(Rocket(self.school))
                self.rocket_timer = current_time
                self.first_rocket = False
        else:
            # Spawn a rocket every 1 second
            self.rocket_spawn_interval = random.choice([2000, 3000, 5000])
            if (
                current_time - self.rocket_timer >= self.rocket_spawn_interval
                and not self.game_over
            ):
                self.rockets.append(Rocket(self.school))
                self.rocket_timer = current_time

        # Update rockets
        for rocket in self.rockets[:]:
            rocket.update()

            # # Create masks
            rocket_mask = pygame.mask.from_surface(rocket.image)

            # # Calculate offset
            offset = (
                self.school.mask_rect.x - rocket.rect.x,
                self.school.mask_rect.y - rocket.rect.y,
            )

            # Remove rockets outside screen
            if colision_point := rocket_mask.overlap(self.school.mask, offset):
                # Convert rocket-local coordinates to screen coordinates
                colision_point = (
                    rocket.rect.left + colision_point[0],
                    rocket.rect.top + colision_point[1],
                )

                self.create_explosion(colision_point, "school")
                self.kill_rocket(rocket)
                self.school.damage(self.WIDTH, self.HEIGHT)
                break

        if self.school.health <= 0:
            self.game_over = True
            self.draw_overlay("شما باختید.", "فرشتگان میناب پر کشیدند.")

        # Update
        self.explosions.update()

    def draw(self):
        self.WIDTH, self.HEIGHT = self.screen.get_size()
        self.background_image = pygame.image.load("./assets/images/bg.png").convert()

        self.background_image = pygame.transform.scale(
            self.background_image, (self.WIDTH, self.HEIGHT)
        )

        self.screen.blit(self.background_image, (0, 0))

        self.school.draw(self.screen)

        for rocket in self.rockets:
            rocket.draw(self.screen)

        self.explosions.draw(self.screen)

        if self.game_over:
            self.rockets = []
            self.draw_overlay("GAME OVER", "Press ESC to exit AND R to Restart")
            self.danger_siren.stop()

        if self.win:
            self.rockets = []
            self.draw_overlay("YOU WIN", "Press ESC to exit AND R to Restart")
            self.danger_siren.stop()

        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
