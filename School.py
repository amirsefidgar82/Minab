import pygame


class School:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("./assets/images/school_0.png").convert_alpha()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Resize image if needed
        self.image = pygame.transform.scale(
            self.image, (self.width * 1.2, self.height * 1.2)
        )

        self.health = 60
        self.damage_level = 0
        
        # get the rect instance
        self.rect = self.image.get_rect()

        # Create collision mask
        self.mask = pygame.mask.from_surface(self.image)

        # Get actual visible boundaries
        self.mask_rect = self.mask.get_bounding_rects()[0]

        self.rect.midbottom = (screen_width // 2, screen_height + 25)
        self.mask_rect.x = self.rect.x
        self.mask_rect.y = self.rect.y

        # self.rect.centerx -= self.mask_rect.centerx - self.rect.width // 2
        # self.rect.bottom += self.rect.height - self.mask_rect.bottom

    def damage(self, screen_width, screen_height):
        self.health -= 10
        self.damage_level = min(self.damage_level + 1, 5)
        
        self.image = pygame.image.load(
            f"./assets/images/school_{self.damage_level}.png"
        ).convert_alpha()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Resize image if needed
        self.image = pygame.transform.scale(
            self.image, (self.width * 1.2, self.height * 1.2)
        )

        self.rect = self.image.get_rect()

        # Create collision mask
        self.mask = pygame.mask.from_surface(self.image)

        # Get actual visible boundaries
        self.mask_rect = self.mask.get_bounding_rects()[0]

        self.rect.midbottom = (screen_width // 2, screen_height + 25)

        self.mask_rect.x = self.rect.x
        self.mask_rect.y = self.rect.y

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
