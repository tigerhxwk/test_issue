from pygame.sprite import Sprite as Sprite
from pygame import Surface as Surface
from pygame import key as key
from pygame import constants
from pygame import transform
from pygame import image
from entities.Entity import CmnEntity
from player.cast import Spell

BLACK = (0, 0, 0)

class PlayerHandler(Sprite, CmnEntity):
    def __init__(self, width, height, path_to_png):
        Sprite.__init__(self)
        self.img_normal = image.load(path_to_png + "/player.png").convert ()
        self.img_normal_left = image.load(path_to_png + "/player_left.png").convert ()
        self.img_damaged = image.load(path_to_png + "/player_damaged.png").convert ()
        self.img_damaged_left = image.load(path_to_png + "/player_left_damaged.png").convert ()
        self.img =self.img_normal
        self.img = transform.scale(self.img, (100, 80))
        self.image = self.img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.screenWidth = width
        self.screenHeight = height
        self.speedx = 0
        self.speedy = 0
        self.jumpCoolDown = 0
        self.redCoolDown = 0
        CmnEntity.__init__(self)
        self.setMaxHp (100)
        self.setCurrHp (100)
        self.direction = 1 #increasing coord, going right
        self.healsLeft = 4

    def update(self):
        self.speedx = 0
        keystate = key.get_pressed()
        if keystate[constants.K_LEFT] or keystate[constants.K_a]:
            self.speedx = -8
            self.direction = 0
        if keystate[constants.K_RIGHT] or keystate[constants.K_d]:
            self.speedx = 8
            self.direction = 1


        self.rect.x += self.speedx
        if self.rect.right > self.screenWidth:
            self.rect.right = self.screenWidth
        if self.rect.left < 0:
            self.rect.left = 0
        if self.jumpCoolDown == 10:
            self.jump(reset = True)

        if self.jumpCoolDown == 0:
            if keystate[constants.K_UP] or keystate[constants.K_w]:
                self.jump()
        else:
            self.jumpCoolDown -= 1

        if self.redCoolDown == 0:
            if self.direction == 1:
                self.img = self.img_normal
            else:
                self.img = self.img_normal_left

        else:
            self.redCoolDown -= 1

        self.image = self.img
        self.image.set_colorkey(BLACK)

    def jump(self, reset = False):
        if reset == True:
            self.speedy = 85
        else:
            self.speedy = -85
            self.jumpCoolDown = 20
        self.rect.y += self.speedy


    def turnRed (self):
        if self.direction == 1:
            self.img = self.img_damaged
        else:
            self.img = self.img_damaged_left

        self.img = transform.scale(self.img, (100, 80))
        self.redCoolDown = 10


    def castSpell (self, fb_path_dict : dict ()):
        spell = Spell (self.rect.centerx, self.rect.centery,
                       direction=self.direction, width=self.screenWidth,
                       path_to_img = fb_path_dict[self.direction])
        return spell

    def heal (self):
        if self.healsLeft != 0:
            self.healsLeft -= 1
            self.setCurrHp (int (self.getCurrHp () + self.getMaxHp ()*0.3))

