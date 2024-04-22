import pygame

class Pipe:

    def __init__(self, image, x: int, y: int, velocity: int):
        
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

        self.velocity = velocity

    @property
    def mask(self):
        return self._mask
    
    @mask.setter
    def mask(self, new_mask):
        self._mask = new_mask
        
    def move(self):
        self.x -= self.velocity

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))