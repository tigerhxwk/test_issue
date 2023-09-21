from pygame.sprite import Sprite as Sprite
from pygame import Surface as Surface
from entities.Entity import CmnEntity
import random
from pygame import image
from pygame import transform

BLACK = (0, 0, 0)

class MobHandler(Sprite, CmnEntity):
    def __init__(self, width, height, path_to_img):
        Sprite.__init__(self)
        self.img_normal = image.load(path_to_img + "/mob.png").convert ()
        self.img_normal = transform.scale(self.img_normal, (60, 80))
        self.img_damaged = image.load(path_to_img + "/mob_damaged.png").convert()
        self.img_damaged = transform.scale(self.img_damaged, (60, 80))
        self.img = self.img_normal
        self.image = self.img
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
        self.redCoolDown = 0

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
            self.speedx = random.randrange(1, 8)

        if self.redCoolDown == 0:
            self.img = self.img_normal
        else:
            self.redCoolDown -= 1

        self.image = self.img
        self.image.set_colorkey(BLACK)

    def isDisappeared (self):
        if self.isEntityDown() == True:
            return True
        return False


    def turnRed (self):
        self.img = self.img_damaged
        self.img = transform.scale(self.img, (60, 80))
        self.redCoolDown = 10

