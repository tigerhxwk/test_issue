#!/usr/bin/python3

import pygame
from player.Player import PlayerHandler
from mobs.Mob import MobHandler
from os import path

img_dir = path.join(path.dirname(__file__), '../props')

WIDTH = 600
HEIGHT = 480
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# create window and env
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test game")
clock = pygame.time.Clock()

background = pygame.image.load(path.join(img_dir, 'background.png')).convert()
background_rect = background.get_rect()

fb_left = path.join(img_dir, "fireball_left.png")
fb_right = path.join(img_dir, "fireball_right.png")
fb_dict = dict ()
fb_dict[0] = fb_left
fb_dict[1] = fb_right
all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
spells_sprites = pygame.sprite.Group()
player = PlayerHandler (WIDTH, HEIGHT, img_dir)
#player_sprites.add(player)
all_sprites.add(player)
mob = MobHandler (WIDTH, HEIGHT, img_dir)
mob_sprites.add(mob)
all_sprites.add(mob)
dmgCoolDown = 0
mobSpawnCoolDown = 250

infoFont = pygame.font.Font('freesansbold.ttf', 14)
infoText = infoFont.render(f'Use WASD or arrows to move, space to cast spells, F to heal.', True, WHITE, BLACK)
infoTextRect = infoText.get_rect()
infoTextRect.center = (WIDTH // 2, 40)
#game cycle
wasted = False
isPlaying = True
score = 0
while isPlaying:
    playerText = infoFont.render(f'Heals left {player.healsLeft} | HP: {player.getCurrHp()} | Score : {score}', True, WHITE, BLACK)
    playerTextRect = playerText.get_rect()
    playerTextRect.center = (160, 60)
    # keep framerate
    clock.tick(FPS)
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isPlaying = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spell = player.castSpell (fb_dict)
                spells_sprites.add(spell)
                all_sprites.add(spell)
            if event.key == pygame.K_f:
                player.heal()

    if mobSpawnCoolDown == 0 and len(mob_sprites.sprites()) < 2:
        new_mob = MobHandler(WIDTH, HEIGHT, img_dir)
        all_sprites.add(new_mob)
        mob_sprites.add(new_mob)
        mobSpawnCoolDown = 500
    else:
        mobSpawnCoolDown -= 1

    hit_mobs = pygame.sprite.groupcollide(mob_sprites, spells_sprites, False, True)
    for mob in hit_mobs:
        mob.DamageAttempt(player)
        mob.turnRed ()

    all_sprites.update()
    # render
    if wasted != True:
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        screen.blit(infoText, infoTextRect)
        screen.blit(playerText, playerTextRect)
        pygame.display.flip()

        if dmgCoolDown == 0:
            if pygame.sprite.collide_rect(player, mob):
                result, damage = player.DamageAttempt(mob)
                if (result == True):
                    player.turnRed()
                    dmgCoolDown = 15
        else:
            dmgCoolDown -= 1

    if player.isEntityDown () == True:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('WASTED', True, RED, BLACK)
        textScore = font.render(f'SCORE:{score}', True, RED, BLACK)
        textRect = text.get_rect()
        textScoreRect = textScore.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        textScoreRect.center = (WIDTH // 2, HEIGHT // 2 + 40)
        mob_sprites.remove(mob)
        player_sprites.remove(player)
        screen.fill(BLACK)
        screen.blit(text, textRect)
        screen.blit(textScore, textScoreRect)
        pygame.display.flip()
        wasted = True


    if mob.isDisappeared() == True:
        score += 1
        all_sprites.remove(mob)
        mob_sprites.remove(mob)
        mob = MobHandler (WIDTH, HEIGHT, img_dir)
        all_sprites.add(mob)
        mob_sprites.add(mob)

pygame.quit()
