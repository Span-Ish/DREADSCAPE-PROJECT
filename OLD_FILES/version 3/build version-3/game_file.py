#IMPORT ALL MODULES AND INITIALIZE PYGAME:
import pygame, os, math
pygame.init()

#DECLARING SPECIFIC VARIABLES:
absolute_path = os.path.dirname(__file__)
SCREEN_WIDTH,SCREEN_HEIGHT = 1200,600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
fps = 60
timer = pygame.time.Clock()

#FONTS:
base_text1 = pygame.font.Font(absolute_path + r"\assets\game_font\TT Octosquares Trial Condensed Black.ttf",18)
octosquares1 = pygame.font.Font(absolute_path + r"\assets\game_font\TT Octosquares Trial Condensed Black.ttf",70)
octosquares2 = pygame.font.Font(absolute_path + r"\assets\game_font\TT Octosquares Trial Black.ttf",30)
pixeldub_1 = pygame.font.Font(absolute_path + r"\assets\game_font\pixeldub.ttf",66)
button_text1 = pygame.font.Font(absolute_path + r"\assets\game_font\pixeldub.ttf",100)

#DECLARING GAME-RELATED VARIABLES:
new_press = True
POI_LIST = [('1',(132,247),(-279,-215)),('2',(624,720),(-384,-292))] #IMP: 1. Coordinate order should always be lesser-to-greater   2. Coordinates are always relative to current player position, because they depend on player_xDisplay_mod and player_yDisplay_mod which are also relative to position
POI_DICT = {'1':True,'2':True}
wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,True
wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
battery_stack = [1,1]
battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':True}
battery_max = 6
battery_reset_event = False
picture_authorized = False

indicator_dict = {'mainD':True,'mainA':True,'mainS':True,'tabletW':True,'tabletA':True,'mapW':True,'mapD':True,'noticeD':True,'cameraA':True,'SONAR_ESCAPE':True}
outside_fadeFlag = False

#DECLARING MOVEMENT-SPECIFIC VARIABLES:
first_run = True
GAME_OVER = False
player_starting_x,player_starting_y = 0,0
player_x,player_y = 0,0
player_xDisplay,player_yDisplay,player_zDisplay = 300,300,92
check_collision = False

x,y = 0,0
TILESIZE = 48 #(image dimensions)
WORLD_MAP = [
    ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
    ['x',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',','x','x','x','x',',','x','x','x','x'],
    ['x',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',','x','x','x','x',',','x','x','x','x'],
    ['x',',',',',',',',',',',',',',',',',',',',',',','x','x','x','x',',',',',',','x','x','x',',',',','x','x','x','x'],
    ['x',',',',',',','x',',',',',',',',',',',',',',',',',',',',','x',',',',',',','x','x','x',',','x','x','x','x','x'],
    ['x',',',',',',','x',',',',',',',',',',',',',',',',',',',',','x',',',',',',','x','x','x',',','x','x','x','x','x'],
    ['x',',',',',',','x',',',',',',',',',',',',',',',',',',',',','x',',',',',',','x','x',',',',',',',',','x','x','x'],
    ['x',',',',',',','x',',',',',',',',',',',',',',',',',',',',','x',',',',',',','x','x','x','x','x',',','x','x','x'],
    ['x',',',',',',','x',',',',',',',',',',',',',',',',',',',',','x','x',',',',','x','x','x',',',',',',','x','x','x'],
    ['x',',',',',',','x',',',',',',',',',',',',',',',',',',',',',',',',',',',',','x','x','x',',','x','x','x','x','x'],
    ['x',',',',',',','x',',',',',',',',',',',',',',',',',',',',',',',',',',',',','x','x','x',',','x','x','x','x','x'],
    ['x',',',',',',','x',',',',',',',',','p',',',',',',',',',',',',',',',',',',','x','x','x',',',',',',','x','x','x'],
    ['x',',',',',',','x',',',',',',',',',',',',',',',',',',',',',',',',',',',',','x','x','x',',',',',',',',','x','x'],
    ['x',',',',',',',',',',',',',',','x',',','x',',',',',',',',',',',',',',',',','x','x','x','x','x',',',',','x','x'],
    ['x',',',',',',',',',',',',','x','x',',','x','x',',',',',',',',',',',',',',','x','x','x','x','x',',',',','x','x'],
    ['x',',',',',',',',',',',',',',','x',',','x',',',',',',',',',',',',',',',',','x','x','x','x','x',',',',','x','x'],
    ['x',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',','x'],
    ['x',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',','x'],
    ['x',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',',','x'],
    ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
  ]

#SURFACES:
title_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
backstory_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
play_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
camera_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
sonar_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
power_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
pda_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
battery_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
sonar_view_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)

