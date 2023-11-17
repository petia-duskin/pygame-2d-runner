import pygame
from sys import exit
from random import randint

pygame.init()

# set window size
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_window_size()

pygame.display.set_caption("2D runner")
clock = pygame.time.Clock()

pixel_font = pygame.font.Font("./font/Pixeltype.ttf", 100)

images = {}

# images[file] = pygame.image.load(file).convert_alpha()


# surfaces
background_surface = pygame.image.load("./graphics/Sky.png").convert_alpha()
scaled_background_surface = pygame.transform.scale(background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground_surface = pygame.image.load("./graphics/ground.png").convert_alpha()
scaled_ground_surface = pygame.transform.scale(ground_surface,
                                               (SCREEN_WIDTH, ground_surface.get_height()))
player_surface = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
GROUND_TOP_Y = SCREEN_HEIGHT - ground_surface.get_height()
player_rect = player_surface.get_rect(x=100,
                                      y=GROUND_TOP_Y - player_surface.get_height())
# Intro screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand_rect = player_stand.get_rect(x=100,
                                          y=GROUND_TOP_Y - player_surface.get_height())

score_surface = pixel_font.render("Simple 2D Runner", False, (64, 64, 64))
score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, 50))

# Obstacles
snail_surface = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
fly_surface = pygame.image.load("./graphics/fly/Fly1.png").convert_alpha()
obstacle_rect_list = []

# Game Menu
game_name = pixel_font.render("Simple 2D Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(SCREEN_WIDTH / 2, 50))

game_message = pixel_font.render("Press SPACE to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(SCREEN_WIDTH / 2, 200))

start_time = 0
score = 0
mobs_speed = 6
player_gravity = 0
game_active = False


def display_score():
    current_time = pygame.time.get_ticks() // 1000 - start_time
    score_surf = pixel_font.render(f"score: {current_time}", False, (64, 64, 64))
    score_rec = score_surf.get_rect(center=(SCREEN_WIDTH / 2, 50))
    screen.blit(score_surf, score_rec)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for type, obstacle_rect in obstacle_list:
            obstacle_rect.x -= mobs_speed

            if obstacle_rect.colliderect(player_rect):
                global game_active, obstacle_rect_list
                game_active = False
                obstacle_rect_list.clear()
                return

            if type == "fly":
                screen.blit(fly_surface, obstacle_rect)
            else:
                screen.blit(snail_surface, obstacle_rect)

        # optimize
        obstacle_list = [(type, obstacle) for type, obstacle in obstacle_list if obstacle.x > 0]
        return obstacle_list
    else:
        return []


# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

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
                start_time = pygame.time.get_ticks() // 1000

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(
                    ("snail", snail_surface.get_rect(x=randint(SCREEN_WIDTH - 300, SCREEN_WIDTH - 50),
                                                     y=SCREEN_HEIGHT - ground_surface.get_height() - snail_surface.get_height())))
            else:
                obstacle_rect_list.append(
                    ("fly", fly_surface.get_rect(x=randint(SCREEN_WIDTH - 300, SCREEN_WIDTH - 50),
                                                 y=randint(
                                                     SCREEN_HEIGHT - ground_surface.get_height() - snail_surface.get_height() - 550,
                                                     SCREEN_HEIGHT - ground_surface.get_height() - snail_surface.get_height() - 100)
                                                 )
                     ))

                obstacle_rect_list.append(
                    ("fly", fly_surface.get_rect(x=randint(SCREEN_WIDTH - 300, SCREEN_WIDTH - 50),
                                                 y=randint(
                                                     SCREEN_HEIGHT - ground_surface.get_height() - snail_surface.get_height() - 700,
                                                     SCREEN_HEIGHT - ground_surface.get_height() - snail_surface.get_height() - 100)
                                                 )
                     ))

    if game_active:
        screen.blit(scaled_background_surface, (0, 0))
        screen.blit(scaled_ground_surface, (0, SCREEN_HEIGHT - ground_surface.get_height()))
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        # Create floor
        if player_rect.bottom > GROUND_TOP_Y:
            player_rect.y = GROUND_TOP_Y - player_surface.get_height()
        screen.blit(player_surface, player_rect)

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        mobs_speed = 0.5 * score + 6
        score = display_score()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = pixel_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(SCREEN_WIDTH / 2, 250))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
