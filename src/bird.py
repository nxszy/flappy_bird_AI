import pygame
import pygame.image

BIRD_DOWN = pygame.image.load('./assets/yellowbird-downflap.png')
BIRD_MID = pygame.image.load('./assets/yellowbird-midflap.png')
BIRD_UP = pygame.image.load('./assets/yellowbird-upflap.png')

class Bird:

    def __init__(self, screen_height: int):
        
        self.x = 150
        self.y = screen_height//2

        self.acceleration = 0.10
        self.velocity = 0

        self.images = [BIRD_DOWN, BIRD_MID, BIRD_UP]
        self.image_cycle = 0
        self.image_index = 0
        self.animation_delay = 5

        self.masks = [pygame.mask.from_surface(img) for img in self.images]


    @property
    def mask(self):
        return self.masks[self.image_index]
    
    @mask.setter
    def mask(self, new_mask):
        self._mask = new_mask
    
    def up(self):
        self.velocity = -8

    def move(self):
        self.y += self.velocity
        self.velocity += (1+self.acceleration)
            
    def draw(self, screen):

        self.image_cycle = (self.image_cycle + 1) % (len(self.images) * self.animation_delay)
        self.image_index = self.image_cycle // self.animation_delay
        self.image = self.images[self.image_index]

        angle = self.calculate_angle()

        rotated_image = pygame.transform.rotate(self.image, angle)

        rotated_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)

        screen.blit(rotated_image, rotated_rect.topleft)
    
    def calculate_angle(self):
        
        factor = self.velocity * 5

        if factor == 0:
            return 0
        elif factor < 10:
            return 20
        else:
            return max(-factor, -90)
        
