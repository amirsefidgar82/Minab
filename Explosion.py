import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, type):
        super().__init__()

        self.explosion_type = type
        self.frames = []
        self.load_frames("./assets/images/explosion.png")

        self.current_frame = 0
        self.animation_speed = 20
        self.last_update = pygame.time.get_ticks()

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)
        
    def load_frames(self, path):
        sprite_sheet = pygame.image.load(path).convert_alpha()

        sheet_width, sheet_height = sprite_sheet.get_size()

        frame_width = sheet_width // 6
        frame_height = sheet_height // 6

        for i in range(34):
            row = i // 6
            col = i % 6

            frame = sprite_sheet.subsurface(
                (col * frame_width, row * frame_height, frame_width, frame_height)
            )

            if self.explosion_type == "school":
                frame = pygame.transform.scale(frame, (300, 300))
                self.animation_speed = 10
            else:
                frame = pygame.transform.scale(frame, (120, 120))
            self.frames.append(frame)

    def update(self):
        now = pygame.time.get_ticks()

        if now - self.last_update >= self.animation_speed:
            self.last_update = now
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                self.kill()
                return

            center = self.rect.center
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=center)
