import pygame, sys, random

# ================= INIT =================
pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()

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

bird = pygame.transform.scale2x(
    pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
)

# ================= BIRD (KHÔNG CHUYỂN ĐỘNG) =================
bird_rect = bird.get_rect(center=(100, 384))

# ================= FLOOR =================
floor_x = 0

# ================= PIPE =================
pipe_list = []
PIPE_GAP = 750
PIPE_SPEED = 3
pipe_height = [250, 300, 350, 400, 450]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1800)

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

# ================= GAME LOOP =================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # ================= UPDATE =================
    pipe_list = move_pipes(pipe_list)

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
