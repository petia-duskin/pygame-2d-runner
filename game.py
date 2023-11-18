import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_window_size()
ground_surface = pygame.image.load("./graphics/ground.png").convert_alpha()
GROUND_TOP_Y = SCREEN_HEIGHT - ground_surface.get_height()


class Player(pygame.sprite.Sprite):
    def __int__(self):
        super().__init__()
        self.image = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
        self.rect = self.image.get_rect(x=100,
                                        y=GROUND_TOP_Y - self.image.get_height())


pygame.display.set_caption("2D runner")
clock = pygame.time.Clock()

pixel_font = pygame.font.Font("./font/Pixeltype.ttf", 50)

# surfaces
background_surface = pygame.image.load("./graphics/Sky.png").convert_alpha()
scaled_background_surface = pygame.transform.scale(background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
scaled_ground_surface = pygame.transform.scale(ground_surface,
                                               (SCREEN_WIDTH, ground_surface.get_height()))

player_walk_1 = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("./graphics/Player/player_walk_2.png").convert_alpha()
player_jump = pygame.image.load("./graphics/Player/jump.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(x=100,
                                      y=GROUND_TOP_Y - player_surface.get_height())
# Intro screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand_rect = player_stand.get_rect(x=100,
                                          y=GROUND_TOP_Y - player_surface.get_height())

score_surface = pixel_font.render("Simple 2D Runner", False, (64, 64, 64))
score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, 50))

# Obstacles

# Snails
snail_frame_1 = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("./graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# Flies
fly_frame_1 = pygame.image.load("./graphics/fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("./graphics/fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

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


def player_animation():
    global player_surface, player_index
    if player_rect.y < GROUND_TOP_Y - player_surface.get_height():
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


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

            if type == "fly":
                screen.blit(fly_surface, obstacle_rect)
            else:
                screen.blit(snail_surface, obstacle_rect)

        # optimize
        obstacle_list = [(type, obstacle) for type, obstacle in obstacle_list if obstacle.x > 0]
        return obstacle_list
    else:
        return []


def check_collisions(player, obstacles):
    if obstacles:
        for type, obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False

    return True


def get_percent(number, percent):
    return number / 100 * percent


# fix code duplication
def generate_flies(obstacles):
    start_y = SCREEN_HEIGHT - ground_surface.get_height() - snail_surface.get_height() - get_percent(
        SCREEN_HEIGHT, 50)
    end_y = SCREEN_HEIGHT - ground_surface.get_height() - snail_surface.get_height() - get_percent(
        SCREEN_HEIGHT, 10)

    first = randint(start_y, end_y)
    second = randint(start_y, end_y)

    is_flies_ranged_enough = abs(first - second) > fly_surface.get_height() + player_surface.get_height()

    if is_flies_ranged_enough:
        obstacles.append(
            ("fly", fly_surface.get_rect(x=randint(SCREEN_WIDTH - 300, SCREEN_WIDTH - 50),
                                         y=first)))

        obstacles.append(
            ("fly", fly_surface.get_rect(x=randint(SCREEN_WIDTH - 300, SCREEN_WIDTH - 50),
                                         y=second)))
    else:
        while True:
            first = randint(start_y, end_y)
            second = randint(start_y, end_y)
            is_flies_ranged_enough = abs(first - second) > fly_surface.get_height() + player_surface.get_height()
            if is_flies_ranged_enough:
                obstacles.append(
                    ("fly", fly_surface.get_rect(x=randint(SCREEN_WIDTH - 300, SCREEN_WIDTH - 50),
                                                 y=first)))

                obstacles.append(
                    ("fly", fly_surface.get_rect(x=randint(SCREEN_WIDTH - 300, SCREEN_WIDTH - 50),
                                                 y=second)))
                break


# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 200)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos): player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.y > get_percent(SCREEN_HEIGHT, 50):
                    player_gravity = -20

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]
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
                generate_flies(obstacle_rect_list)

    if game_active:
        screen.blit(scaled_background_surface, (0, 0))
        screen.blit(scaled_ground_surface, (0, SCREEN_HEIGHT - ground_surface.get_height()))
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        # Create floor
        if player_rect.bottom > GROUND_TOP_Y:
            player_rect.y = GROUND_TOP_Y - player_surface.get_height()

        player_animation()
        screen.blit(player_surface, player_rect)

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collisions
        game_active = check_collisions(player_rect, obstacle_rect_list)

        mobs_speed = 0.5 * score + 6
        score = display_score()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_gravity = 0

        score_message = pixel_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(SCREEN_WIDTH / 2, 250))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