#IMAGES:
#backgrounds:
title_bg = pygame.image.load(absolute_path + r'\assets\images\new_title_screen.png').convert_alpha()
title_bg = pygame.transform.scale(title_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
main_view_bg = pygame.image.load(absolute_path + r'\assets\images\main_view.png').convert_alpha()
main_view_bg = pygame.transform.scale(main_view_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
play_bg = pygame.image.load(absolute_path + r'\assets\images\play_screen.png').convert_alpha()
play_bg = pygame.transform.scale(play_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
camera_bg = pygame.image.load(absolute_path + r'\assets\images\camera_view.png').convert_alpha()
camera_bg = pygame.transform.scale(camera_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
sonar_bg = pygame.image.load(absolute_path + r'\assets\images\sonarscreen.png').convert_alpha()
sonar_bg = pygame.transform.scale(sonar_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
sonar_offline_bg = pygame.image.load(absolute_path + r'\assets\images\sonarscreen_offline.png').convert_alpha()
sonar_offline_bg = pygame.transform.scale(sonar_offline_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
power_bg = pygame.image.load(absolute_path + r'\assets\images\batteryscreen.png').convert_alpha()
power_bg = pygame.transform.scale(power_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
pda_bg = pygame.image.load(absolute_path + r'\assets\images\pdascreen.png').convert_alpha()
pda_bg = pygame.transform.scale(pda_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))


#background rectangles:
title_bg_rect = title_bg.get_rect()
play_bg_rect = play_bg.get_rect()
camera_bg_rect = camera_bg.get_rect()
main_view_bg_rect =main_view_bg.get_rect()
sonar_bg_rect = sonar_bg.get_rect()
sonar_offline_bg_rect = sonar_offline_bg.get_rect()
power_bg_rect = power_bg.get_rect()
pda_bg_rect = pda_bg.get_rect()


#assets:
battery_img6 = pygame.image.load(absolute_path + r'\assets\images\battery_6.png').convert_alpha()
battery_img6 = pygame.transform.scale(battery_img6,(200,240))
battery_img5 = pygame.image.load(absolute_path + r'\assets\images\battery_5.png').convert_alpha()
battery_img5 = pygame.transform.scale(battery_img5,(200,240))
battery_img4 = pygame.image.load(absolute_path + r'\assets\images\battery_4.png').convert_alpha()
battery_img4 = pygame.transform.scale(battery_img4,(200,240))
battery_img3 = pygame.image.load(absolute_path + r'\assets\images\battery_3.png').convert_alpha()
battery_img3 = pygame.transform.scale(battery_img3,(200,240))
battery_img2 = pygame.image.load(absolute_path + r'\assets\images\battery_2.png').convert_alpha()
battery_img2 = pygame.transform.scale(battery_img2,(200,240))
battery_img1 = pygame.image.load(absolute_path + r'\assets\images\battery_1.png').convert_alpha()
battery_img1 = pygame.transform.scale(battery_img1,(200,240))
battery_img0 = pygame.image.load(absolute_path + r'\assets\images\battery_0.png').convert_alpha()
battery_img0 = pygame.transform.scale(battery_img0,(200,240))

indicator_pic = pygame.image.load(absolute_path + r'\assets\images\indicator.png').convert_alpha()
indicator_pic = pygame.transform.scale(indicator_pic,(50,50))
indicator_pic.set_alpha(191)

fade_img = pygame.image.load(absolute_path + r'\assets\images\fade.png').convert_alpha()
fade_img = pygame.transform.scale(fade_img,(1200,600))


#UI CLASSES:
#Buttons:
class Button:
    def __init__(self,text,x_pos,y_pos,x_offset,enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_offset = x_offset
        self.enabled = enabled
        self.draw()
    
    def draw(self):
        button_Text = base_text1.render(self.text,True,'black')
        button_Rect = pygame.rect.Rect((self.x_pos,self.y_pos),(200,20))
        if self.enabled:
            if self.check_click():
                pygame.draw.rect(screen,'dark gray',button_Rect,0,5)
            else:
                pygame.draw.rect(screen,'gray',button_Rect,0,5)
        else:
            pygame.draw.rect(screen,'black',button_Rect,0,5)
        pygame.draw.rect(screen,'black',button_Rect,2,5)
        screen.blit(button_Text,(self.x_pos + self.x_offset,self.y_pos-2))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = button_rect = pygame.rect.Rect((self.x_pos,self.y_pos),(200,20))
        if left_click and self.enabled and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

class invButton:
    def __init__(self, x_pos, y_pos,b_width, b_height, b_surface, opacity,enabled, text = '',text_xoffset = 10,text_yoffset = 10,text_colour = 'white',text_font = 'pixeldub'):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.b_width = b_width
        self.b_height = b_height
        self.b_surface = b_surface
        self.opacity = opacity
        self.enabled = enabled
        self.text = text
        self.text_xoffset = text_xoffset
        self.text_yoffset = text_yoffset
        self.text_colour = text_colour
        self.text_font = text_font
        self.draw()

    def draw(self):
        if self.enabled:
            pygame.draw.rect(self.b_surface,(255,0,0,self.opacity),(self.x_pos,self.y_pos,self.b_width,self.b_height))
            if self.text_font == 'pixeldub':
                invbutton_text = pixeldub_1.render('{0}'.format(self.text),True,'{0}'.format(self.text_colour))
                self.b_surface.blit(invbutton_text,(self.x_pos + self.text_xoffset,self.y_pos + self.text_yoffset))
            elif self.text_font == 'octosquares':
                invbutton_text = octosquares1.render('{0}'.format(self.text),True,'{0}'.format(self.text_colour))
                self.b_surface.blit(invbutton_text,(self.x_pos + self.text_xoffset,self.y_pos + self.text_yoffset))

    def invcheck_Click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos,self.y_pos),(self.b_width,self.b_height))
        if self.enabled and left_click and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

class powerButtons:
    def __init__(self,text,x_pos,y_pos,enabled,active,x_offset):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.active = active
        self.x_offset = x_offset
        self.draw()
    
    def draw(self):
        button_disableText = base_text1.render(self.text,True,'white')
        button_crossText = base_text1.render('X',True,'red')
        if self.active:
            button_status = 'ON'
            button_statusText = base_text1.render(button_status,True,'green')
        else:
            button_status = 'OFF'
            button_statusText = base_text1.render(button_status,True,'dark red')
        button_Text = base_text1.render(self.text,True,'black')
        button_Rect = pygame.rect.Rect((self.x_pos,self.y_pos),(200,20))
        if self.enabled:
            if self.textcheck_click():
                pygame.draw.rect(screen,'dark gray',button_Rect,0,5)
            else:
                pygame.draw.rect(screen,'gray',button_Rect,0,5)
        else:
            pygame.draw.rect(screen,'black',button_Rect,0,5)
        pygame.draw.rect(screen,'black',button_Rect,2,5)
        if self.enabled:
            screen.blit(button_Text,(self.x_pos + self.x_offset,self.y_pos-2))
            screen.blit(button_statusText,(self.x_pos+210,self.y_pos-2))
        else:
            screen.blit(button_disableText,(self.x_pos + self.x_offset,self.y_pos-2))
            screen.blit(button_crossText,(self.x_pos+210,self.y_pos-2))

    def textcheck_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = button_rect = pygame.rect.Rect((self.x_pos,self.y_pos),(200,20))
        if left_click and self.enabled and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

class camButton:
    def __init__(self, x_pos, y_pos,b_width, b_height, b_surface, opacity,enabled, text = '',text_xoffset = 10,text_yoffset = 10,text_colour = 'white',text_font = 'pixeldub'):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.b_width = b_width
        self.b_height = b_height
        self.b_surface = b_surface
        self.opacity = opacity
        self.enabled = enabled
        self.text = text
        self.text_xoffset = text_xoffset
        self.text_yoffset = text_yoffset
        self.text_colour = text_colour
        self.text_font = text_font
        self.draw()

    def draw(self):
        #authorization rect:
        if self.enabled:
            pygame.draw.rect(self.b_surface,(0,255,0,140),(791,503,62,62))
        else:
            pygame.draw.rect(self.b_surface,(255,0,0,140),(791,503,62,62))

        #button rect:
        pygame.draw.rect(self.b_surface,(255,0,0,self.opacity),(self.x_pos,self.y_pos,self.b_width,self.b_height))
        invbutton_text = octosquares1.render('{0}'.format(self.text),True,'{0}'.format(self.text_colour))
        self.b_surface.blit(invbutton_text,(self.x_pos + self.text_xoffset,self.y_pos + self.text_yoffset))

    def camcheck_Click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos,self.y_pos),(self.b_width,self.b_height))
        if self.enabled and left_click and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

#Others:
class Indicator:
    def __init__(self,text,x_pos,y_pos,x_offset,y_offset,angle,enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.angle = angle
        self.enabled = enabled
        if self.enabled:
            self.draw()

    def draw(self):
        indicator_Text = base_text1.render(self.text,True,'black')
        new_indicator = pygame.transform.rotate(indicator_pic,self.angle)
        screen.blit(new_indicator,(self.x_pos,self.y_pos))
        screen.blit(indicator_Text,(self.x_pos + self.x_offset,self.y_pos + self.y_offset))

class fadeObject:
    def __init__(self,time):
        self.time_delay = time
        self.fade_flag = False

    def fadeIn(self): 
        global fade_img
        for alpha in range(0, 180):
            fade_img.set_alpha(alpha)
            screen.blit(fade_img, (0,0))
            pygame.display.update()
            pygame.time.delay(self.time_delay)
        self.fade_flag = True

    def fadeOut(self):
        global fade_img
        for alpha in range(180,-1,-1):
            fade_img.set_alpha(alpha)
            screen.blit(fade_img,(0,0))
            pygame.display.update()
            pygame.time.delay(self.time_delay)
        self.fade_flag = False

fadeScreen = fadeObject(10)
titleFade = fadeObject(20)
titleFade.fade_flag = True

#MOVEMENT-RELATED CLASSES:
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,x,y):
        global player_x,player_y
        super().__init__(groups)
        self.image = pygame.image.load(absolute_path + r'\assets\images\player_arrow.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48,48))
        self.rect = self.image.get_rect(center = (player_xDisplay + self.image.get_width() // 2, player_yDisplay + self.image.get_height() // 2))
        

        player_x,player_y,self.player_angle,self.player_velocity = x,y,0,[0,0]
        self.max_speed,self.max_rotationSpeed,self.current_speed,self.current_rotationSpeed = 1.5,0.005,0,0
        self.move_forward,self.move_forwardPressed,self.move_backward,self.move_backwardPressed = False,False,False,False


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load(absolute_path + r'\assets\images\obstacle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(48,48))
        self.rect = self.image.get_rect(topleft = pos)


class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.surface.Surface((1200,600))

        #sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = YSortCameraGroup()

        #sprite setup
        self.create_map()

    def create_map(self):
        global player_starting_x,player_starting_y
        player_check = False
        for row_index,row in enumerate(WORLD_MAP):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites])
                if col == 'p':
                    player_check = True
                    player_starting_x,player_starting_y = x,y
                    
                    

        if player_check:
            self.player = Player((player_starting_x,player_starting_y),[self.visible_sprites],self.obstacles_sprites,player_starting_x,player_starting_y)
    def run(self):
        global first_run
        #update and draw the game
        if first_run:
            self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.surface.Surface((1200,600))
        
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        

    def custom_draw(self, player):
        global first_run, player_starting_x, player_starting_y
        
        for sprite in self.sprites():
            if sprite == player:
                
                rotated_player_arrow = pygame.transform.rotate(sprite.image, math.degrees(sprite.player_angle))
                new_rotatedRect = rotated_player_arrow.get_rect(center=(player_xDisplay + sprite.image.get_width() // 2, player_yDisplay + sprite.image.get_height() // 2))
                self.offset.x = new_rotatedRect.centerx - self.half_width
                self.offset.y = new_rotatedRect.centery - self.half_height
                offset_rect = new_rotatedRect.topleft - self.offset
                
                player_mask = pygame.mask.from_surface(rotated_player_arrow)
                self.check_collision(player,player_mask, offset_rect)
                
            else:
                offset_rect = sprite.rect.topleft - self.offset
                sprite.mask = pygame.mask.from_surface(sprite.image)
                screen.blit(sprite.image, offset_rect)

    def check_collision(self, player,player_mask, player_rect):
        global check_collision
        #player-obstacle collision
        collision_runCondition = True
        if collision_runCondition:
            for obstacle_sprite in self.sprites():
                if obstacle_sprite != player:
                    obstacle_mask = pygame.mask.from_surface(obstacle_sprite.image)
                    obstacle_rect = obstacle_sprite.rect.topleft - self.offset
 
                    if player_mask.overlap(obstacle_mask, (obstacle_rect.x - player_rect.x, obstacle_rect.y - player_rect.y)):
                        collision_runCondition = False
                    else:
                        pass
                


        if collision_runCondition:
            check_collision = False
        else:
            check_collision = True




level = Level()

#FUNCTIONS TO RUN THE GAME (SCREENS):
def main_gameLoop():
    
    def title_screen(): 
        global new_press
        pygame.display.set_caption('Title')

        if titleFade.fade_flag:
            fade_run = True
            alpha = 180
            while fade_run:
                screen.blit(title_bg,title_bg_rect)
                fade_img.set_alpha(alpha)
                screen.blit(fade_img,(0,0))
                pygame.display.update()
                pygame.time.delay(titleFade.time_delay)
                alpha -= 2
                if alpha == 0:
                    fade_run = False
            titleFade.fade_flag = False

        title_run = True
        while title_run:
            timer.tick(fps)
            screen.blit(title_bg,title_bg_rect)
            screen.blit(title_surface,(0,0))


            play_button = invButton(411,544,176,43,title_surface,0,True)
            quit_button = invButton(614,544,176,43,title_surface,0,True)

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if play_button.invcheck_Click():
                    fadeScreen.fadeIn()
                    if fadeScreen.fade_flag:
                        backstory()

                if quit_button.invcheck_Click():
                    fadeScreen.fadeIn()
                    title_run = False

            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    title_run = False
            pygame.display.update()
        pygame.quit()
    
    def backstory():
        global new_press, fade_img
        pygame.display.set_caption('Backstory')
        back_text1 = base_text1.render('oh no government sent u here bla bla bla land rover omg wow weird research team didnt come',True,'black')
        back_text2 = base_text1.render('back no way so scary navigate a canyon spooky caves oh noes monster chasing you so spoopy',True,'black')

        if fadeScreen.fade_flag:
            fade_run = True
            alpha = 180
            while fade_run:
                screen.fill((120,130,80))
                screen.blit(back_text1,(200,200))
                screen.blit(back_text2,(200,240))
                fade_img.set_alpha(alpha)
                screen.blit(fade_img,(0,0))
                pygame.display.update()
                pygame.time.delay(fadeScreen.time_delay)
                alpha -= 2
                if alpha == 0:
                    fade_run = False
            fadeScreen.fade_flag = False

        backstory_var = True
        while backstory_var:
            timer.tick(fps)
            screen.fill((120,130,80))
            screen.blit(back_text1,(200,200))
            screen.blit(back_text2,(200,240))

            continue_button = Button('Continue',480,540,60,True)

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if continue_button.check_click():
                    fadeScreen.fadeIn()
                    if fadeScreen.fade_flag:
                        main_view()
            
            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    backstory_var = False

            pygame.display.update()
        pygame.quit()

    def main_view():
        global new_press, fade_img
        pygame.display.set_caption('Main View')

        if fadeScreen.fade_flag:
            fade_run = True
            alpha = 180
            while fade_run:
                screen.blit(main_view_bg,main_view_bg_rect)
                fade_img.set_alpha(alpha)
                screen.blit(fade_img,(0,0))
                pygame.display.update()
                pygame.time.delay(fadeScreen.time_delay)
                alpha -= 2
                if alpha == 0:
                    fade_run = False
            fadeScreen.fade_flag = False

        main_view_var = True
        while main_view_var:
            timer.tick(fps)
            screen.blit(main_view_bg,main_view_bg_rect)
            
            main_view_d_indicator = Indicator('D',1120,250,15,11,90,indicator_dict['mainD'])
            main_view_a_indicator = Indicator('A',30,250,21,11,270,indicator_dict['mainA'])
            main_view_s_indicator = Indicator('S',756,335,19,9,0,indicator_dict['mainS'])

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN,pygame.K_2,pygame.K_s):
                        indicator_dict['mainS'] = False
                        welcome_screen()
                    elif event.key in (pygame.K_RIGHT,pygame.K_6,pygame.K_d):
                        indicator_dict['mainD'] = False
                        camera_view()
                    elif event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
                        indicator_dict['mainA'] = False
                        notice_board_view()
                if event.type == pygame.QUIT:
                    main_view_var = False

            pygame.display.update()
        pygame.quit()

    def map_view():
        global new_press
        pygame.display.set_caption('Map')
        testtext2 = base_text1.render('map view',True,'black')
        map_view_var = True
        while map_view_var:
            timer.tick(fps)
            screen.fill('orange')
            screen.blit(testtext2,(200,200))
            
            map_d_indicator = Indicator('D',1130,250,15,11,90,indicator_dict['mapD'])
            map_w_indicator = Indicator('W',553,10,16,14,180,indicator_dict['mapW'])

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP,pygame.K_8,pygame.K_w):
                        indicator_dict['mapW'] = False
                        main_view()
                    elif event.key in (pygame.K_RIGHT,pygame.K_6,pygame.K_d):
                        indicator_dict['mapD'] = False
                        welcome_screen()
                if event.type == pygame.QUIT:
                    map_view_var = False

            pygame.display.update()
        pygame.quit()

    def camera_view():
        global new_press, battery_max, battery_reset_event,picture_authorized,POI_DICT,POI_LIST,player_xDisplay,player_yDisplay
        pygame.display.set_caption('Camera')
        camera_var = True
        while camera_var:
            timer.tick(fps)
            screen.blit(camera_bg,camera_bg_rect)
            screen.blit(camera_surface,(0,0))

            camera_button = camButton(316,500,408,64,camera_surface,0,picture_authorized,'CAPTURE',37,-16,'gray')

            camera_a_indicator = Indicator('A',10,250,21,11,270,indicator_dict['cameraA'])

            test_button1 = Button('battery toggle 5',400,200,20,True)
            test_button2 = Button('battery toggle 4',700,200,20,True)
            test_button3 = Button('battery toggle 2',1000,200,20,True)

            player_xDisplay_mod = round(player_xDisplay - 432,2)
            player_yDisplay_mod = round(player_yDisplay - 432,2)
            current_poi = 0
            for cords in POI_LIST:
                if (cords[1][0] <= player_xDisplay_mod  <= cords[1][1]) and (cords[2][0] <= player_yDisplay_mod <= cords[2][1]) and picture_authorized:
                    current_poi = cords[0]

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if camera_button.camcheck_Click():
                    POI_DICT[current_poi] = False

                if test_button1.check_click():
                    battery_max = 5
                    battery_reset_event = True
                elif test_button2.check_click():
                    battery_max = 4
                    battery_reset_event = True
                elif test_button3.check_click():
                    battery_max = 2
                    battery_reset_event = True

            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

                

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
                        indicator_dict['cameraA'] = False
                        main_view()
                if event.type == pygame.QUIT:
                    camera_var = False

            pygame.display.update()
        pygame.quit()

    def welcome_screen():
        global new_press
        pygame.display.set_caption('Play')
        play_run = True
        while play_run:
            timer.tick(fps)
            screen.blit(play_bg,play_bg_rect)
            screen.blit(play_surface,(0,0))

            sonar_button = invButton(168,95,273,74,play_surface,0,True,'SONAR',21,8,'#01240b')
            power_button = invButton(463,95,273,74,play_surface,0,True,'POWER',20,8,'#01240b')
            pda_button = invButton(760,95,273,74,play_surface,0,True,'COMMS',16,8,'#01240b')

            tablet_a_indicator = Indicator('A',10,250,21,11,270,indicator_dict['tabletA'])
            tablet_w_indicator = Indicator('W',553,10,16,14,180,indicator_dict['tabletW'])

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if sonar_button.invcheck_Click():
                    sonar_screen()
                elif power_button.invcheck_Click():
                    power_screen()
                elif pda_button.invcheck_Click():
                    pda_screen()

            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP,pygame.K_8,pygame.K_w):
                        indicator_dict['tabletW'] = False
                        main_view()
                    elif event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
                        indicator_dict['tabletA'] = False
                        map_view()
                if event.type == pygame.QUIT:
                    play_run = False
            

            pygame.display.update()
        pygame.quit()

    def sonar_screen():
        global new_press,sonar_check_status
        pygame.display.set_caption('Sonar')
        sonar_run = True
        while sonar_run:
            timer.tick(fps)

            if not sonar_check_status:
                screen.blit(sonar_offline_bg,sonar_offline_bg_rect)
                screen.blit(sonar_surface,(0,0))
            else:
                screen.blit(sonar_bg,sonar_bg_rect)
                screen.blit(sonar_surface,(0,0))

                activate_sonar_button = invButton(409,392,396,104,sonar_surface,0,sonar_check_status,'ACTIVATE',30,5,'#170200','octosquares')

                if pygame.mouse.get_pressed()[0] and new_press:
                    new_press = False
                    if power_button.invcheck_Click():
                        power_screen()
                    elif pda_button.invcheck_Click():
                        pda_screen()
                    elif activate_sonar_button.invcheck_Click():
                        sonar_view()
                
                if not pygame.mouse.get_pressed()[0] and not new_press:
                    new_press = True

            power_button = invButton(463,95,273,74,sonar_surface,0,True,'POWER',20,8,'#01240b')
            pda_button = invButton(760,95,273,74,sonar_surface,0,True,'COMMS',16,8,'#01240b')
            sonar_text = pixeldub_1.render('SONAR',True,'#01240b')
            sonar_surface.blit(sonar_text,(189,103))

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if power_button.invcheck_Click():
                    power_screen()
                elif pda_button.invcheck_Click():
                    pda_screen()

            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sonar_run = False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP,pygame.K_8,pygame.K_w):
                        indicator_dict['tabletW'] = False
                        main_view()
                    elif event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
                        indicator_dict['tabletA'] = False
                        map_view()
            pygame.display.update()
        pygame.quit()


    def sonar_view():
        global GAME_OVER,player_x,player_y,first_run,player_xDisplay,player_yDisplay,player_starting_x,player_starting_y,check_collision,battery_max,POI_LIST,POI_DICT,picture_authorized
        if first_run:
            player_xDisplay,player_yDisplay = player_starting_x,player_starting_y
        
        sonar_view_run = True
        while sonar_view_run:
            screen.fill('#2A0700')
            screen.blit(sonar_view_surface,(0,0))


            timer.tick(fps)

            if GAME_OVER:
                game_over_screen()
            
            level.run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        indicator_dict['SONAR_ESCAPE'] = False
                        level.player.move_forward,level.player.move_forwardPressed,level.player.move_backward,level.player.move_backwardPressed = False,False,False,False
                        sonar_view_run = False
                    
                    #retrieve forward-backward speed
                    elif event.key == pygame.K_w and not level.player.move_forwardPressed:
                        if not level.player.move_backward:
                            level.player.move_forward = not level.player.move_forward
                            if level.player.move_forward:
                                level.player.current_speed = level.player.max_speed
                            else:
                                level.player.current_speed = 0
                        level.player.move_forwardPressed = True
                    if event.key == pygame.K_s and not level.player.move_backwardPressed:
                        if not level.player.move_forward:
                            level.player.move_backward = not level.player.move_backward
                            if level.player.move_backward:
                                level.player.current_speed = -level.player.max_speed//4
                            else:
                                level.player.current_speed = 0
                        level.player.move_backwardPressed = True
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        level.player.move_forwardPressed = False
                    elif event.key == pygame.K_s:
                        level.player.move_backwardPressed = False
            
            #retrieve rotation angle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                if level.player.current_rotationSpeed < level.player.max_rotationSpeed:
                    level.player.current_rotationSpeed += 0.02
                level.player.player_angle += level.player.current_rotationSpeed
            elif keys[pygame.K_d]:
                if level.player.current_rotationSpeed < level.player.max_rotationSpeed:
                    level.player.current_rotationSpeed += 0.02
                level.player.player_angle -= level.player.current_rotationSpeed
            else:
                level.player.current_rotationSpeed = max(0,level.player.current_rotationSpeed -0.01)
            
            #adjust velocity based on rotation and movement speeds
            if level.player.move_forward or level.player.move_backward:
                level.player.player_velocity[0] = -level.player.current_speed * math.sin(level.player.player_angle)
                level.player.player_velocity[1] = -level.player.current_speed * math.cos(level.player.player_angle)
            else:
                level.player.player_velocity[0],level.player.player_velocity[1] = 0,0
            
            #update player positions
            level.player.rect.centerx += level.player.player_velocity[0]
            level.player.rect.centery += level.player.player_velocity[1]
            player_xDisplay += level.player.player_velocity[0]
            player_yDisplay += level.player.player_velocity[1]

            #rotate image based on angle and put in at the center
            rotated_playerArrow = pygame.transform.rotate(level.player.image,math.degrees(level.player.player_angle))
            rotated_playerArrow_rect = rotated_playerArrow.get_rect(center = (600,300))
            screen.blit(rotated_playerArrow,rotated_playerArrow_rect.topleft)


            first_run = False
            level.visible_sprites.custom_draw(level.player)
            player_xDisplay_mod = round(player_xDisplay - 432,2)
            player_yDisplay_mod = round(player_yDisplay - 432,2)
            x_Cord = base_text1.render('X: {0}m'.format(player_xDisplay_mod),True,'white')
            y_Cord = base_text1.render('Y: {0}m'.format(player_yDisplay_mod),True,'white')
            screen.blit(x_Cord,(1000,50))
            screen.blit(y_Cord,(1000,80))
            if battery_max == 6:
                player_zDisplay = 92
            elif battery_max == 5:
                player_zDisplay = 108
            elif battery_max == 4:
                player_zDisplay = 124
            elif battery_max == 3:
                player_zDisplay = 158
            elif battery_max == 2:
                player_zDisplay = 196
            z_Cord = base_text1.render('Z: {0}m'.format(player_zDisplay),True,'white')
            screen.blit(z_Cord,(1000,110))
            sonar_view_d_indicator = Indicator('ESC',10,10,13,12,270,indicator_dict['SONAR_ESCAPE'])
            
            #checking for POIs:
            intersect_POI = False
            for cords in POI_LIST:
                if (cords[1][0] <= player_xDisplay_mod  <= cords[1][1]) and (cords[2][0] <= player_yDisplay_mod <= cords[2][1]):
                    intersect_POI = True
                    picture_authorized = True
                if intersect_POI:
                    pass
                else:
                    picture_authorized = False
                

            #checking for collision:
            if check_collision:
                game_over_screen()

            pygame.display.update()

    def game_over_screen():
        enter_GO = True
        if enter_GO:
            fade_run = True
            alpha = 180
            while fade_run:
                fade_img.set_alpha(alpha)
                screen.blit(fade_img,(0,0))
                pygame.display.update()
                pygame.time.delay(20)
                alpha -= 2
                if alpha == 0:
                    fade_run = False
            enter_GO = False

        pygame.display.set_caption('Game Over')
        while True:
            screen.fill('black')
            text = octosquares2.render('GAME OVER',True,'#9c1947')
            screen.blit(text,(490,250))
            timer.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()
                

    def power_screen():
        global new_press, wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled, battery_stack, battery_dict, battery_max, battery_reset_event

        if battery_reset_event:
            wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
            wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
            battery_stack = [1]
            battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
            battery_reset_event = False
        pygame.display.set_caption('Power')
        power_run = True
        while power_run:
            timer.tick(fps)
            screen.blit(power_bg,power_bg_rect)
            screen.blit(power_surface,(0,0))
            #change battery on screen based on battery_stack:
            if battery_max == 6:
                if len(battery_stack) == 6:
                    screen.blit(battery_img0,(214,230))
                elif len(battery_stack) == 5:
                    screen.blit(battery_img1,(214,230))
                elif len(battery_stack) == 4:
                    screen.blit(battery_img2,(214,230))
                elif len(battery_stack) == 3:
                    screen.blit(battery_img3,(214,230))
                elif len(battery_stack) == 2:
                    screen.blit(battery_img4,(214,230))
                elif len(battery_stack) == 1:
                    screen.blit(battery_img5,(214,230))
                elif len(battery_stack) == 0:
                    screen.blit(battery_img6,(214,230))
            elif battery_max == 5:
                if len(battery_stack) == 5:
                    screen.blit(battery_img0,(214,230))
                elif len(battery_stack) == 4:
                    screen.blit(battery_img1,(214,230))
                elif len(battery_stack) == 3:
                    screen.blit(battery_img2,(214,230))
                elif len(battery_stack) == 2:
                    screen.blit(battery_img3,(214,230))
                elif len(battery_stack) == 1:
                    screen.blit(battery_img4,(214,230))
                elif len(battery_stack) == 0:
                    screen.blit(battery_img5,(214,230))
            elif battery_max == 4:
                if len(battery_stack) == 4:
                    screen.blit(battery_img0,(214,230))
                elif len(battery_stack) == 3:
                    screen.blit(battery_img1,(214,230))
                elif len(battery_stack) == 2:
                    screen.blit(battery_img2,(214,230))
                elif len(battery_stack) == 1:
                    screen.blit(battery_img3,(214,230))
                elif len(battery_stack) == 0:
                    screen.blit(battery_img4,(214,230))
            elif battery_max == 3:
                if len(battery_stack) == 3:
                    screen.blit(battery_img0,(214,230))
                elif len(battery_stack) == 2:
                    screen.blit(battery_img1,(214,230))
                elif len(battery_stack) == 1:
                    screen.blit(battery_img2,(214,230))
                elif len(battery_stack) == 0:
                    screen.blit(battery_img3,(214,230))
            elif battery_max == 2:
                if len(battery_stack) == 2:
                    screen.blit(battery_img0,(214,230))
                elif len(battery_stack) == 1:
                    screen.blit(battery_img1,(214,230))
                elif len(battery_stack) == 0:
                    screen.blit(battery_img2,(214,230))
            elif battery_max == 1:
                if len(battery_stack) == 1:
                    screen.blit(battery_img0,(214,230))
                elif len(battery_stack) == 0:
                    screen.blit(battery_img1,(214,230))
            
            if len(battery_stack) == battery_max:
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = battery_dict['wheels'],battery_dict['sonar'],battery_dict['ls'],battery_dict['camera'],battery_dict['scanner'],battery_dict['lights']
            else:
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True

            sonar_button = invButton(168,95,273,74,power_surface,0,True,'SONAR',21,8,'#01240b')
            pda_button = invButton(760,95,273,74,power_surface,0,True,'COMMS',16,8,'#01240b')
            power_text = pixeldub_1.render('POWER',True,'#01240b')
            power_surface.blit(power_text,(483,103))

            wheels_check = powerButtons('WHEELS',650,240,wheels_check_enabled,wheels_check_status,64)
            sonar_check = powerButtons('SONAR',650,280,sonar_check_enabled,sonar_check_status,68)
            ls_check = powerButtons('LIFE SUPPORT',650,320,ls_check_enabled,ls_check_status,38)
            camera_check = powerButtons('CAMERA',650,360,camera_check_enabled,camera_check_status,62)
            scanner_check = powerButtons('SCANNER',650,400,scanner_check_enabled,scanner_check_status,58)
            lights_check = powerButtons('LIGHTS',650,440,lights_check_enabled,lights_check_status,66)

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if sonar_button.invcheck_Click():
                    sonar_screen()
                elif pda_button.invcheck_Click():
                    pda_screen()
                
                if wheels_check.textcheck_click():
                    if wheels_check_status == False and len(battery_stack) <= 6:
                        wheels_check_status = True
                        battery_stack.append(1)
                        battery_dict['wheels'] = True
                    else:
                        wheels_check_status = False
                        battery_stack.pop()
                        battery_dict['wheels'] = False

                if sonar_check.textcheck_click():
                    if sonar_check_status == False and len(battery_stack) <= 6:
                        sonar_check_status = True
                        battery_stack.append(1)
                        battery_dict['sonar'] = True
                    else:
                        sonar_check_status = False
                        battery_stack.pop()
                        battery_dict['sonar'] = False

                if ls_check.textcheck_click():
                    if ls_check_status == False and len(battery_stack) <= 6:
                        ls_check_status = True
                        battery_stack.append(1)
                        battery_dict['ls'] = True
                    else:
                        ls_check_status = False
                        battery_stack.pop()
                        battery_dict['ls'] = False

                if camera_check.textcheck_click():
                    if camera_check_status == False and len(battery_stack) <= 6:
                        camera_check_status = True
                        battery_stack.append(1)
                        battery_dict['camera'] = True
                    else:
                        camera_check_status = False
                        battery_stack.pop()
                        battery_dict['camera'] = False

                if scanner_check.textcheck_click():
                    if scanner_check_status == False and len(battery_stack) <= 6:
                        scanner_check_status = True
                        battery_stack.append(1)
                        battery_dict['scanner'] = True
                    else:
                        scanner_check_status = False
                        battery_stack.pop()
                        battery_dict['scanner'] = False

                if lights_check.textcheck_click():
                    if lights_check_status == False and len(battery_stack) <= 6:
                        lights_check_status = True
                        battery_stack.append(1)
                        battery_dict['lights'] = True
                    else:
                        lights_check_status = False
                        battery_stack.pop()
                        battery_dict['lights'] = False
                        
            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP,pygame.K_8,pygame.K_w):
                        indicator_dict['tabletW'] = False
                        main_view()
                    elif event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
                        indicator_dict['tabletA'] = False
                        map_view()
                        
                if event.type == pygame.QUIT:
                    power_run = False
            pygame.display.update()
        pygame.quit()

    def pda_screen():
        global new_press
        pygame.display.set_caption('PDA')
        pda_run = True
        while pda_run:
            timer.tick(fps)
            screen.blit(pda_bg,pda_bg_rect)
            screen.blit(pda_surface,(0,0))

            sonar_button = invButton(168,95,273,74,power_surface,0,True,'SONAR',21,8,'#01240b')
            power_button = invButton(463,95,273,74,sonar_surface,0,True,'COMMS',16,8,'#01240b')

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if sonar_button.invcheck_Click():
                    sonar_screen()
                elif power_button.invcheck_Click():
                    power_screen()


            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP,pygame.K_8,pygame.K_w):
                        indicator_dict['tabletW'] = False
                        main_view()
                    elif event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
                        indicator_dict['tabletA'] = False
                        map_view()
                if event.type == pygame.QUIT:
                    pda_run = False
            pygame.display.update()
        pygame.quit()

    def notice_board_view():
        global new_press,POI_DICT
        pygame.display.set_caption('Notice Board')
        testtext5 = base_text1.render('notice board view',True,'white')

        notice_board_var = True
        while notice_board_var:
            timer.tick(fps)
            screen.fill('dark blue')
            screen.blit(testtext5,(200,200))
            
            notice_board_d_indicator = Indicator('D',1130,250,15,11,90,indicator_dict['noticeD'])

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RIGHT,pygame.K_6,pygame.K_d):
                        indicator_dict['noticeD'] = False
                        main_view()
                if event.type == pygame.QUIT:
                    notice_board_var = False

            pygame.display.update()
        pygame.quit()
    

    title_screen()
