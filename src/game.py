import pygame
import random
from collections import deque
from pipe import Pipe
from bird import Bird

pygame.init()

# const
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 512
FPS = 15

# assets
BASE = pygame.image.load("./assets/base.png")
BASE_HEIGHT = BASE.get_height()
BASE = pygame.transform.scale(BASE, (SCREEN_WIDTH, BASE_HEIGHT))
BASE_WIDTH = BASE.get_width()

PIPE_UP = pygame.image.load("./assets/pipe-green.png")
PIPE_DOWN = pygame.transform.flip(PIPE_UP, False, True)
PIPE_WIDTH = PIPE_UP.get_width()

BACKGROUND = pygame.transform.scale(pygame.image.load("./assets/background-day.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# TODO:
# fix pipe generation
# add score to UI
# add bird physics

class Game:

    def __init__(self):
        
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

        self.pipes = deque(maxlen=3)
        self.bird = Bird(self.height)
        self.scroll_speed = 5

        self.reset()

    def reset(self):

        self.base_x1 = 0
        self.base_x2 = BASE_WIDTH
        
        for x_offset in (200, 375, 550):
            self.pipes.append(self.generate_pipe(x_offset))

        self.bird.down()

        self.score = 0

    def generate_pipe(self, x_offset=0):

        new_x = self.width + PIPE_WIDTH + x_offset
        new_y_up = random.randint(self.height-350, self.height-150)
        new_y_down = new_y_up-100-320

        return (Pipe(PIPE_UP, new_x, new_y_up, self.scroll_speed), Pipe(PIPE_DOWN, new_x, new_y_down, self.scroll_speed))
    
    def update_pipes(self):

        if self.pipes[0][0].x < -(PIPE_WIDTH):
            self.pipes.append(self.generate_pipe(125-PIPE_WIDTH*2))
        
    def update_ui(self):

        self.screen.blit(BACKGROUND, (0,0))
        
        for pipe_up, pipe_down in self.pipes:
            pipe_up.draw(self.screen)
            pipe_down.draw(self.screen)
        
        self.bird.draw(self.screen)

        self.screen.blit(BASE, (self.base_x1, 425))
        self.screen.blit(BASE, (self.base_x2, 425))

        pygame.display.flip()

    def check_collision(self):

        for pipe_up, pipe_down in self.pipes:
            offset_x = pipe_up.x - self.bird.x
            offset_y_up = pipe_up.y - self.bird.y
            offset_y_down =  pipe_down.y - self.bird.y

            if self.bird.mask.overlap(pipe_up.mask, (offset_x, offset_y_up)) \
                or self.bird.mask.overlap(pipe_down.mask, (offset_x, offset_y_down)):
                return True
        
        if self.bird.y >= 400:
            return True
        
        return False
    
    def scroll(self):

        self.base_x1 -= self.scroll_speed
        if self.base_x1 <= -BASE_WIDTH:
            self.base_x1 = 0

        self.base_x2 = self.base_x1 + BASE_WIDTH

        for pipe_up, pipe_down in self.pipes:
            pipe_up.move()
            pipe_down.move()

        self.bird.move()
        self.bird.down()

    def handle_user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.bird.up()

    def play_step(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.handle_user_input()
        
        self.update_pipes()
        self.scroll()
        self.update_ui()

        if self.check_collision():
            return True, self.score
        
        self.clock.tick(FPS)

        return False, self.score

if __name__ == '__main__':
    game = Game()

    keys = pygame.key.get_pressed()

    while True:
        game_over, record = game.play_step()

        if game_over:
            break
    
        


        

        
    
