import pygame, sys, random
#tạo hàm
def draw_floor():
    screen.blit(floor,(floor_x_pos, 650))
    screen.blit(floor,(floor_x_pos+432, 650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes :
        pipe.centerx -= 5  
    return pipes
def draw_pipe(pipes):
    for pipe in pipes :
        if pipe.bottom >= 786:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe) 
pygame.init()
screen= pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
#tạo biến
gravity = 0.25
bird_movement = 0
#background
background = pygame.image.load('assets/background-night.png').convert()
background = pygame.transform.scale2x(background)
#floor
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#bird
bird = pygame.image.load('assets/yellowbird-midflap.png').convert()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))
#tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
#tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)     
pipe_height = [200,300,400]  
while True:
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = -11   
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
    screen.blit(background, (0,0))
    #chim
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird, bird_rect)
    #ống
    pipe_list = move_pipe(pipe_list)
    draw_pipe(pipe_list)
    #sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
       floor_x_pos = 0 
   
    pygame.display.update() 
    clock.tick(120)