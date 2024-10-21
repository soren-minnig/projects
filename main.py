# For my CodeJam project, I decided to make a simple game using pygame.
# Even though I wanted to add projectiles and have the enemies follow the
# player, I'm temporarily shying away from it (the math library scares me...)
# Maybe I'll try to make a better game in the future when I learn more.

import pygame
import pytmx
import sys
from sprites import *
from config import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible
        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        pygame.display.set_caption('Game')
        
        self.running = True

    def new(self):
        # new game
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 1, 2)
        
        self.enemy1 = Enemy(self, 6, 11)
        self.enemy2 = Enemy(self, 11, 4)

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    elif self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
                    elif self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    elif self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)

    def update(self):
        # game loop updates
        self.all_sprites.update()

    def draw(self):
        # game loop draw
        map = pytmx.load_pygame('tilemap.tmx')
        for layer in map.visible_layers:
            for x, y, gid, in layer:
                tile = map.get_tile_image_by_gid(gid)
                self.screen.blit(tile, (x * 32,
                                        y * 32))
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)

        # creating a boundary from the window
        barrier = pygame.Rect(32, 64, 640-64, 480-96)
        self.player.rect.clamp_ip(barrier)
        self.player_x, self.player_y = (0, 0)
        self.enemy1.rect.clamp_ip(barrier)
        self.enemy1_x, self.enemy_y = (0, 0)
        self.enemy2.rect.clamp_ip(barrier)
        self.enemy2_x, self.enemy_y = (0, 0)

        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass
        
    def intro_screen(self):
        pass


# game begins
game = Game()
game.intro_screen()
game.new()
while game.running:
    game.main()
    game.game_over()

pygame.quit()
sys.exit()