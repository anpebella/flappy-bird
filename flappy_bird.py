from pygame import*
from random import randint
from time import sleep

init()
window_size=1200,800
window=display.set_mode(window_size)
clock=time.Clock()

player_rect=Rect(150,window_size[1]/2-100,100,100)
main_font=font.Font(None, 100)
player_img=transform.scale(image.load('atribute/bird.png'),(100,100))
wall_img=image.load('atribute/column.png')
resume_btn=transform.scale(image.load('atribute/resume-btn.png'),(150,50))
resume_rect=Rect(525,375,150,50)
score=0
lose=False
run=True
y_well=2
fall_speed=0
wall_speed=10

def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distance=650):
   pipes = []
   start_x = window_size[0]
   for i in range(count):
       height = randint(min_height, max_height)
       top_pipe = Rect(start_x, 0, pipe_width, height)
       top=transform.scale(wall_img,(pipe_width,height))
       top_img=transform.flip(top,False,True)
       bottom_pipe = Rect(start_x, height + gap, pipe_width, window_size[1] - (height + gap))
       a=window_size[1] - (height + gap)
       bottom_img=transform.scale(wall_img,(pipe_width,a))
       pipes.append((top_pipe, top_img))
       pipes.append((bottom_pipe, bottom_img))
       start_x += distance
   return pipes

pipes = generate_pipes(150)

while run:
    for e in event.get():
        x,y=mouse.get_pos()
        keys=key.get_pressed()
        if e.type==QUIT:
            quit()
        if e.type==MOUSEBUTTONDOWN:
            if lose==True and resume_rect.collidepoint(x,y):
                lose=False
                run=True
                fall_speed = 0
                player_rect.x = 150
                player_rect.y = window_size[1] / 2 - 100
                pipes = generate_pipes(150)
                score = 0

    window.fill((25,120,200))
    window.blit(player_img,(player_rect.x,player_rect.y))
    score_text=main_font.render(f'{int(score)}',True,'black')

    for pipe,pipe_img in pipes:
        if not lose:
            pipe.x-=wall_speed
        window.blit(pipe_img,(pipe.x,pipe.y))
        if pipe.x<=-100:
            pipes.remove((pipe,pipe_img))
            score+=0.5
        if player_rect.colliderect(pipe):
            lose=True
    if len(pipes)<8:
        pipes+=generate_pipes(150)

    window.blit(score_text, (590, 20))

    if not lose:
        if keys[K_w]:
            player_rect.y -= 10
        if keys[K_s]:
            player_rect.y += 10

    if lose:
        if player_rect.y < window_size[1] - player_rect.height:
            fall_speed += 0.5
            player_rect.y += fall_speed
        else:
            window.fill('black')
            window.blit(resume_btn,(resume_rect.x,resume_rect.y))

    
    display.update()
    clock.tick(60)