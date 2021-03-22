from box import Box
from constants import BLACK
from ball import Ball
import pygame
from pygame import display
from pygame import event

ball = Ball()
boxes = [
    Box(0, 500, 800,50)
]

def main():
    pygame.init()
    screen = display.set_mode((800, 600))

    init(screen)

    running = True

    while running:
        screen.fill(BLACK)
        update(screen)
        display.update()
        event.pump()


def init(screen):
    ball.init(screen)


def update(screen):
    ball.update(screen, boxes)

    for b in boxes:
        b.update(screen)

if __name__ == '__main__':
    main()
