import pygame, sys, random

# ================= INIT =================
pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()

# ================= CONSTANT =================
gravity = 0.25
PIPE_GAP = 750
PIPE_SPEED = 3

# ================= LOAD ASSETS =================
bg = pygame.transform.scale2x(
    pygame.image.load("assets/background-sunset.png").convert()
)

floor = pygame.transform.scale2x(
    pygame.image.load("assets/floor.png").convert()
)

pipe_surface = pygame.transform.scale2x(
    pygame.image.load("assets/pipe-green.png").convert()
)

# ====== BIRD FRAMES (THÊM) ======
bird_frames = [
    pygame.transform.scale2x(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()),
    pygame.transform.scale2x(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()),
    pygame.transform.scale2x(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha())
]

bird_index = 0
bird = bird_frames[bird_index]

# ================= BIRD =================
bird_rect = bird.get_rect(center=(100, 384))
bird_movement = 0

# ================= FLOOR =================
floor_x = 0

# ================= PIPE =================
pipe_list = []
pipe_height = [250, 300, 350, 400, 450]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1800)

# ====== BIRD FLAP EVENT (THÊM) ======
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# ================= GAME STATE =================
game_active = True

# ================= FUNCTIONS =================
def create_pipe():
    y = random.choice(pipe_height)
    bottom = pipe_surface.get_rect(midtop=(500, y))
    top = pipe_surface.get_rect(midtop=(500, y - PIPE_GAP))
    return bottom, top

def move_pipes(pipes):
    for p in pipes:
        p.centerx -= PIPE_SPEED
    return pipes

def draw_pipes(pipes):
    for p in pipes:
        if p.bottom >= 600:
            screen.blit(pipe_surface, p)
        else:
            screen.blit(
                pygame.transform.flip(pipe_surface, False, True),
                p
            )

def check_collision(pipes):
    for p in pipes:
        if bird_rect.colliderect(p):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

# ================= GAME LOOP =================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

        # ====== XỬ LÝ ĐẬP CÁNH (THÊM) ======
        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % 3
            bird = bird_frames[bird_index]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -8
            elif event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0

    # ================= UPDATE =================
    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement

        pipe_list = move_pipes(pipe_list)
        game_active = check_collision(pipe_list)

    # ================= DRAW =================
    screen.blit(bg, (0, 0))

    draw_pipes(pipe_list)
    screen.blit(bird, bird_rect)

    floor_x -= 1
    screen.blit(floor, (floor_x, 650))
    screen.blit(floor, (floor_x + 432, 650))
    if floor_x <= -432:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)
