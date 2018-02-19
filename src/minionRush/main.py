'''
Created on 2-Nov-2017

@author: Kavya Reddy
'''

import pygame
import random
from minionRush.constants import *
from minionRush.sprites import *
from os import path


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((480, 600))
        pygame.display.set_caption('Unicorn Island')
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.background = pygame.image.load("pinkbg.png")
        self.load_data()

    def load_data(self):
        # Loads the high score
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # Loads the sprite sheet image
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.splash_image = pygame.image.load("splash.png")
        # Loads the sounds
        self.snd_dir = path.join(self.dir, 'sounds')
        self.jump_sound = pygame.mixer.Sound(path.join(
                          self.snd_dir, "jumping.wav"))
        self.splash_sound = pygame.mixer.Sound(path.join(
                            self.snd_dir, 'minionsplash.wav'))
        self.gameover_sound = pygame.mixer.Sound(path.join(
                              self.snd_dir, 'gameover.wav'))

    def new(self):
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player, _layer=PLAYER_LAYER)
        for platform in PLATFORM_LIST:
            p = Platform(self, *platform)
            self.all_sprites.add(p, _layer=PLATFORM_LAYER)
            self.platforms.add(p)
        self.mob_timer = 0
        pygame.mixer.music.load(path.join(self.snd_dir, 'des.wav'))
        self.run()

    def run(self):
        pygame.mixer.music.play()
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.stop()

    def update(self):
        self.all_sprites.update()

        # Spawns the enemies
        now = pygame.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice(
           [-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.playing = False

        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(
                   self.player, self.platforms, False)

            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                   self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # If player reaches the top 1/4th of screen
        if self.player.rect.top <= SCREEN_HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for platform in self.platforms:
                platform.rect.y += max(abs(self.player.vel.y), 2)
                if platform.rect.top >= SCREEN_HEIGHT:
                    platform.kill()
                    self.score += 5

        # Hits Banana
        pow_hits = pygame.sprite.spritecollide(
                   self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.player.vel.y = -BOOST_POWER
                self.score += 10
                self.player.jumping = False

        # If the Player dies
        if self.player.rect.bottom > SCREEN_HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # Spawn new platforms to keep same average number
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(self, random.randrange(0, SCREEN_WIDTH - width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.jump()

    def draw(self):
        self.screen.fill(BGCOLOR)
#         self.screen.blit(self.background, [0, 0])
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, SCREEN_WIDTH / 2, 15)
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.blit(self.splash_image, [0, 0])
        self.splash_sound.play(loops=-1)
        self.draw_text("Minion Rush", 48, BLACK,
                       SCREEN_WIDTH / 2, SCREEN_HEIGHT / 7)
        self.draw_text("Kavya Reddy Vemula / Priyanka Gadde ", 22, BLACK,
                       SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1 / 4)
        self.draw_text("Use the arrow keys to move the player", 22, BLACK,
                       SCREEN_WIDTH / 2, SCREEN_HEIGHT - 70)
        self.draw_text("Press a key to play", 22, BLACK, SCREEN_WIDTH / 2,
                       SCREEN_HEIGHT - 40)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE,
                       SCREEN_WIDTH / 2, 15)
        pygame.display.flip()
        self.wait_for_key()
        self.splash_sound.fadeout(500)

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.gameover_sound.play()
        self.draw_text("Game Over!!", 58, WHITE, SCREEN_WIDTH / 2,
                       SCREEN_HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 32, WHITE,
                       SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text("Press a key to play again", 32, WHITE,
                       SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, SCREEN_WIDTH / 2,
                           SCREEN_HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE,
                           SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40)

        pygame.display.flip()
        self.wait_for_key()
        self.gameover_sound.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
