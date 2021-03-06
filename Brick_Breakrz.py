#!/usr/bin/env python3

import sys
import pygame
from pygame.locals import *
from sys import exit
import random

ENDGAME = False
win = False

# hold ball until player is ready
hold_ball = True

score = 0
lives = 3

num_blocks = 49

screen_width = 648
screen_height = 600


class Ball:

    def __init__(self):
        self.diameter = 7

        # ball speed
        self.xy_gain = 4

        # place ball at a random coordinate inside the empty area
        self.x = random.randint(100, screen_width - 100)
        self.y = random.randint(200, screen_height - 200)

        # set ball to go in random southern direction
        direction = random.randint(1, 2)
        if direction == 1:
            self.angle = 'SE'
        elif direction == 2:
            self.angle = 'SW'

    def move(self):
        '''moves ball in the appropriate direction'''
        if self.angle == 'NE':
            self.y -= self.xy_gain
            self.x += self.xy_gain
        elif self.angle == 'NW':
            self.y -= self.xy_gain
            self.x -= self.xy_gain
        elif self.angle == 'SE':
            self.y += self.xy_gain
            self.x += self.xy_gain
        elif self.angle == 'SW':
            self.y += self.xy_gain
            self.x -= self.xy_gain

    def update(self):
        '''redraws the ball'''
        screen.blit(ball_img, (self.x, self.y))

    def check_ball(self):
        '''resets ball, decrements lives, and returns true if
           ball flew off the bottom side of the screen'''
        global lives

        if self.y > screen_height + 20:
            lives -= 1

            # place ball at a random coordinate inside the empty area
            self.x = random.randint(100, screen_width - 100)
            self.y = random.randint(200, screen_height - 200)

            # set ball to go in random southern direction
            direction = random.randint(1, 2)
            if direction == 1:
                self.angle = 'SE'
            elif direction == 2:
                self.angle = 'SW'

            return True

    def hit_wall(self):
        '''changes direction of ball when it hits a block, wall,
           or paddle. Decreases lives if ball goes off the screen'''

        global lives

        # touching left side
        if self.x - self.diameter <= 40:
            if self.angle == 'NW':
                self.angle = 'NE'
            elif self.angle == 'SW':
                self.angle = 'SE'

        # touching top
        elif self.y - self.diameter <= 40:
            if self.angle == 'NE':
                self.angle = 'SE'
            elif self.angle == 'NW':
                self.angle = 'SW'

        # touching right side
        elif self.x + self.diameter >= screen_width - 40:
            if self.angle == 'SE':
                self.angle = 'SW'
            elif self.angle == 'NE':
                self.angle = 'NW'

        # touching paddle
        elif self.y >= paddle.y - self.diameter and self.y < paddle.y:
            if self.x >= paddle.x and self.x < paddle.x + paddle.width:
                self.y -= 1
                if self.angle == 'SE':
                    self.angle = 'NE'
                elif self.angle == 'SW':
                    self.angle = 'NW'

        # # taking place of paddle for debugging REMOVE FOR FINAL GAME
        # if self.y >= paddle.y:
        #     if self.angle == 'SE':
        #         self.angle = 'NE'
        #     elif self.angle == 'SW':
        #         self.angle = 'NW'




class Block:
    def __init__(self, x, y):
        self.width = 75
        self.height = 20
        self.x = x
        self.y = y

    def update(self):
        '''redraws block'''
        screen.blit(block_img, (self.x, self.y))

    def check_collision(self):
        '''changes direction of ball according to what side of block it touches'''
        if ball.x >= self.x and ball.x <= self.x + self.width:
            # touching bottom
            if ball.y <= self.y + self.height and ball.y <= self.y + self.height + 1:
                if ball.angle == 'NE':
                    ball.angle = 'SE'
                elif ball.angle == 'NW':
                    ball.angle = 'SW'
                return True

            # touching top
            elif ball.y >= self.y - ball.diameter and ball.y <= self.y:
                if ball.angle == 'SE':
                    ball.angle = 'NE'
                elif ball.angle == 'SW':
                    ball.angle = 'NW'
                return True

        elif ball.y >= self.y and ball.y <= self.y + self.height:
            # touching left side
            if ball.x >= self.x - ball.diameter and ball.x <= self.x + ball.diameter:
                if ball.angle == 'NE':
                    ball.angle = 'NW'
                elif ball.angle == 'SE':
                    ball.angle = 'SW'
                return True

            # touching right side
            elif ball.x >= self.x + self.width and ball.x <= self.x + self.width + ball.diameter:
                if ball.angle == 'NW':
                    ball.angle = 'NE'
                elif ball.angle == 'SW':
                    ball.angle = 'SE'
                return True

        return False


