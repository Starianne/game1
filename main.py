import pygame
from sys import exit
from random import randint 

class Player(pygame.sprite.Sprite): #inherits from pygame class
    
    def __init__(self):
        super().__init__() #overriding class
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()


        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom =(200,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300: #makes player jump
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()




def display_score():
    current_time = pygame.time.get_ticks() - start_time
    #formatting current time
    seconds = (current_time // 100) % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    minutes = current_time // 6000
    if minutes < 10:
        minutes = f"0{minutes}"
    score_surf = text_font.render(f'{minutes}:{seconds}',False,(64,64,64))
    score_rect = score_surf.get_rect(topleft = (0,0))
    screen.blit(score_surf,score_rect)
    return current_time # to use later

def obstacle_movement(obstacle_list):
    if obstacle_list: #if a list is empty python evaluates to false
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] #we only copy every item in list IF x value is bigger than -100
          
        return obstacle_list
    else: # otherwise returns none and you cant append none
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): 
                return False
    return True

def player_animation():
    #display jump surface when player is not on floor
    global player_surf, player_index

    if player_rect.bottom <300:
        player_surf = player_jump
    else:
        #play walking animation if player on floor
        player_index +=0.1 #slow animation speed between indexes
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]
    



pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = False
start_time = 0
best_time = 0

#font
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)

#background
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

player = pygame.sprite.GroupSingle()
player.add(Player())


#Obstacles
#snail
snail_frame_1= pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2= pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

#fly
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

#player
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

#intro
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400,200))
#title - intro
title_surface = text_font.render('My game', False, (111,196,169)).convert()
title_rect = title_surface.get_rect(center =(400,50))
#descript - intro
game_message = text_font.render("Press space to run",False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

#timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()    
            exit()
        if game_active:
            #jump with space
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300: #space = jump only if on floor
                    player_gravity = -20
        else:
            #restart game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        if game_active: #these are to make obstacles change frames to appear animated
            if event.type == obstacle_timer and game_active:
                if randint(0,2): #if true (1) make snail
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), 200)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else: 
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            elif event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else: 
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
    
    if game_active:
        #background surface
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        time = display_score() #get current time
        if time > best_time:
            best_time = time #set best time

        #obstacle movement
        obstacle_rect_list= obstacle_movement(obstacle_rect_list)
        

        #collision
        game_active = collisions(player_rect,obstacle_rect_list)

        #player movement
        player_gravity += 1
        player_rect.y += player_gravity

        #player floor
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        #player surface
        screen.blit(player_surf,player_rect)
        player.draw(screen)
        player.update()

        display_score()
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        #format best time
        best_seconds = (best_time // 100) % 60
        if best_seconds < 10:
            best_seconds = f"0{best_seconds}"
        best_minutes = best_time // 6000
        if best_minutes < 10:
            best_minutes = f"0{best_minutes}"

        best_time_message = text_font.render(f"Your best time is {best_minutes}:{best_seconds}",False,(111,196,169))
        best_time_message_rect = best_time_message.get_rect(center = (400,330))
        screen.blit(title_surface,title_rect)
        if best_time == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(best_time_message, best_time_message_rect)

        
    # draw all of our elements + update everything
    pygame.display.update()
    clock.tick(60) #this while true loop should not run faster than 60 frames per second