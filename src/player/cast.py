from pygame.sprite import Sprite as Sprite
from pygame import transform
from pygame import image

BLACK = (0, 0, 0)
class Spell(Sprite):
    def __init__(self, x, y, direction, width, path_to_img):
        Sprite.__init__(self)
        self.img = image.load(path_to_img).convert()
        self.img = transform.scale(self.img, (50, 50))
        self.image = self.img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.width = width
        print (f"bottom {y}, center {x}")
        if direction == 1:
            self.speedx= 10
        else:
            self.speedx= -10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0 or self.rect.right > self.width:
            self.kill()