class Paddle:

    def __init__(self):
        self.x = screen_width / 2 # start paddle at middle of screen
        self.y = screen_height - 60 # position paddle some distance from bottom of screen

        # dimensions
        self.width = 80
        self.height = 10

    def update(self):
        '''redraws paddle wherever mouse is pointed'''
        self.x, ignore = pygame.mouse.get_pos()
        screen.blit(paddle_img, (self.x, self.y))


def display(message, coords=(8,8), font=40, color=(175, 4, 4)):
    '''displays score and lives'''
    font = pygame.font.Font(None, font)
    text = font.render(message, 1, color)
    screen.blit(text, coords)

def check_lives_and_score():
    '''checks if player has enough lives'''
    global ENDGAME, win

    if lives <= 0:
        ENDGAME = True

    if score >= num_blocks:
        win = True
        ENDGAME = True

#***** Setting up game ******
pygame.init()


#******* Setting up screen ******
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Brick Breakrz')


#**** Setting up images *****
# paddle
paddle_img = pygame.image.load('paddle.png').convert()

# blocks
block_img = pygame.image.load('brick.png').convert()

# ball
ball_img = pygame.image.load('ball.png').convert()

# background
background = pygame.image.load('background.png').convert()


#********* Setting up blocks ********
blocks = []

block_width_plus_padding = 76
block_height_plus_padding = 21
x_padding = 57
y_padding = 55

row = 0
column = 0
for _ in range(0, num_blocks):
    # keep blocks from going off the screen
    if (x_padding + column * block_width_plus_padding > \
            screen_width - block_width_plus_padding):
        row += 1
        column = 0

    # pass in coordinates and append block object to list
    blocks.append(Block((x_padding + column * block_width_plus_padding), \
                            (y_padding + row * block_height_plus_padding)))

    # move to next column
    column += 1


#***** Setting up paddle, ball, and clock ******
paddle = Paddle()

ball = Ball()

clock = pygame.time.Clock()


#********** Start game message *****
while True:
    # check if player closed game
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # fill screen with white then render background
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    # display instructions
    display('Instructions:', (50, 50), 36)
    display('Use the mouse to keep the ball', (50, 80), 36)
    display('on the screen using the paddle.', (50, 110), 36)
    display('(Click to play)', (40, screen_height - 32))

    # check for left click
    left_click, middle_click, right_click = pygame.mouse.get_pressed()
    if left_click == True:
        break

    pygame.display.update()


#********* Game Loop **********
while ENDGAME == False:
    # check if player closed game
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # fill screen with white then render
    # background image before other objects
    screen.fill((255, 255, 255))
    screen.blit(background, (0,0))

    left_click, middle_click, right_click = pygame.mouse.get_pressed()
    if left_click == True:
        hold_ball = False

    if hold_ball == False:
        ball.move()
    else:
        display('Click to release ball', (40, screen_height - 32))

    ball.update()

    ball.hit_wall()

    ball_off_screen = ball.check_ball()

    if ball_off_screen == True:
        hold_ball = True

    paddle.update()

    check_lives_and_score()

    for block in blocks:
        ball_hit_block = block.check_collision()

        if ball_hit_block == True:
            # throw block off the screen if hit
            block.x = -100
            block.y = 0

            score += 1

        # update block
        block.update()

    # display score and lives
    display('Score: ' + str(score) + '  Lives: ' + str(lives))

    pygame.display.update()

    # 60 frames per second
    clock.tick(60)


if win == True:
    message = 'You Win!!!'
else:
    message = 'You Lose.'


#***** End game message *****
while True:
    # check if player closed game
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # fill screen with white then render background
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    # display winning/losing message
    display(message)

    pygame.display.update()