import pygame

BIRD = pygame.image.load('./assets/yellowbird-downflap.png')

class Bird:

    def __init__(self, screen_height: int):
        
        self.x = 100
        self.y = screen_height//2

        self.acceleration = 0.1
        self.velocity = 0

        self.image = BIRD
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def mask(self):
        return self._mask
    
    @mask.setter
    def mask(self, new_mask):
        self._mask = new_mask
    
    def up(self):
        self.velocity = 2.5
        self.y -= 15
        self.y += self.velocity

    def down(self):
        self.velocity += self.velocity * self.acceleration

    def move(self):
        self.y += self.velocity

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
