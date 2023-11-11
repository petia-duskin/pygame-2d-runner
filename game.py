import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D runner")

clock = pygame.time.Clock()
score_font = pygame.font.Font("./font/Pixeltype.ttf", 100)

background_surface = pygame.image.load("./graphics/Sky.png").convert_alpha()
background_surface = pygame.transform.scale(background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

ground_surface = pygame.image.load("./graphics/ground.png").convert_alpha()
ground_surface = pygame.transform.scale(ground_surface, (SCREEN_WIDTH, ground_surface.get_height()))

player_surface = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(x=100,
                                      y=SCREEN_HEIGHT - ground_surface.get_height() - player_surface.get_height())

score_surface = score_font.render("Simple 2D Runner", False, (64, 64, 64))
score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, 50))

snail_surface = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(x=SCREEN_WIDTH - 200,
                                    y=SCREEN_HEIGHT - ground_surface.get_height() - snail_surface.get_height())

player_gravity = 0
game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos): player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.y > 350:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.x = SCREEN_WIDTH - 200

    if game_active:
        screen.blit(background_surface, (0, 0))
        screen.blit(ground_surface, (0, SCREEN_HEIGHT - ground_surface.get_height()))
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        # Create floor
        if player_rect.bottom > SCREEN_HEIGHT - ground_surface.get_height():
            player_rect.y = SCREEN_HEIGHT - ground_surface.get_height() - player_surface.get_height()
        screen.blit(player_surface, player_rect)

        snail_rect.x -= 5
        if snail_rect.x < 0:
            snail_rect.x = SCREEN_WIDTH
        screen.blit(snail_surface, snail_rect)

        pygame.draw.rect(screen, '#c0e8ec', score_rect, border_radius=5)
        screen.blit(score_surface, score_rect)

        # check collision between player and snail
        if snail_rect.colliderect(player_rect):
            game_active = False

    print(pygame.time.get_ticks())
    pygame.display.update()
    clock.tick(60)
