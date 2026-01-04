import pygame, sys, random, os

# ================== INIT ==================
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()

# ================== STATE ==================
MENU = "menu"
PLAYING = "playing"
INSTRUCTIONS = "instructions"
HIGHSCORE = "highscore"
GAMEOVER = "gameover"
game_state = MENU

# ================== CONSTANT ==================
gravity = 0.25
PIPE_GAP = 750
HIGHSCORE_FILE = "highscore.txt"

# ================== HIGH SCORE ==================
def load_high_score():
    with open(HIGHSCORE_FILE, "w") as f:
        f.write("0")
    return 0

def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

high_score = load_high_score()

# ================== LOAD ASSETS ==================
bg_day = pygame.transform.scale2x(
    pygame.image.load("assets/background-sunset.png").convert()
)
bg_night = pygame.transform.scale2x(
    pygame.image.load("assets/background-night.png").convert()
)
bg_moon = pygame.transform.scale2x(
    pygame.image.load("assets/background-moon.png").convert()
)

floor = pygame.transform.scale2x(
    pygame.image.load("assets/floor.png").convert()
)

pipe_surface = pygame.transform.scale2x(
    pygame.image.load("assets/pipe-green.png").convert()
)

coin_surface = pygame.transform.scale(
    pygame.image.load("assets/worm.png").convert_alpha(),
    (30, 30)
)

bird_frames = [
    pygame.transform.scale2x(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()),
    pygame.transform.scale2x(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()),
    pygame.transform.scale2x(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha())
]

flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
die_sound = pygame.mixer.Sound("sound/sfx_die.wav")

# ================== FONT ==================
def draw_text(text, size, x, y):
    font = pygame.font.Font("04B_19__.TTF", size)
    surf = font.render(text, True, (255, 255, 255))
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)
    return rect

# ================== GAME VARIABLES ==================
bird_index = 0
bird = bird_frames[bird_index]
bird_rect = bird.get_rect(center=(100, 384))
bird_movement = 0

pipe_list = []
coin_list = []
score = 0
game_started = False
game_active = False
floor_x = 0

pipe_height_low = [350, 380, 410, 440]
pipe_height_normal = [200, 250, 300, 350, 400, 450]

# ================== EVENTS ==================
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1800)

SPAWNCOIN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNCOIN, 3000)

BIRDFLAP = pygame.USEREVENT + 2
pygame.time.set_timer(BIRDFLAP, 200)

# ================== FUNCTIONS ==================
def create_pipe():
    y = random.choice(pipe_height_normal if score >= 10 else pipe_height_low)
    bottom = pipe_surface.get_rect(midtop=(500, y))
    top = pipe_surface.get_rect(midtop=(500, y - PIPE_GAP))
    return {"rect": bottom, "scored": False}, {"rect": top}

def move_objects(lst, speed):
    for o in lst:
        o["rect"].centerx -= speed
    return lst

def draw_pipes(pipes):
    for p in pipes:
        if p["rect"].bottom >= 600:
            screen.blit(pipe_surface, p["rect"])
        else:
            screen.blit(pygame.transform.flip(pipe_surface, False, True), p["rect"])

def check_collision():
    for p in pipe_list:
        if bird_rect.colliderect(p["rect"]):
            hit_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 650:
        die_sound.play()
        return False
    return True

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)

def reset_game():
    global bird_movement, score, pipe_list, coin_list, game_active, game_started
    bird_rect.center = (100, 384)
    pipe_list.clear()
    coin_list.clear()
    score = 0
    bird_movement = 0
    game_started = False
    game_active = False

# ================== GAME LOOP ==================
while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state == MENU:
                game_state = PLAYING
                reset_game()
            elif game_state == PLAYING:
                bird_movement = -8
                game_started = True
                game_active = True
                flap_sound.play()
            elif game_state == GAMEOVER:
                game_state = MENU
            elif game_state in (INSTRUCTIONS, HIGHSCORE):
                game_state = MENU

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == MENU:
                if play_rect.collidepoint(mouse_pos):
                    game_state = PLAYING
                    reset_game()
                if ins_rect.collidepoint(mouse_pos):
                    game_state = INSTRUCTIONS
                if hs_rect.collidepoint(mouse_pos):
                    game_state = HIGHSCORE
                if exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            elif game_state == GAMEOVER:
                game_state = MENU

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

        if event.type == SPAWNCOIN and game_active:
            coin_rect = coin_surface.get_rect(center=(500, random.randint(200, 450)))
            coin_list.append({"rect": coin_rect})

        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % 3
            bird = bird_frames[bird_index]

    # ================== BACKGROUND AUTO ==================
    if score < 10:
        screen.blit(bg_day, (0, 0))
    elif score < 20:
        screen.blit(bg_night, (0, 0))
    else:
        screen.blit(bg_moon, (0, 0))

    # ================== DRAW ==================
    if game_state == MENU:
        draw_text("FLAPPY BIRD", 40, 216, 160)
        play_rect = draw_text("PLAY", 30, 216, 260)
        ins_rect = draw_text("INSTRUCTIONS", 20, 216, 310)
        hs_rect = draw_text("HIGH SCORE", 20, 216, 350)
        exit_rect = draw_text("EXIT", 20, 216, 390)

    elif game_state == INSTRUCTIONS:
        draw_text("SPACE TO FLY", 20, 216, 300)
        draw_text("AVOID PIPES", 20, 216, 340)
        draw_text("EAT COIN +5", 20, 216, 380)
        draw_text("PRESS SPACE", 18, 216, 440)

    elif game_state == HIGHSCORE:
        draw_text("HIGH SCORE", 35, 216, 300)
        draw_text(str(high_score), 40, 216, 360)
        draw_text("PRESS SPACE", 18, 216, 430)

    elif game_state == PLAYING:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(rotate_bird(bird), bird_rect)

        pipe_list = move_objects(pipe_list, 3)
        draw_pipes(pipe_list)

        coin_list = move_objects(coin_list, 3)
        for c in coin_list[:]:
            screen.blit(coin_surface, c["rect"])
            if bird_rect.colliderect(c["rect"]):
                score += 5
                score_sound.play()
                coin_list.remove(c)

        if not check_collision():
            game_state = GAMEOVER
            high_score = max(score, high_score)
            save_high_score(high_score)

        for p in pipe_list:
            if "scored" in p and not p["scored"] and p["rect"].centerx < bird_rect.centerx:
                score += 1
                p["scored"] = True
                score_sound.play()

        draw_text(str(score), 30, 216, 100)

    elif game_state == GAMEOVER:
        draw_text("GAME OVER", 40, 216, 260)
        draw_text(f"SCORE: {score}", 25, 216, 320)
        draw_text(f"BEST: {high_score}", 25, 216, 360)
        draw_text("SPACE / CLICK TO MENU", 16, 216, 420)

    # ================== FLOOR ==================
    floor_x -= 1
    screen.blit(floor, (floor_x, 650))
    screen.blit(floor, (floor_x + 432, 650))
    if floor_x <= -432:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)
