import pygame
from config import *
import math
import random

pygame.font.init()
font = pygame.font.SysFont('Tahoma', 15)

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.character_spritesheet = Spritesheet('images/fuu.png')

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # movement
        self.x_change = 0
        self.y_change = 0

        # animation
        self.facing = 'down'
        self.animation_loop = 0

        # the default down image is the 12th sprite and each is 32*32
        self.image = self.character_spritesheet.get_sprite(32*12, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.pos = self.x, self.y

    def update(self):
        self.movement()
        self.animate()
        # self.approach_block()
        self.collide_enemy()
        
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def animate(self):
        left_animations = [
            self.character_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*2, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*3, 0, self.width, self.height)
            ]
        right_animations = [
            self.character_spritesheet.get_sprite(32*4, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*5, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*6, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*7, 0, self.width, self.height)
            ]
        up_animations = [
            self.character_spritesheet.get_sprite(32*8, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*9, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*10, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*11, 0, self.width, self.height)
            ]
        down_animations = [
            self.character_spritesheet.get_sprite(32*12, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*13, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*14, 0, self.width, self.height),
            self.character_spritesheet.get_sprite(32*15, 0, self.width, self.height)
            ]

        if self.facing == 'left':
            # we start with an if loop: if the player is only looking left
            # and not moving, we don't want to loop through the animation
            if self.x_change == 0:
                self.image = left_animations[0]
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 0
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = right_animations[0]
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 0
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = up_animations[0]
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 0
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = down_animations[0]
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 0
        
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.enemy_spritesheet = Spritesheet('images/evil_fuu.png')

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(TILESIZE, TILESIZE*2)

        self.image = self.enemy_spritesheet.get_sprite(32*12, 0, self.width, self.height)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        left_animations = [
            self.enemy_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.enemy_spritesheet.get_sprite(32, 0, self.width, self.height),
            self.enemy_spritesheet.get_sprite(32*2, 0, self.width, self.height),
            self.enemy_spritesheet.get_sprite(32*3, 0, self.width, self.height)
            ]
        right_animations = [
            self.enemy_spritesheet.get_sprite(32*4, 0, self.width, self.height),
            self.enemy_spritesheet.get_sprite(32*5, 0, self.width, self.height),
            self.enemy_spritesheet.get_sprite(32*6, 0, self.width, self.height),
            self.enemy_spritesheet.get_sprite(32*7, 0, self.width, self.height)
            ]

        if self.facing == 'left':
            # I had to add in set_colorkey each time for some reason...
            if self.x_change == 0:
                self.image = left_animations[0]
                self.image.set_colorkey(WHITE)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.image.set_colorkey(WHITE)
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 0
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = right_animations[0]
                self.image.set_colorkey(WHITE)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.image.set_colorkey(WHITE)
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 0


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ATTACK_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.attack_spritesheet = Spritesheet('images/attacks.png')

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.image = self.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        left_animations = [
            self.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*2, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*3, 0, self.width, self.height)
            ]
        right_animations = [
            self.attack_spritesheet.get_sprite(32*4, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*5, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*6, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*7, 0, self.width, self.height)
            ]
        up_animations = [
            self.attack_spritesheet.get_sprite(32*8, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*9, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*10, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*11, 0, self.width, self.height)
            ]
        down_animations = [
            self.attack_spritesheet.get_sprite(32*12, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*13, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*14, 0, self.width, self.height),
            self.attack_spritesheet.get_sprite(32*15, 0, self.width, self.height)
            ]
        
        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 4:
                self.kill()
        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 4:
                self.kill()
        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 4:
                self.kill()
        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 4:
                self.kill()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ATTACK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.x = x
        self.y = y

        self.image = pygame.image.load('images/normal_projectile.png')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.velocity = 5
        
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.x, my - self.y
        len = math.hypot(dx, dy)
        self.dx = dx / len
        self.dy = dy / len
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        self.move()
        self.collide()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def collide(self):
        pygame.sprite.spritecollide(self, self.game.enemies, True)

    def move(self):
        self.x_change = self.dx * self.velocity
        self.y_change = self.dy * self.velocity


class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        self.type = type
        self._layer = OBJECT_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.intobject_spritesheet = Spritesheet('images/sign.png')

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.intobject_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.change_image()
        # self.interact()

    def change_image(self):
        if self.type == 'sign':
            self.image = self.intobject_spritesheet.get_sprite(0, 0, self.width, self.height)
        
    # def interact(self):
    #     if self.rect.colliderect(self.game.player.rect):
    #         self.nearby = True
    #         self.act = False
    #         text = font.render('e to interact', False, (WHITE))
    #         self.game.screen.blit(text, (self.x - 25, self.y - 16))
    #         pygame.display.flip()