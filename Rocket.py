import pygame
import random
import math

from School import School


class Rocket:
    def __init__(self, target: School):
        self.sprite_sheet = pygame.image.load(
            "./assets/images/rocket.png"
        ).convert_alpha()

        self.frames = []

        frame_width = self.sprite_sheet.get_width() // 5
        frame_height = self.sprite_sheet.get_height()

        for i in range(5):
            frame = self.sprite_sheet.subsurface(
                (i * frame_width, 0, frame_width, frame_height)
            ).copy()

            self.width = frame.get_width()
            self.height = frame.get_height()
            frame = pygame.transform.scale(frame, (self.width * 0.25, self.height * 0.25))

            self.frames.append(frame)

        self.animation_index = 0
        self.animation_speed = 80
        self.last_update = pygame.time.get_ticks()

        # Position
        self.x = random.randint(50, 1150)
        self.y = -100

        self.speed = random.randint(2, 10)
        self.target = target

        # Calculate random target position
        target_rect = target.mask.get_bounding_rects()[0]

        target_x = random.randint(
            target.rect.left + target_rect.left,
            target.rect.left + target_rect.right - 1
        )

        target_y = random.randint(
            target.rect.top + target_rect.top,
            target.rect.top + target_rect.bottom - 1
        )
        # # Calculate direction
        # dx = target_x - self.x
        # dy = target_y - self.y

        # angle = math.atan2(dy, dx)

        # self.velocity_x = math.cos(angle) * self.speed
        # self.velocity_y = math.sin(angle) * self.speed

        # # Rotate all frames toward target
        # self.angle = -math.degrees(angle) - 90

        # self.frames = [
        #     pygame.transform.rotate(frame, self.angle) for frame in self.frames
        # ]
        
        
        self.position = pygame.Vector2(self.x, self.y)
        self.target_pos = pygame.Vector2(target_x, target_y)

        direction = self.target_pos - self.position

        if direction.length_squared() > 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.Vector2(0, 0)

        self.velocity = self.direction * self.speed

        self.angle = -math.degrees(
            math.atan2(self.direction.y, self.direction.x)
        ) - 90

        self.frames = [
            pygame.transform.rotate(frame, self.angle)
            for frame in self.frames
        ]
        

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def update(self):
        self.position += self.velocity

        self.rect.center = (
            round(self.position.x),
            round(self.position.y)
        )
        # self.x += self.velocity_x
        # self.y += self.velocity_y

        # self.rect.center = (int(self.x), int(self.y))

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update >= self.animation_speed:
            self.animation_index = (self.animation_index + 1) % len(self.frames)
            self.last_update = now

            
            center = self.rect.center
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center=center)

    def draw(self, screen):
        self.animate()

        screen.blit(self.frames[self.animation_index], self.rect)