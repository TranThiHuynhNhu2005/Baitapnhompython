import pygame, sys, random
#Tạo hàm cho trò chơi
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
def create_pipe():
    if score < 10:
        random_pipe_pos = random.choice(pipe_height_low)
    else:
        random_pipe_pos = random.choice(pipe_height_normal)
    bottom_rect = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_rect = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 900))
    bottom_pipe = {"rect": bottom_rect, "scored": False}
    top_pipe = {"rect": top_rect}
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe["rect"].centerx -= 3
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        rect = pipe["rect"]
        if rect.bottom >= 600:
            screen.blit(pipe_surface, rect)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, rect)

def check_collision(pipes):
    # Va chạm với ống
    for pipe in pipes:
        if bird_rect.colliderect(pipe["rect"]):
            hit_sound.play()
            return False

    # Va chạm trần hoặc sàn
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        die_sound.play()
        return False
    return True

def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
	return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,630))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen= pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19__.TTF',35)
#Tạo các biến cho trò chơi
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
#chèn background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
#chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]
#bird= pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))

#tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)
#tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[]
#tạo timer
spawnpipe= pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1800)
pipe_height_low = [350, 380, 410, 440]   # Ống thấp (dễ lúc đầu)
pipe_height_normal = [200, 250, 300, 350, 400, 450]  # Bình thường
#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))
#Chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
<<<<<<< HEAD
score_sound = pygame.mixer.Sound('sound/sfx_point.wav') 

=======
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
die_sound = pygame.mixer.Sound('sound/sfx_die.wav')
>>>>>>> f8b0d56feef9a88c62bb42c34dd799d7c08f94f4
#while loop của trò chơi
while True:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement =-8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                score = 0
                pipe_passed = False

        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index =0 
            bird, bird_rect = bird_animation()    
            
    screen.blit(bg,(0,0))
    if game_active:
        # ===== CHIM =====
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        # kiểm tra va chạm
        game_active = check_collision(pipe_list)

        # ===== ỐNG =====
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        # ===== TÍNH ĐIỂM (CHỈ KHI GAME ĐANG CHẠY) =====
        for pipe in pipe_list:
            # chỉ xét ống dưới
            if "scored" in pipe:
                if pipe["rect"].centerx < bird_rect.centerx and not pipe["scored"]:
                    score += 1
                    score_sound.play()
                    pipe["scored"] = True

        score_display('main game')

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    #sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos =0
     
    pygame.display.update()
    clock.tick(120)
