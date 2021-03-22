from pygame.rect import Rect
from constants import G, WHITE
from pygame import Vector2, draw

class Box():

    def __init__(self, x, y, w, h):
        self.pos = Vector2(x, y)
        self.size = Vector2(w, h)

    def update(self, screen):
        draw.rect(screen, WHITE, self.as_rect())


    def as_rect(self):
        return Rect(self.pos, self.size)
