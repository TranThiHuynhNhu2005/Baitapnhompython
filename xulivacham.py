import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()

# ================= BACKGROUND =================
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

# ================= CHIM =================
bird_down = pygame.transform.scale2x(
    pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(
    pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(
    pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())

bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

gravity = 0.25
bird_movement = 0

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)

birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

# ================= ỐNG =================
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

pipe_list = []
pipe_height = [250, 300, 350, 400, 450]

def create_pipe():
    pos = random.choice(pipe_height)
    bottom = pipe_surface.get_rect(midtop=(500, pos))
    top = pipe_surface.get_rect(midtop=(500, pos - 700))
    return bottom, top

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1800)

# ================= VA CHẠM =================
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

# ================= BIẾN GAME =================
game_active = True

# ================= GAME LOOP =================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -8

            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0

        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

        if event.type == birdflap and game_active:
            bird_index = (bird_index + 1) % 3
            bird = bird_list[bird_index]

    screen.blit(bg, (0, 0))

    if game_active:
        # ===== CHIM =====
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(rotate_bird(bird), bird_rect)

        # ===== VA CHẠM =====
        game_active = check_collision(pipe_list)

        # ===== ỐNG =====
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

    # ===== SÀN =====
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
