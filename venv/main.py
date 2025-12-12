import pygame
from sys import exit

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    seconds = (current_time // 100) % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    minutes = current_time // 6000
    if minutes < 10:
        minutes = f"0{minutes}"
    score_surf = text_font.render(f'{minutes}:{seconds}',False,(64,64,64))
    score_rect = score_surf.get_rect(topleft = (0,0))
    screen.blit(score_surf,score_rect)

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = True
start_time = 0

#font
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)

#background
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()



#snail
snail_surface= pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))

#player
player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

#intro
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400,200))
#title - intro
title_surface = text_font.render('My game', False, (111,196,169)).convert()
title_rect = title_surface.get_rect(center =(400,50))

game_message = text_font.render("Press space to run",False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()    
            exit()
        if game_active:
            if event.type ==pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300: #space = jump only if on floor
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = pygame.time.get_ticks()
    
    if game_active:
        #background surface
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        

        #snail movement
        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surface,snail_rect)

        #collision
        if snail_rect.colliderect(player_rect):
            game_active=False

        #player movement
        player_gravity += 1
        player_rect.y += player_gravity

        #player floor
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        #player surface
        screen.blit(player_surf,player_rect)
        display_score()
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surface,title_rect)
        screen.blit(game_message, game_message_rect)

        
    # draw all of our elements + update everything
    pygame.display.update()
    clock.tick(60) #this while true loop should not run faster than 60 frames per second