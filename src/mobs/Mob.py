from pygame.sprite import Sprite as Sprite
from pygame import Surface as Surface
from entities.Entity import CmnEntity
import random
from pygame import image
from pygame import transform

WIDTH = 600
HEIGHT = 480
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class MobHandler(Sprite, CmnEntity):
    def __init__(self, width, height, path_to_img):
        Sprite.__init__(self)
        self.img = image.load(path_to_img).convert()
        self.image = transform.scale(self.img, (100, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        startpos = random.choice([-(width + 25), 25])
        self.rect.x = width + startpos
        if self.rect.x < 0:
            self.direction = 1
        else:
            self.direction = 0
        self.rect.bottom = height - 10
        self.speedx = random.randrange(-10, 10)
        self.screenWidth = width
        self.screenHeight = height
        CmnEntity.__init__(self)

    def update(self):
        if self.rect.left <= 0:
            self.direction = 1
        if self.rect.right >= self.screenWidth:
            self.direction = 0
        if self.direction == 1:
            self.rect.x += self.speedx
        else:
            self.rect.x -= self.speedx
        if self.rect.left <= 0 or self.rect.right > self.screenWidth + 20:
            #self.rect.x = random.randrange(self.screenWidth - self.rect.width)
  #          self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(1, 8)

    def isDisappeared (self):
        if self.isEntityDown() == True:
            return True
        return False

