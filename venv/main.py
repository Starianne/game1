import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

text_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

title_surface = text_font.render('My game', False, 'Black').convert()
title_rect = title_surface.get_rect(center =(400,100))

snail_surface= pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type ==pygame.MOUSEMOTION:
            #print(event.pos)
            if player_rect.collidepoint(event.pos):
                print("boo")

        
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    pygame.draw.rect(screen, 'Pink', title_rect)
    pygame.draw.rect(screen, 'Pink', title_rect,10)
    screen.blit(title_surface,title_rect)

    snail_rect.x -= 4
    if snail_rect.right <= 0:
        snail_rect.left = 800
    screen.blit(snail_surface,snail_rect)

    player_rect.left += 1
    screen.blit(player_surf,player_rect)
    
    #if player_rect.colliderect(snail_rect):
        #print('collision')


    #mouse_pos = pygame.mouse.get_pos()
    #if player_rect.collidepoint(mouse_pos):
        #print(pygame.mouse.get_pressed())

    # draw all of our elements + update everything
    pygame.display.update()
    clock.tick(60) #this while true loop should not run faster than 60 frames per second