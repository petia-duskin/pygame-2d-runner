import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D runner")

clock = pygame.time.Clock()
test_font = pygame.font.Font("./font/Pixeltype.ttf", 100)

background_surface = pygame.image.load("./graphics/Sky.png").convert_alpha()
background_surface = pygame.transform.scale(background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

ground_surface = pygame.image.load("./graphics/ground.png").convert_alpha()
ground_surface = pygame.transform.scale(ground_surface, (SCREEN_WIDTH, ground_surface.get_height()))

player_surface = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(x=100,
                                      y=SCREEN_HEIGHT - ground_surface.get_height() - player_surface.get_height())

text_surface = test_font.render("Simple 2D Runner", False, "black")

snail_surface = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(x=SCREEN_WIDTH - 200,
                                    y=SCREEN_HEIGHT - ground_surface.get_height() - snail_surface.get_height())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, (0, 0))
    screen.blit(ground_surface, (0, SCREEN_HEIGHT - ground_surface.get_height()))
    screen.blit(player_surface, player_rect)
    snail_rect.x -= 5
    if snail_rect.x < 0:
        snail_rect.x = SCREEN_WIDTH
    screen.blit(snail_surface, snail_rect)
    screen.blit(text_surface, (SCREEN_WIDTH / 2 - text_surface.get_width() / 2, 50))
    player_rect.x += 1
    pygame.display.update()
    clock.tick(60)
