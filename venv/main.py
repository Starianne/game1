import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

test_surface = pygame.Surface((100,200))
test_surface.fill('coral')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        
    screen.blit(test_surface, (200,100))
    
    # draw all of our elements + update everything
    pygame.display.update()
    clock.tick(60) #this while true loop should not run faster than 60 frames per second