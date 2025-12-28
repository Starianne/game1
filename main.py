import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite): #inherits from pygame class

    def __init__(self):
        super().__init__() #overriding class
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom =(80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300: #makes player jump
            self.gravity = -20
            self.jump_sound.play()

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

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1= pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2= pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0 #spawn object
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self): #obstacle animation
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    #formatting current time
    seconds = (current_time // 1000) % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    minutes = current_time // 60000
    if minutes < 10:
        minutes = f"0{minutes}"
    score_surf = text_font.render(f'{minutes}:{seconds}',False,(64,64,64))
    score_rect = score_surf.get_rect(topleft = (10,10))
    screen.blit(score_surf,score_rect)
    return current_time # to use later


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False): #sprite, group , boolean are arguments
        obstacle_group.empty() #get rid of all sprites on screen so you arent stuck after dying
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((1720,1010))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = False
start_time = 0
best_time = 0
#sets music:
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

#font
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)

#background
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()    
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail'])))
        else:
            #restart game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
            
    
    if game_active:
        #background surface
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        time = display_score() #get current time
        if time > best_time:
            best_time = time #set best time

        game_active = collision_sprite()

#put player sprite on screen
        player.draw(screen)
        player.update()

#put obstacle sprites on screen
        obstacle_group.draw(screen)
        obstacle_group.update()

        display_score()
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        #format best time
        best_seconds = (best_time // 1000) % 60
        if best_seconds < 10:
            best_seconds = f"0{best_seconds}"
        best_minutes = best_time // 60000
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