import pygame
import random
from collections import deque
from pipe import Pipe
from bird import Bird
import numpy as np

pygame.init()

# const
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 512
FPS = 240

# assets
BASE = pygame.image.load("./assets/base.png")
BASE_HEIGHT = BASE.get_height()
BASE = pygame.transform.scale(BASE, (SCREEN_WIDTH, BASE_HEIGHT))
BASE_WIDTH = BASE.get_width()

PIPE_UP = pygame.image.load("./assets/pipe-green.png")
PIPE_DOWN = pygame.transform.flip(PIPE_UP, False, True)
PIPE_WIDTH = PIPE_UP.get_width()
PIPE_HEIGHT = PIPE_UP.get_height()

BACKGROUND = pygame.transform.scale(pygame.image.load("./assets/background-day.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

SCORE_IMAGES = {i : pygame.image.load(f"./assets/{i}.png") for i in range(10)}

# TODO:
# fix pipe generation
# add score to UI
# add bird physics

class Game:

    def __init__(self):

        self.idle = True
        
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

        self.pipes = deque(maxlen=3)
        self.bird = Bird(self.height)
        self.scroll_speed = 5

        self.jump_timer = 0
        self.jump_delay = 125

        self.reset()

    def reset(self):

        self.bird = Bird(self.height)
        self.pipes.clear()
        
        for x_offset in (200, 375, 550):
            self.pipes.append(self.generate_pipe(x_offset))
        
        self.score = 0
        self.jump_timer = 0

        self.base_x1 = 0
        self.base_x2 = BASE_WIDTH

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

        self.base_x1 -= self.scroll_speed
        if self.base_x1 <= -BASE_WIDTH:
            self.base_x1 = 0

        self.base_x2 = self.base_x1 + BASE_WIDTH

        self.screen.blit(BASE, (self.base_x1, 425))
        self.screen.blit(BASE, (self.base_x2, 425))

        self.update_score_ui()

        pygame.display.flip()

    def update_score_ui(self):

        digits = [int(d) for d in str(self.score)]
        score_size = len(digits)

        score_x = (self.width - SCORE_IMAGES[digits[0]].get_width() * score_size) // 2
        score_y = 50

        for d in digits:
            self.screen.blit(SCORE_IMAGES[d], (score_x, score_y))
            score_x += SCORE_IMAGES[d].get_width()

    def check_collision(self):

        for pipe_up, pipe_down in self.pipes:
            offset_x = pipe_up.x - self.bird.x
            offset_y_up = pipe_up.y - self.bird.y
            offset_y_down =  pipe_down.y - self.bird.y

            if self.bird.mask.overlap(pipe_up.mask, (offset_x, offset_y_up)) \
                or self.bird.mask.overlap(pipe_down.mask, (offset_x, offset_y_down)):
                return True
        
        if self.bird.y >= 400 or self.bird.y < -50:
            return True
        
        return False
    
    def scroll(self):

        for pipe_up, pipe_down in self.pipes:
            pipe_up.move()
            pipe_down.move()

        self.bird.move()


    def play_step(self, move):

        reward = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if move and pygame.time.get_ticks() - self.jump_timer > self.jump_delay:
            self.bird.up()
        
        for pipe_up, _ in self.pipes:
            if self.bird.x > pipe_up.x and not pipe_up.scored:
                reward += 5
                self.score += 1
                pipe_up.scored = True

        self.update_pipes()
        self.scroll()
        self.update_ui()

        closest_pipes = [p for p in self.pipes if p[0].scored == False][0]
        if closest_pipes[0].y + PIPE_HEIGHT < self.bird.y < closest_pipes[1].y:
            reward += 25

        if self.check_collision():
            reward -= 50
            return True, self.score, reward
        
        self.clock.tick(FPS)

        return False, self.score, reward

    def get_state(self):
        closest_pipes = [p for p in self.pipes if p[0].scored == False][0]
        c_pipe_down, c_pipe_up = closest_pipes

        state = [
            self.bird.y < c_pipe_down.y,
            c_pipe_down.y < self.bird.y < c_pipe_up.y,
            self.bird.y > c_pipe_up.y,
            self.bird.velocity,
            self.bird.x - c_pipe_up.x
        ]

        return np.array(state, dtype=float).reshape(1,5)