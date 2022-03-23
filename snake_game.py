
# Snake for the micro:bit

# GLOBAL CONFIG
FPS = 2
# COLORS are numbers 0-9
HEAD_COLOR = 6
SEGMENT_COLORS = [4,3,5]
APPLE_COLOR = 9
BACKGROUND_COLOR = 0

import random
from microbit import *

DIRECTIONS = [
    [1,0],
    [0,-1],
    [-1,0],
    [0,1]
]

class Snake:
    def __init__(self):
        self.blocks = [[0,0]]
        self.direction = 0
        display.set_pixel(0,0,HEAD_COLOR)
    def collides(self,position):
        for block in self.blocks:
            if block[0] == position[0] and block[1] == position[1]: return True
        else: return False
    def step(self):
        global game
        if button_a.was_pressed(): self.direction += 1
        if button_b.was_pressed(): self.direction -= 1
        self.direction %= 4
        new_block = [a+b for a,b in zip(self.blocks[0],DIRECTIONS[self.direction])]
        for position in new_block:
            if position < 0 or position >= 5:
                game.game_over(new_block); return
        if self.collides(new_block):
            game.game_over(new_block); return
        self.blocks.insert(0,new_block)
        if new_block[0] == game.apple[0] and new_block[1] == game.apple[1]:
            if len(self.blocks) == 25: game.game_over(); return
            else: game.spawn_apple()
        else:
            display.set_pixel(self.blocks[-1][0],self.blocks[-1][1],BACKGROUND_COLOR)
            self.blocks = self.blocks[:-1]
        display.set_pixel(new_block[0],new_block[1],HEAD_COLOR)
        for i, block in enumerate(self.blocks[1:]):
            display.set_pixel(block[0],block[1],SEGMENT_COLORS[i%3])

class Game:
    def __init__(self):
        self.apple = None
        self.snake = Snake()
        self.spawn_apple()
        self.running = True
    def score(self): return len(self.snake.blocks) - 1
    def step(self): self.snake.step()
    def game_over(self, position):
        self.running = False
        self.death_position = position
    def spawn_apple(self):
        if self.apple:
            display.set_pixel(self.apple[0],self.apple[1],BACKGROUND_COLOR)
        new_apple = [random.randint(0,4),random.randint(0,4)]
        while self.snake.collides(new_apple):
            new_apple = [random.randint(0,4),random.randint(0,4)]
        self.apple = new_apple
        display.set_pixel(self.apple[0],self.apple[1],APPLE_COLOR)

game = Game()

while game.running:
    sleep(1000/FPS)
    game.step()
    
score = game.score()

# move memory to save space
# (required)

death_position = game.death_position
snake_blocks = game.snake.blocks
apple = game.apple

del game
del Game
del DIRECTIONS
del Snake

for explosion in range((score//5)+1):
    for radius in range(10):
        darken = 9-radius
        explosion_brightness = max(0,9-radius)
        display.set_pixel(apple[0],apple[1],int(APPLE_COLOR/(2-radius/9)))
        display.set_pixel(snake_blocks[0][0],snake_blocks[0][1],int(HEAD_COLOR//(2-radius/9)))
        for i, block in enumerate(snake_blocks):
            display.set_pixel(block[0],block[1],int(SEGMENT_COLORS[i%3]//(2-radius/9)))
        for y in range(5):
            for x in range(5):
                if abs(x-death_position[0]) + abs(y-death_position[1]) == radius:
                    display.set_pixel(x,y,explosion_brightness)
        sleep(100)
        for y in range(5):
            for x in range(5):
                if abs(x-death_position[0]) + abs(y-death_position[1]) == radius:
                    display.set_pixel(x,y,BACKGROUND_COLOR)

if score < 10:
    display.show(str(score),loop=True)
else:
    display.scroll(str(score),loop=True,monospace=True)
