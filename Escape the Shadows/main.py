import pygame
import config
from Sprites.Sprites import Player, Mob, HealthBar

pygame.init()
pygame.font.init()

font = pygame.font.Font(pygame.font.get_default_font(), 20)

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
clock = pygame.time.Clock()

player = pygame.sprite.Group()
mobs = pygame.sprite.Group()
additional = pygame.sprite.Group()

ticks_from_start = 0

n_mobs = 5
for i in range(n_mobs):
    mobs.add(Mob())

player_entity = Player()
player.add(player_entity)

healthbar = HealthBar(player_entity)
additional.add(healthbar)

running = True

while running:
    clock.tick(config.FRAMERATE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()

    for mob in mobs:
        mob.compute_move(player_entity)

    mobs.update()
    additional.update()

    if player_entity.health == 0:
        running = False

    if len(mobs) < n_mobs:
        mobs.add(Mob())

    # hits = pygame.sprite.spritecollide(player_entity, mobs, True)
    hits = pygame.sprite.groupcollide(player, mobs, False, True)
    if hits:
        player_entity.health -= 1
        healthbar.health -= 1
        # sX, sY = player_entity.speed
        # player_entity.speed = (sX - 5, sY - 5)

    ticks_from_start += 1
    screen.fill(config.BLACK)
    player.draw(screen)
    mobs.draw(screen)
    additional.draw(screen)

    if config.DEBUG:
        for mob in mobs:
            player_cords = player_entity.rect.center
            mob_cords = mob.rect.center
            pygame.draw.aaline(screen, (255, 0, 0), player_cords, mob_cords)

    # text = font.render(f"Hp: {player_entity.health}", 0, (255, 255, 255))
    # time = font.render(f"Seconds: {ticks_from_start // config.FRAMERATE}", 0, (255, 255, 255))
    #
    # screen.blit(text, (0, 0))
    # screen.blit(time, (0, 30))

    pygame.display.flip()

pygame.quit()
