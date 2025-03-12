import pygame.key
from pygame.sprite import Sprite
from pygame import Surface
import config
import random
import utils


class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((50, 50))
        self.image.fill(config.COLORS[random.randint(0, 3)])
        self.rect = self.image.get_rect()
        # self.rect.center = (config.WIDTH / 2, config.HEIGHT / 2)
        self.rect.center = (
            random.randint(0, config.WIDTH - 50) // 2,
            config.HEIGHT - self.rect.height
        )
        self.speed_x = random.randint(5, 20)
        self.speed_y = random.randint(5, 20)
        self.health = 5

    # @property
    # def speed(self):
    #     return self.speed_x, self.speed_y
    #
    # @speed.setter
    # def speed(self, value):
    #     if len(value) != 2 or type(value) not in [list, tuple] or value[0] <= 0 or value[1] <= 0:
    #         return
    #     self.speed_x, self.speed_y = value

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.rect.y -= self.speed_y
        if key[pygame.K_s]:
            self.rect.y += self.speed_y
        if key[pygame.K_a]:
            self.rect.x -= self.speed_x
        if key[pygame.K_d]:
            self.rect.x += self.speed_x

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > config.WIDTH - self.rect.width:
            self.rect.x = config.WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > config.HEIGHT - self.rect.height:
            self.rect.y = config.HEIGHT - self.rect.height
        # self.rect.x += self.speed_x
        # if self.rect.x < 0 or self.rect.x > config.WIDTH - self.rect.width:
        #     self.speed_x = -self.speed_x
        #
        # self.rect.y += self.speed_y
        # if self.rect.y < 0 or self.rect.y > config.HEIGHT - self.rect.height:
        #     self.speed_y = -self.speed_y


class Mob(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((20, 20))
        self.image.fill(config.COLORS[0])
        self.rect = self.image.get_rect()
        # self.rect.center = (config.WIDTH / 2, config.HEIGHT / 2)
        self.rect.center = (
            random.randint(0, config.WIDTH - 50),
            random.randint(0, 10)
        )
        self.speed_y = random.randint(1, 3)
        self.speed_x = random.randint(1, 3)

    def update(self):
        if self.rect.y + self.rect.height < config.HEIGHT:
            self.rect.y += self.speed_y
        else:
            self.kill()

    def compute_move(self, player: Player):
        x_player, y_player = player.rect.center  # (10, 20)
        x_mob, y_mob = self.rect.center

        move_right = utils.lenght(x_player, y_player, x_mob + self.speed_x, y_mob)
        move_left = utils.lenght(x_player, y_player, x_mob - self.speed_x, y_mob)
        stay_here = utils.lenght(x_player, y_player, x_mob, y_mob)

        min_len = min(move_left, move_right, stay_here)
        if min_len == move_left:
            self.rect.x -= self.speed_x
        if min_len == move_right:
            self.rect.x += self.speed_x


class HealthBar(Sprite):
    def __init__(self, player: Player):
        Sprite.__init__(self)
        self.__health = player.health
        self.image = Surface((config.WIDTH, 10))
        self.step = config.WIDTH // self.__health
        self.image.fill(config.RED)
        self.rect = self.image.get_rect()

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, val):
        self.__health = val
        self.image = Surface((config.WIDTH - self.step * self.__health, 10))
        self.image.fill(config.RED)
        self.rect = self.image.get_rect()