main_gameLoop()

'''
def menufunction():
    global new_press
    pygame.display.set_caption('')
    run_var = True
    while run_var:
        timer.tick(fps)
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_var = False

        pygame.display.update()
    pygame.quit()
'''


'''
TASKS:
* [DONE] UPDATE THE POWER MENU - CREATE CLICKABLE OPTIONS FOR (Wheels, Sonar, Life Support, Camera, Scanner, Lights)
* [DONE] DISABLE SYSTEMS WHEN CERTAIN POWER OPTIONS ARE TURNED OFF (ex. place message over sonar screen saying 'offline' when no power is supplied to sonar)
* CREATE THE MAIN AREA WITH THE TABLE AND OXYGEN METER,
   [DONE] THEN ADD A MAP ON THE LEFT OF THE TABLET,
   [DONE] THEN ADD A CAMERA AND RADIO LOCATION ON THE WALL ON THE RIGHT OF THE TABLE. 
   [DONE] ADD FUNCTIONALITY TO SWITCH BETWEEN MENUS USING ARROW KEYS OR CLICKABLE ELEMENTS ON THE SCREEN
* ADD BATTERY FUNCTIONALITY (POWER METERS, REDESIGN BATTERY)
    [DONE] ADD RELATIVE DIRECTORIES
    [DONE] ADD THE IMAGES AND THEN THE OPERATIONS TO CHANGE PICTURES BASED ON SELECTIONS
* CREATE A:
    [DONE] FADE CLASS
    [DONE] TRANSITION CLASS
* [DONE] ADD A NOTICE BOARD ON THE LEFT TO STORE GUIDELINES ON USING THE SYSTEMS IN THE ROVER
* [LONG] ADJUST THE BATTERY SO THAT:
    [DONE] THE TOTAL AVAILABLE BATTERY LEVEL CAN DECREASE (available power can go down as the game progresses)
    [DONE] THE BATTERY STACK RESETS WHEN MAX AVAILABLE BATTERY GOES DOWN, AND THAT LIFE SUPPORT IS ON BY DEFAULT
    [DONE] THE BUTTONS CANNOT BE ACTIVATED AND GET DISABLED IF THE BATTERY STACK IS FULL
* [DONE] ADD INDICATORS THAT POP UP ONLY AT THE START OF THE GAME TO SHOW WHAT THE CONTROLS ARE
* [DONE] TEST OUT ADDING THE ENTIRE GAME WITHIN ANOTHER FUNCTION SO THAT EXTERNAL EFFECTS LIKE FADING AND CONTROL INDICATORS ONLY POP UP FOR A CERTAIN TIME
* [DONE] (LONG) ADD SCANNER TO THE GAME (certain points on the map glow red and u can scan them if u look at it, scanning an item adds an entry to the pda)
* [DONE] (LONG) REDO AND ANIMATE THE TITLE SCREEN IMAGE AND BUTTON LAYOUTS (visual effects on press can be done later)
-------------------
* (LONG) START WORKING ON:
    [DONE] MOVEMENT SYSTEM AND SONAR DISPLAY
    [DONE] ADD X,Y,Z COORDINATES TO THE SONAR DISPLAY
* (LONG) DECORATE THE NOTICE BOARD AND CAMERA VIEWS, THEN ADD AND TEST NOTICE BOARD FUNCTIONALITY EITHER THROUGH POP-UPS OR THROUGH WRITTEN TEXT FOR GAME CONTROLS AND OBJECTIVES
* [DONE] INTEGRATE AN X-Y-Z COORDINATE SYSTEM INTO THE SONAR VIEW SCREEN
* [DONE] FIX THE POIS SO THAT EACH OF THEM HAVE A UNIQUE IDENTIFIER AND ARE EITHER CREATED DIRECTLY ON THE MAP OR ARE STORED EXTERNALLY. THEY SHOULD ACTIVATE THE AUTHORIZATION SEQUENCE IF THE PLAYER OVERLAPS IN THEIR AREA
* [DONE] ADD CAMERA FUNCTIONALITY SO THAT IT TAKES PICTURES WITH SINE WAVES FOR THE RADIO WHENEVER THE PLAYER PRESSES THE 'CAPTURE' BUTTON. ALSO ONLY ALLOW PICTURE-TAKING WHEN PLAYERS ARE AUTHORIZED TO DO SO
-------------------
* CREATE THE BACKGROUND STORY AND ADD IT TO THE BACKSTORY PAGE
* ADD THE OXYGEN METER TO THE FRONT IN THE MAIN VIEW. IT IS CONTAINED WITHIN A CLASS AND IT UPDATES WHEN CALLED SPECIFICALLY (based on in-game events). FOR TESTING PURPOSES, IT UPDATES WHEN THE BATTERY LEVEL GOES DOWN.
* DEVELOP THE PDA/COMMS SCREEN. IT SHOULD CONTAIN THE OPTIONS TO SELECT DATA LOGS(from ship scans),SCAN LOGS(based on environmental data), AND COMMUNICATIONS(external help from the VC).
     DATA LOGS SHOULD ONLY BE UPDATED WITH INFO SENT FROM WRECKAGE SCANS (scanning the HEMS, only adds entries based on the scanner button in the camera room)
     COMMUNICATIONS SHOULD UPDATE RARELY (most significant instance is the external broadcast from an official on the mission team informing you wont be coming back)
     SCAN LOGS SHOULD CONSTANTLY UPDATE WITH INFORMATION SO LONG AS THE SCANNER IS TURNED ON IN THE POWER SECTION. SPECIFIC ENVIRONMENTAL DETAILS AND SCANS OCCUR AS THE PLAYER MOVES FORWARD/PROGRESSES THROUGH THE GAME. MOST SIGNIFACT USES WOULD BE FOR WORLDBUILDING WHEN SCANNING THE MONSTER IN THE END OR THE CAVES IT CREATES THROUGHOUT THE GAME
* ADD THE SCANNER IN THE CAMERA ROOM. IT ONLY WORKS WHEN TURNED ON AND WHEN AUTHORIZED (seperate from picture authorization). IT SCANS INFO AND PLACES IT UNDER THE "SCAN LOGS" SECTION IN THE PDA.
'''