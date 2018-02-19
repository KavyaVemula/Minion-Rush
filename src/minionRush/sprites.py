'''
Created on 2-Nov-2017

@author: Kavya Reddy
@author: Priyanka Gadde
'''

import pygame
from minionRush.constants import *
from random import randrange, choice
vec = pygame.math.Vector2


class Spritesheet:
    # Class for loading Spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        return image


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.jumping = False
        self.image = pygame.image.load('minion_frontFacing.png')
        self.image = pygame.transform.scale(self.image, (60, 75))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.pos = vec(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        self.rect.x += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # Applies friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Wraps around the sides of screen
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH

        self.rect.midbottom = self.pos


class Banana(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("banana.png")
        self.rect = self.image.get_rect()


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((w, h))
        self.image.fill(LIGHTGREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)


class Pow(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.powerups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        self.image = pygame.image.load("banana.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(416, 1660, 150, 181)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(584, 0, 121, 201)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, SCREEN_WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > SCREEN_WIDTH:
            self.vx *= -1
        self.rect.y = randrange(SCREEN_HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > SCREEN_WIDTH + 100 or self.rect.right < -100:
            self.kill()
