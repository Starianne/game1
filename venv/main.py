import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

#font
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)

#background
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#title
title_surface = text_font.render('My game', False, (64,64,64)).convert()
title_rect = title_surface.get_rect(center =(400,100))

#snail
snail_surface= pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))

#player
player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()    
            exit()

        if event.type ==pygame.MOUSEBUTTONDOWN:
           if player_rect.collidepoint(event.pos):
               player_gravity = -20
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom == 300: #space = jump only if on floor
                player_gravity = -20
        
    #background surface
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))

    #title surface
    pygame.draw.rect(screen, '#c0e8ec', title_rect)
    pygame.draw.rect(screen, '#c0e8ec', title_rect,20)

    screen.blit(title_surface,title_rect)

    #snail movement
    snail_rect.x -= 4
    if snail_rect.right <= 0:
        snail_rect.left = 800
    screen.blit(snail_surface,snail_rect)

    #player movement
    player_gravity += 1
    player_rect.y += player_gravity
    player_rect.left += 1

    #player floor
    if player_rect.bottom >= 300:
        player_rect.bottom = 300

    screen.blit(player_surf,player_rect)

    # draw all of our elements + update everything
    pygame.display.update()
    clock.tick(60) #this while true loop should not run faster than 60 frames per second