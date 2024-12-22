#IMPORT ALL MODULES AND INITIALIZE PYGAME:
import pygame, os, math, random
from level_data_file import *
from images_file import *
from pythonvideoplayerscript import Video

pygame.init()
pygame.mixer.init(buffer = 2048) 

#DECLARING SPECIFIC VARIABLES:
absolute_path = os.path.dirname(__file__)
SCREEN_WIDTH,SCREEN_HEIGHT = 1200,600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('DreadScape')
pygame.display.set_icon(ds_icon)
fps = 30
timer = pygame.time.Clock()
#SURFACES:
title_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
backstory_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
play_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
camera_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
map_view_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
notice_board_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
notice_board_open_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
sonar_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
power_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
pda_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
battery_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
sonar_view_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
base_scan_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
base_data_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
base_comms_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)
end_animation_surface = pygame.Surface((swidth,sheight),pygame.SRCALPHA)


#FONTS:
base_text1 = pygame.font.Font(absolute_path + r"\assets\game_font\TT Octosquares Trial Condensed Black.ttf",18)
octosquares1 = pygame.font.Font(absolute_path + r"\assets\game_font\TT Octosquares Trial Condensed Black.ttf",70)
octosquares2 = pygame.font.Font(absolute_path + r"\assets\game_font\TT Octosquares Trial Black.ttf",30)
octosquares3 = pygame.font.Font(absolute_path + r"\assets\game_font\TT Octosquares Trial Black.ttf",15)
octosquares4 = pygame.font.Font(absolute_path + r'\assets\game_font\TT Octosquares Trial Black.ttf',22)
pixeldub_1 = pygame.font.Font(absolute_path + r"\assets\game_font\pixeldub.ttf",66)
button_text1 = pygame.font.Font(absolute_path + r"\assets\game_font\pixeldub.ttf",100)
EType_1 = pygame.font.Font(absolute_path + r'\assets\game_font\ELEGANT TYPEWRITER Bold.ttf',30)
EType_2 = pygame.font.Font(absolute_path + r'\assets\game_font\ELEGANT TYPEWRITER Bold.ttf',20)
EType_3 = pygame.font.Font(absolute_path + r'\assets\game_font\ELEGANT TYPEWRITER Bold.ttf',18)

#DECLARING GAME-RELATED VARIABLES:
new_press = True
active_map = 1
l2_run,l3_run,l4_run,l5_run,l6_1_run,l6_2_run = False,False,False,False,False,False
user_text = ''
active_frequency = 0.0


wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,True
wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
battery_stack = [1,1]
battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':True}
battery_max = 6
oxygen_meter = 4
check_batteryReset = [False] #1. map2-map3
battery_reset_event = False
oxygen_reset_event = False
battery_change_after_event = False
picture_authorized = False
player_maxSpeed,player_maxRotationSpeed = 2.5,0.03

indicator_dict = {'mainD':True,'mainA':True,'mainS':True,'tabletW':True,'tabletA':True,'mapW':True,'mapD':True,'noticeD':True,'NOTICE_ESCAPE':True,'cameraA':True,'cameraButton':True,'scannerButton':True,'SONAR_ESCAPE':True,'LOGS_ESCAPE':True,'sonarLMB':True,'noticeboardLMB':True}
COD_dict = {'crash':False,'ls':False,'fin':False}
scan_rect = 0
outside_fadeFlag = False
endEvent_dict = {'monstercrash':'_','monstercrash_event':False,'photo_taken':False}
#DECLARING MOVEMENT-SPECIFIC VARIABLES:
first_run = True
GAME_OVER = False
player_starting_x,player_starting_y = 0,0
player_x,player_y = 0,0
player_xDisplay,player_yDisplay,player_zDisplay= 300,300,92
player_xDisplay_mod,player_yDisplay_mod = round(player_xDisplay,2),round(player_yDisplay,2)
last_xPos,last_yPos,x_Update,y_Update = 0,0,0,0
check_collision = False

#SOUND EFFECTS / MUSIC:
#Channels:

bg_audio = pygame.mixer.Channel(1)
bg_audio2 = pygame.mixer.Channel(2)
additionals1 = pygame.mixer.Channel(3)
additionals2 = pygame.mixer.Channel(4)
additionals3 = pygame.mixer.Channel(5)
bg_audio.set_volume(0.2)

#Sounds:
rv_ambiance = pygame.mixer.Sound(absolute_path + r'\assets\audio\rover_ambiance.wav')
lab_ambience = pygame.mixer.Sound(absolute_path + r'\assets\audio\lab_ambience.wav')
rv_moving = pygame.mixer.Sound(absolute_path + r'\assets\audio\rover_moving.wav')
rv_crash = pygame.mixer.Sound(absolute_path + r'\assets\audio\impact_crash.wav')
fall_crash = pygame.mixer.Sound(absolute_path + r'\assets\audio\fall_crash.wav')
fall_crash.set_volume(0.3)
impact_crash = pygame.mixer.Sound(absolute_path + r'\assets\audio\rover_crash.wav')
rv_crash.set_volume(0.55)
running = pygame.mixer.Sound(absolute_path + r'\assets\audio\runningindistance.wav')
ts_wind = pygame.mixer.Sound(absolute_path + r'\assets\audio\title_screen_wind.wav')
ts_gc = pygame.mixer.Sound(absolute_path + r'\assets\audio\title_screen_geiger_counter.wav')
ts_gc.set_volume(0.6)
button1 = pygame.mixer.Sound(absolute_path + r'\assets\audio\button1.wav')
button2 = pygame.mixer.Sound(absolute_path + r'\assets\audio\button2.wav')
button3 = pygame.mixer.Sound(absolute_path + r'\assets\audio\button3.wav')
button1.set_volume(0.2)
button2.set_volume(0.2)
button3.set_volume(0.2)
camera_shutter = pygame.mixer.Sound(absolute_path + r'\assets\audio\camera_shutter.wav')
log_notif = pygame.mixer.Sound(absolute_path + r'\assets\audio\log_notif.wav')
paper_shuffle = pygame.mixer.Sound(absolute_path + r'\assets\audio\paper_shuffle.wav')
ending_fade = pygame.mixer.Sound(absolute_path + r'\assets\audio\ending_fade.wav')
ending_hardhit = pygame.mixer.Sound(absolute_path + r'\assets\audio\ending_hardhit.wav')
warning_alert = pygame.mixer.Sound(absolute_path + r'\assets\audio\warning_alert.wav')
warning_alert.set_volume(0.5)
oxygen_alert = pygame.mixer.Sound(absolute_path + r'\assets\audio\oxygen_alert.wav')
monster_breathing = pygame.mixer.Sound(absolute_path + r'\assets\audio\monster_breathing.wav')
monster_breathing.set_volume(0.7)

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
    def __init__(self, x_pos, y_pos,width,height,b_xpos,b_ypos,b_width, b_height, b_surface, opacity,enabled, text = '',text_xoffset = 10,text_yoffset = 10,text_colour = 'white',text_font = 'pixeldub'):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.b_xpos = b_xpos
        self.b_ypos = b_ypos
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
        global picture_authorized
        #authorization rect:
        if self.enabled:
            if picture_authorized:
                pygame.draw.rect(self.b_surface,(0,255,0,90),(self.b_xpos,self.b_ypos,self.b_width,self.b_height)) if lights_check_status else pygame.draw.rect(self.b_surface,(0,255,0,40),(self.b_xpos,self.b_ypos,self.b_width,self.b_height))
            else:
                pygame.draw.rect(self.b_surface,(255,0,0,90),(self.b_xpos,self.b_ypos,self.b_width,self.b_height)) if lights_check_status else pygame.draw.rect(self.b_surface,(255,0,0,40),(self.b_xpos,self.b_ypos,self.b_width,self.b_height))
        else:
            pygame.draw.rect(self.b_surface,(255,0,0,0),(self.b_xpos,self.b_ypos,self.b_width,self.b_height))
        #button rect:
        pygame.draw.rect(self.b_surface,(255,0,0,self.opacity),(self.x_pos,self.y_pos,self.width,self.height))
        invbutton_text = octosquares1.render('{0}'.format(self.text),True,'{0}'.format(self.text_colour))
        self.b_surface.blit(invbutton_text,(self.x_pos + self.text_xoffset,self.y_pos + self.text_yoffset))

    def camcheck_Click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos,self.y_pos),(self.width,self.height))
        if self.enabled and left_click and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

class logButton:
    def __init__(self,enabled, buttonType):
        self.enabled = enabled
        self.buttonType = buttonType
        self.x_pos,self.y_pos,self.b_surface,self.text,self.text_xoffset,self.text_yoffset,self.text_colour,self.text_font = -60,-60,0,0,0,0,0,0
    
    def create(self, x_pos, y_pos, b_surface,text = '',text_xoffset = 10,text_yoffset = 10,text_colour = 'white',text_font = 'pixeldub'):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.b_surface = b_surface
        self.text = text
        self.text_xoffset = text_xoffset
        self.text_yoffset = text_yoffset
        self.text_colour = text_colour
        self.text_font = text_font
        self.draw()
        
    def draw(self):
        if self.enabled:
            if self.buttonType == 'SCAN':
                self.b_surface.blit(log_scanButton,(self.x_pos,self.y_pos))
            
            elif self.buttonType == 'DATA':
                self.b_surface.blit(log_dataButton,(self.x_pos,self.y_pos))

            if self.text_font == 'pixeldub':
                invbutton_text = pixeldub_1.render('{0}'.format(self.text),True,'{0}'.format(self.text_colour))
                self.b_surface.blit(invbutton_text,(self.x_pos + self.text_xoffset,self.y_pos + self.text_yoffset))
            elif self.text_font == 'octosquares':
                invbutton_text = octosquares4.render('{0}'.format(self.text),True,'{0}'.format(self.text_colour))
                self.b_surface.blit(invbutton_text,(self.x_pos + self.text_xoffset,self.y_pos + self.text_yoffset))

    def invcheck_Click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos,self.y_pos),(300,50))
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
        if self.text == 'LMB':
            new_indicator = pygame.transform.rotate(indicator_pic,self.angle)
            screen.blit(new_indicator,(self.x_pos,self.y_pos))
            screen.blit(LMB_indicator_pic,(self.x_pos + self.x_offset,self.y_pos + self.y_offset))
        elif self.text[0] == ';':
            indicator_text = octosquares2.render(self.text[1:],True,'dark gray')
            screen.blit(indicator_text,(self.x_pos,self.y_pos))
        else:
            new_indicator = pygame.transform.rotate(indicator_pic,self.angle)
            screen.blit(new_indicator,(self.x_pos,self.y_pos))
            indicator_Text = base_text1.render(self.text,True,'black')
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

class Timer:
    def __init__(self,duration):
        self.duration = duration
        self.start_time = 0
        self.current_time = 0
        self.active = False
        self.timeout = False
    
    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0


    def update(self):
        if self.active:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.start_time >= self.duration:
                self.active = False
                self.start_time = 0
                self.timeout = True

class Notification:
    def __init__(self):
        self.duration = 0
        self.start_time = 0
        self.current_time = 0
        self.active = False
        self.timeout = False
        self.type = 0
    
    def activate(self,type,current_scan = 0):
        global SCAN_DICT
        if type == 'SCAN':
            if current_scan != 0:
                if not SCAN_DICT[current_scan]:
                    self.active = True
                    additionals2.play(log_notif)
                    self.start_time = pygame.time.get_ticks()
                    self.type = type
                    self.duration = 3500
        elif type == 'IMPACT':
            self.active = True
            self.start_time = pygame.time.get_ticks()
            self.type = type
            self.duration = 2500

    def deactivate(self):
        self.active = False
        self.start_time = 0
        self.type = 0
        self.duration = 0


    def update(self):
        if self.active:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.start_time >= self.duration:
                self.active = False
                self.start_time = 0
                self.timeout = True

class POI_Marker:
    def __init__(self,x_pos,y_pos,active,enabled):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.active = active
        self.enabled = enabled
        self.draw()

    def draw(self):
        global lights_check_status
        if self.enabled:
            if self.active:
                screen.blit(poi_marker,(self.x_pos,self.y_pos))
            else:
                screen.blit(poi_marker_done,(self.x_pos,self.y_pos))
    
    def hover_event(self):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.rect.Rect((self.x_pos-2,self.y_pos-2),(34,34))
        if self.enabled and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False


fadeScreen = fadeObject(10)
titleFade = fadeObject(20)
titleFade.fade_flag = True
ls_timer = Timer(7000)
cavefall_timer = Timer(7000)
main_Notif = Notification()


#MOVEMENT-RELATED CLASSES:
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,x,y):
        global player_x,player_y,player_maxSpeed,player_maxRotationSpeed
        super().__init__(groups)
        self.image = pygame.image.load(absolute_path + r'\assets\images\extras\player_arrow.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48,48))
        self.rect = self.image.get_rect(center = (player_xDisplay + self.image.get_width() // 2, player_yDisplay + self.image.get_height() // 2))
        
        player_x,player_y,self.player_angle,self.player_velocity = x,y,0,[0,0]
        self.max_speed,self.max_rotationSpeed,self.current_speed,self.current_rotationSpeed = player_maxSpeed,player_maxRotationSpeed,0,0
        self.move_forward,self.move_forwardPressed,self.move_backward,self.move_backwardPressed = False,False,False,False


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load(absolute_path + r'\assets\images\extras\obstacle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(48,48))
        self.rect = self.image.get_rect(topleft = pos)


class Level1:
    def __init__(self):
        global active_map
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
        for row_index,row in enumerate(WORLD_MAP1):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col in('x','3','5'):
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

    def remove(self,cords):
        global player_xDisplay,player_yDisplay
        player_xDisplay,player_yDisplay = cords[0],cords[1]
        for sprite1 in self.visible_sprites:
            sprite1.kill()
        for sprite2 in self.obstacles_sprites:
            sprite2.kill()
        self.visible_sprites.empty()
        self.obstacles_sprites.empty()

class Level2:
    def __init__(self):
        #get the display surface
        self.display_surface = pygame.surface.Surface((1200,600))
    
    def sprite_initialize(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = YSortCameraGroup()
        self.create_map()

    def create_map(self):
        global player_starting_x,player_starting_y,player_xDisplay,player_yDisplay
        player_check = False
        for row_index,row in enumerate(WORLD_MAP2):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col in('x','3','5'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites])
                if col == 'p1':
                    player_check = True
                    player_starting_x,player_starting_y = x,y
                    
        if player_check:
            self.player = Player((player_starting_x,player_starting_y),[self.visible_sprites],self.obstacles_sprites,player_starting_x,player_starting_y)
            player_xDisplay,player_yDisplay = player_starting_x,player_starting_y
            
    def run(self):
        global first_run
        #update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
    
    def remove(self,cords):
            global player_xDisplay,player_yDisplay
            player_xDisplay,player_yDisplay = cords[0],cords[1]
            for sprite1 in self.visible_sprites:
                sprite1.kill()
            for sprite2 in self.obstacles_sprites:
                sprite2.kill()
            self.visible_sprites.empty()
            self.obstacles_sprites.empty()

class Level3:
    def __init__(self):
        #get the display surface
        self.display_surface = pygame.surface.Surface((1200,600))
    
    def sprite_initialize(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = YSortCameraGroup()
        self.create_map()

    def create_map(self):
        global player_starting_x,player_starting_y,player_xDisplay,player_yDisplay
        player_check = False
        for row_index,row in enumerate(WORLD_MAP3):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col in('x','3','5'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites])
                if col == 'p1':
                    player_check = True
                    player_starting_x,player_starting_y = x,y
                    
        if player_check:
            self.player = Player((player_starting_x,player_starting_y),[self.visible_sprites],self.obstacles_sprites,player_starting_x,player_starting_y)
            player_xDisplay,player_yDisplay = player_starting_x,player_starting_y
            
    def run(self):
        global first_run
        #update and draw the game

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
    
    def remove(self,cords):
            global player_xDisplay,player_yDisplay
            player_xDisplay,player_yDisplay = cords[0],cords[1]
            for sprite1 in self.visible_sprites:
                sprite1.kill()
            for sprite2 in self.obstacles_sprites:
                sprite2.kill()
            self.visible_sprites.empty()
            self.obstacles_sprites.empty()

class Level4:
    def __init__(self):
        #get the display surface
        self.display_surface = pygame.surface.Surface((1200,600))
    
    def sprite_initialize(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = YSortCameraGroup()
        self.create_map()

    def create_map(self):
        global player_starting_x,player_starting_y,player_xDisplay,player_yDisplay
        player_check = False
        for row_index,row in enumerate(WORLD_MAP4):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col in('x','3','5'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites])
                if col == 'p1':
                    player_check = True
                    player_starting_x,player_starting_y = x,y
                    
        if player_check:
            self.player = Player((player_starting_x,player_starting_y),[self.visible_sprites],self.obstacles_sprites,player_starting_x,player_starting_y)
            player_xDisplay,player_yDisplay = player_starting_x,player_starting_y
            
    def run(self):
        global first_run
        #update and draw the game

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
    
    def remove(self,cords):
            global player_xDisplay,player_yDisplay
            player_xDisplay,player_yDisplay = cords[0],cords[1]
            for sprite1 in self.visible_sprites:
                sprite1.kill()
            for sprite2 in self.obstacles_sprites:
                sprite2.kill()
            self.visible_sprites.empty()
            self.obstacles_sprites.empty()

class Level5:
    def __init__(self):
        #get the display surface
        self.display_surface = pygame.surface.Surface((1200,600))
    
    def sprite_initialize(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = YSortCameraGroup()
        self.create_map()

    def create_map(self):
        global player_starting_x,player_starting_y,player_xDisplay,player_yDisplay
        player_check = False
        for row_index,row in enumerate(WORLD_MAP5):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col in('x','3','5'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites])
                if col == 'p1':
                    player_check = True
                    player_starting_x,player_starting_y = x,y
                    
        if player_check:
            self.player = Player((player_starting_x,player_starting_y),[self.visible_sprites],self.obstacles_sprites,player_starting_x,player_starting_y)
            player_xDisplay,player_yDisplay = player_starting_x,player_starting_y
            
    def run(self):
        global first_run
        #update and draw the game

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
    
    def remove(self,cords):
            global player_xDisplay,player_yDisplay
            player_xDisplay,player_yDisplay = cords[0],cords[1]
            for sprite1 in self.visible_sprites:
                sprite1.kill()
            for sprite2 in self.obstacles_sprites:
                sprite2.kill()
            self.visible_sprites.empty()
            self.obstacles_sprites.empty()

class Level6_1:
    def __init__(self):
        #get the display surface
        self.display_surface = pygame.surface.Surface((1200,600))
    
    def sprite_initialize(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = YSortCameraGroup()
        self.create_map()

    def create_map(self):
        global player_starting_x,player_starting_y,player_xDisplay,player_yDisplay
        player_check = False
        for row_index,row in enumerate(WORLD_MAP61):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col in('x','3','5','7','8'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites])
                if col == 'p1':
                    player_check = True
                    player_starting_x,player_starting_y = x,y
                    
        if player_check:
            self.player = Player((player_starting_x,player_starting_y),[self.visible_sprites],self.obstacles_sprites,player_starting_x,player_starting_y)
            player_xDisplay,player_yDisplay = player_starting_x,player_starting_y
            
    def run(self):
        global first_run
        #update and draw the game

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
    
    def remove(self,cords):
            global player_xDisplay,player_yDisplay
            player_xDisplay,player_yDisplay = cords[0],cords[1]
            for sprite1 in self.visible_sprites:
                sprite1.kill()
            for sprite2 in self.obstacles_sprites:
                sprite2.kill()
            self.visible_sprites.empty()
            self.obstacles_sprites.empty()

class Level6_2:
    def __init__(self):
        #get the display surface
        self.display_surface = pygame.surface.Surface((1200,600))
    
    def sprite_initialize(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = YSortCameraGroup()
        self.create_map()

    def create_map(self):
        global player_starting_x,player_starting_y,player_xDisplay,player_yDisplay
        player_check = False
        for row_index,row in enumerate(WORLD_MAP62):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col in('x','3','5'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites])
                if col == 'p1':
                    player_check = True
                    player_starting_x,player_starting_y = x,y
                    
        if player_check:
            self.player = Player((player_starting_x,player_starting_y),[self.visible_sprites],self.obstacles_sprites,player_starting_x,player_starting_y)
            player_xDisplay,player_yDisplay = player_starting_x,player_starting_y
            
    def run(self):
        global first_run
        #update and draw the game

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
    
    def remove(self,cords):
            global player_xDisplay,player_yDisplay
            player_xDisplay,player_yDisplay = cords[0],cords[1]
            for sprite1 in self.visible_sprites:
                sprite1.kill()
            for sprite2 in self.obstacles_sprites:
                sprite2.kill()
            self.visible_sprites.empty()
            self.obstacles_sprites.empty()

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


level1 = Level1()
level2 = Level2()
level3 = Level3()
level4 = Level4()
level5 = Level5()
level6_1 = Level6_1()
level6_2 = Level6_2()

#FUNCTIONS TO RUN THE GAME (SCREENS):
def main_gameLoop():
    #GAME SCREENS:
    def title_screen(): 
        global new_press
        if bg_audio.get_busy():
            pass
        else:
            bg_audio.play(ts_wind,-1,0,3000)
            additionals2.play(ts_gc,-1,0,2500)
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
                    ts_gc.fadeout(700)
                    fadeScreen.fadeIn()
                    if fadeScreen.fade_flag:
                        backstory()

                if quit_button.invcheck_Click():
                    ts_wind.fadeout(2000)
                    ts_gc.fadeout(2000)
                    fadeScreen.fadeIn()
                    bg_audio.stop()
                    additionals2.stop()
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

        if fadeScreen.fade_flag:
            fade_run = True
            alpha = 180
            while fade_run:
                screen.blit(backstory_bg,backstory_bg_rect)
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
            screen.blit(backstory_bg,backstory_bg_rect)
            screen.blit(backstory_surface,(0,0))

            continue_button = Button('Continue',480,540,60,True)

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if continue_button.check_click():
                    ts_wind.fadeout(2000)
                    fadeScreen.fadeIn()
                    if fadeScreen.fade_flag:
                        additionals2.stop()
                        bg_audio.stop()
                        bg_audio.play(rv_ambiance,-1,0,10000)
                        main_view()
            
            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    backstory_var = False

            pygame.display.update()
        pygame.quit()

    def main_view():
        global new_press, fade_img, oxygen_meter, battery_reset_event,wheels_check_status,sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled,battery_stack,battery_dict,check_batteryReset,battery_max     

        if fadeScreen.fade_flag:
            fade_run = True
            alpha = 180
            while fade_run:
                if lights_check_status:
                    screen.blit(main_view_bg,main_view_bg_rect)
                    if oxygen_meter == 4:
                        screen.blit(OM4,(550,200))
                    else:
                        screen.blit(OM1,(550,200))
                else:
                    screen.blit(main_view_bg_LO,main_view_bg_rect)
                    screen.blit(OM1_LO,(550,200))
                fade_img.set_alpha(alpha)
                screen.blit(fade_img,(0,0))
                pygame.display.update()
                pygame.time.delay(fadeScreen.time_delay)
                alpha -= 2
                if alpha == 0:
                    fade_run = False
            fadeScreen.fade_flag = False

        if bg_audio.get_busy():
            pass
        else:
            bg_audio.play(rv_ambiance,-1,0,2000)

        if active_map in (6,7):
            if bg_audio2.get_busy():
                pass
            else:
                pass
                bg_audio2.play(lab_ambience,-1,0,2000)

        main_view_var = True
        while main_view_var:
            if battery_reset_event:
                wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
                battery_stack = [1]
                battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
                battery_reset_event = False

            if check_batteryReset[0]:
                check_batteryReset[0] = False
                battery_max = 4
                battery_reset_event = True
            

            timer.tick(fps)
            if lights_check_status:
                screen.blit(main_view_bg,main_view_bg_rect)
            else:
                screen.blit(main_view_bg_LO,main_view_bg_rect)
            
            if lights_check_status:
                if ls_timer.active:
                    screen.blit(OM0,(550,200))
                else:
                    if oxygen_meter == 4:
                        screen.blit(OM4,(550,200))
                    elif oxygen_meter == 3:
                        screen.blit(OM3,(550,200))
                    elif oxygen_meter == 2:
                        screen.blit(OM2,(550,200))
                    elif oxygen_meter == 1:
                        screen.blit(OM1,(550,200))
            else:
                if ls_timer.active:
                    screen.blit(OM0_LO,(550,200))
                else:
                    if oxygen_meter == 4:
                        screen.blit(OM4_LO,(550,200))
                    elif oxygen_meter == 3:
                        screen.blit(OM3_LO,(550,200))
                    elif oxygen_meter == 2:
                        screen.blit(OM2_LO,(550,200))
                    elif oxygen_meter == 1:
                        screen.blit(OM1_LO,(550,200))
                
            main_view_d_indicator = Indicator('D',1120,250,15,11,90,indicator_dict['mainD'])
            main_view_a_indicator = Indicator('A',30,250,21,11,270,indicator_dict['mainA'])
            main_view_s_indicator = Indicator('S',763,329,19,9,0,indicator_dict['mainS'])

            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()
            
            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

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
        global new_press,battery_reset_event,wheels_check_status,sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled,battery_stack,battery_dict,POI_DICT

        poi_hover = False
        map_view_var = True
        while map_view_var:
            if battery_reset_event:
                wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
                battery_stack = [1]
                battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
                battery_reset_event = False

            timer.tick(fps)
            if lights_check_status:
                screen.blit(map_view_bg,map_view_bg_rect)
            else:
                screen.blit(map_view_bg_LO,map_view_bg_rect)
            screen.blit(map_view_surface,(0,0))

            poi1 = POI_Marker(255,100,POI_DICT['1'],lights_check_status)
            poi2 = POI_Marker(224,136,POI_DICT['2'],lights_check_status)
            poi3 = POI_Marker(326,138,POI_DICT['3'],lights_check_status)
            poi4 = POI_Marker(302,195,POI_DICT['4'],lights_check_status)
            poi5 = POI_Marker(340,249,POI_DICT['5'],lights_check_status)
            poi6 = POI_Marker(364,279,POI_DICT['6'],lights_check_status)
            poi7 = POI_Marker(476,215,POI_DICT['7'],lights_check_status)
            poi8 = POI_Marker(446,280,POI_DICT['8'],lights_check_status)
            poi9 = POI_Marker(606,260,POI_DICT['9'],lights_check_status)
            poi10 = POI_Marker(564,300,POI_DICT['10'],lights_check_status)
            poi11 = POI_Marker(500,450,True,lights_check_status)
            poi12 = POI_Marker(745,345,True,lights_check_status)
            poi13 = POI_Marker(875,480,True,lights_check_status)
            poi14 = POI_Marker(596,100,True,lights_check_status)
            poi15 = POI_Marker(913,185,True,lights_check_status)
            poi16 = POI_Marker(986,378,True,lights_check_status)

            map_d_indicator = Indicator('D',1130,250,15,11,90,indicator_dict['mapD'])
            map_w_indicator = Indicator('W',553,10,16,14,180,indicator_dict['mapW'])

            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()
            
            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

            if poi1.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 1,920m','Y = 930m','z = 92m',poi1.x_pos,poi1.y_pos
                poi_hover = True
            elif poi2.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 1,680m','Y = 1,680m','z = 96m',poi2.x_pos,poi2.y_pos
                poi_hover = True
            elif poi3.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 2,930m','Y = 1,745m','z = 108m',poi3.x_pos,poi3.y_pos
                poi_hover = True
            elif poi4.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 2,750m','Y = 3,050m','z = 110m',poi4.x_pos,poi4.y_pos
                poi_hover = True
            elif poi5.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 3,150m','Y = 4,611m','z = 124m',poi5.x_pos,poi5.y_pos
                poi_hover = True
            elif poi6.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 3,550m','Y = 5,175m','z = 131m',poi6.x_pos,poi6.y_pos
                poi_hover = True
            elif poi7.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 5,250m','Y = 3,750m','z = 151m',poi7.x_pos,poi7.y_pos
                poi_hover = True
            elif poi8.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 4,650m','Y = 5,115m','z = 168m',poi8.x_pos,poi8.y_pos
                poi_hover = True
            elif poi9.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 7,150m','Y = 4,850m','z = 193m',poi9.x_pos,poi9.y_pos
                poi_hover = True
            elif poi10.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 6,450m','Y = 5,775m','z = 208m',poi10.x_pos,poi10.y_pos
                poi_hover = True
            elif poi11.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 5,525m','Y = 9,500m','z = 215m',poi11.x_pos,poi11.y_pos
                poi_hover = True
            elif poi12.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 9,125m','Y = 6,975m','z = 259m',poi12.x_pos,poi12.y_pos
                poi_hover = True
            elif poi13.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 11,100m','Y = 10,500m','z = 232m',poi13.x_pos,poi13.y_pos
                poi_hover = True
            elif poi14.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 6,975m','Y = 950m','z = 184m',poi14.x_pos,poi14.y_pos
                poi_hover = True
            elif poi15.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 11,675m','Y = 2,915m','z = 167m',poi15.x_pos,poi15.y_pos
                poi_hover = True
            elif poi16.hover_event():
                textx,texty,textz,poiX,poiY = 'X = 12,700m','Y = 7,850m','z = 108m',poi16.x_pos,poi16.y_pos
                poi_hover = True
            else:
                poi_hover = False

            if poi_hover:
                hover_text1 = EType_3.render('{0}'.format(textx),True,'white')
                hover_text2 = EType_3.render('{0}'.format(texty),True,'white')
                hover_text3 = EType_3.render('{0}'.format(textz),True,'white')
                screen.blit(hover_text1,(poiX + 40,poiY - 20))
                screen.blit(hover_text2,(poiX + 40,poiY))
                screen.blit(hover_text3,(poiX + 40,poiY + 20))

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
        global new_press, battery_max, oxygen_meter,picture_authorized,POI_DICT,POI_LIST,player_xDisplay,player_yDisplay,player_xDisplay_mod,player_yDisplay_mod,battery_reset_event,wheels_check_status,sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled,battery_stack,battery_dict,active_map,player_maxSpeed,player_maxRotationSpeed,check_batteryReset,battery_change_after_event,COD_dict

        end_count = 0
        pic_var = 0
        pic_load_var = False
        camera_var = True
        map_change = 0 #change to 'x'
        animation_change_flag = False
        while camera_var:
            if battery_reset_event:
                wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
                battery_stack = [1]
                battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
                battery_reset_event = False

            timer.tick(fps)
            if lights_check_status:
                empty.set_alpha(255)
                screen.blit(camera_bg,camera_bg_rect)
            else:
                empty.set_alpha(90)
                camera_surface.blit(empty,(320,84))
                screen.blit(camera_bg_LO,camera_bg_rect)
            screen.blit(camera_surface,(0,0))

            camera_button = camButton(316,500,408,64,791,503,62,62,camera_surface,0,camera_check_status,'',37,-16,'gray')
            scanner_button = camButton(960,156,232,40,1036,212,84,87,camera_surface,0,scanner_check_status,'',10,10,'gray')

            camera_a_indicator = Indicator('A',10,250,21,11,270,indicator_dict['cameraA'])
            camera_button_indicator = Indicator(';CAMERA',436,511,0,0,0,indicator_dict['cameraButton'])
            sonar_button_indicator = Indicator(';SCANNER',985,154,0,0,0,indicator_dict['scannerButton'])


            current_poi = 0
            for cords in POI_LIST:
                if (cords[1][0] <= player_xDisplay_mod  <= cords[1][1]) and (cords[2][0] <= player_yDisplay_mod <= cords[2][1]) and cords[3] == str(active_map) and picture_authorized:
                    current_poi = cords[0]
            
            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if camera_button.camcheck_Click():
                    indicator_dict['cameraButton'] = False
                    #level change features:
                    if current_poi != 0:
                        POI_DICT[current_poi] = False
                        if POI_DICT['2'] == False and active_map == 1:
                            map_change = 2
                        if POI_DICT['4'] == False and active_map == 2:
                            map_change = 3
                    
                    #confirming picture:
                    if picture_authorized and current_poi != 0:
                        pic_load_var = True
                        additionals1.play(camera_shutter)

                    if endEvent_dict['monstercrash_event']:
                        endEvent_dict['photo_taken'] = True

                if scanner_button.camcheck_Click():
                    indicator_dict['scannerButton'] = False
                    if current_poi not in (0,'11'):
                        additionals2.play(log_notif)
                        DATASCAN_DICT[current_poi] = True
                        
            
            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()

            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

            #picture blitting
            if pic_load_var:
                if pic_var != 168:
                    pic_var += 2

            if pic_var == 168:
                if current_poi == '1':
                    camera_surface.blit(grove,(320,84))
                elif current_poi == '2':
                    camera_surface.blit(spirals,(320,84))
                elif current_poi == '3':
                    camera_surface.blit(metal_plate,(320,84))
                elif current_poi == '4':
                    camera_surface.blit(skeletons,(320,84))
                elif current_poi == '5':
                    camera_surface.blit(campsite1,(320,84))
                elif current_poi == '6':
                    camera_surface.blit(landscape1,(320,84))
                elif current_poi == '7':
                    camera_surface.blit(rover,(320,84))
                elif current_poi == '8':
                    camera_surface.blit(dead_researcher,(320,84))
                elif current_poi == '9':
                    camera_surface.blit(campsite2,(320,84))
                elif current_poi == '10':
                    camera_surface.blit(landscape2,(320,84))
                elif current_poi == '11':
                    camera_surface.blit(facility_entrance,(320,84))
                elif current_poi == '12':
                    if not lights_check_status:
                        facility_monster.set_alpha(200)
                    camera_surface.blit(facility_monster,(320,84))
                    rv_ambiance.fadeout(2000)
            else:
                camera_surface.blit(empty,(320,84))

            loading_rect = pygame.rect.Rect((724,410-(pic_var*2 if pic_var != 168 else 167)),(176,10+(pic_var*2 if pic_var != 168 else 167)))#as the height decreases, y position increases 76,344
            if lights_check_status:
                pygame.draw.rect(camera_surface,(3,252,169,120),loading_rect)
            else:
                pygame.draw.rect(camera_surface,(3,252,169,20),loading_rect)

            if pic_var == 0:
                camera_surface.blit(load_darken,(724,76))

            if end_count == 120 and lights_check_status:
                lights_check_status = False
                pygame.draw.rect(camera_surface,(3,252,160,20),(724,76,176,344))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a) and pic_var in (0,168):
                        indicator_dict['cameraA'] = False
                        if map_change == 2:
                            active_map = 2
                            player_maxSpeed,player_maxRotationSpeed = 2.8,0.033
                            level1.remove((player_xDisplay_mod,player_yDisplay_mod))
                            map_change = 0
                        elif map_change == 3:
                            active_map = 3
                            level2.remove((player_xDisplay_mod,player_yDisplay_mod))
                            map_change = 0
                        if not endEvent_dict['photo_taken']:
                            main_view()
                        else:
                            animation_end()

                if event.type == pygame.QUIT:
                    camera_var = False

            if endEvent_dict['photo_taken']:
                    end_count += 1
            pygame.display.update()
        pygame.quit()

    def welcome_screen():
        global new_press,battery_reset_event,wheels_check_status,sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled,battery_stack,battery_dict
        
        play_run = True
        while play_run:
            if battery_reset_event:
                wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
                battery_stack = [1]
                battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
                battery_reset_event = False

            timer.tick(fps)
            if lights_check_status:
                screen.blit(play_bg,play_bg_rect)
            else:
                screen.blit(play_bg_LO,play_bg_rect)
            screen.blit(play_surface,(0,0))

            sonar_button = invButton(168,95,273,74,play_surface,0,True,'SONAR',21,8,'#01240b')
            power_button = invButton(463,95,273,74,play_surface,0,True,'POWER',20,8,'#01240b')
            pda_button = invButton(760,95,273,74,play_surface,0,True,'COMMS',16,8,'#01240b')

            tablet_a_indicator = Indicator('A',10,250,21,11,270,indicator_dict['tabletA'])
            tablet_w_indicator = Indicator('W',553,10,16,14,180,indicator_dict['tabletW'])

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if sonar_button.invcheck_Click():
                    additionals1.play(button2)
                    sonar_screen()
                elif power_button.invcheck_Click():
                    additionals1.play(button2)
                    power_screen()
                elif pda_button.invcheck_Click():
                    additionals1.play(button2)
                    pda_screen()

            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True
            
            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()
            
            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

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
        global new_press,battery_reset_event,wheels_check_status,sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled,battery_stack,battery_dict

        
        sonar_run = True
        while sonar_run:
            if battery_reset_event:
                wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
                battery_stack = [1]
                battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
                battery_reset_event = False

            timer.tick(fps)
            if lights_check_status:
                screen.blit(sonar_bg,sonar_bg_rect)
            else:
                screen.blit(sonar_bg_LO,sonar_bg_rect)
            screen.blit(sonar_surface,(0,0))

            sonar_LMB_indicator = Indicator('LMB',370,320,-4,1,90,indicator_dict['sonarLMB'])
            tablet_w_indicator = Indicator('W',553,10,16,14,180,indicator_dict['tabletW'])
            tablet_a_indicator = Indicator('A',10,250,21,11,270,indicator_dict['tabletA'])
            activate_sonar_button = invButton(439,192,324,314,sonar_surface,0,True)

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if power_button.invcheck_Click():
                    additionals1.play(button2)
                    power_screen()
                elif pda_button.invcheck_Click():
                    additionals1.play(button2)
                    pda_screen()
                elif activate_sonar_button.invcheck_Click():
                    indicator_dict['sonarLMB'] = False
                    additionals1.play(button3)
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

            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()

            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

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
        global GAME_OVER,player_x,player_y,first_run,player_xDisplay,player_yDisplay,player_xDisplay_mod,player_yDisplay_mod,player_starting_x,player_starting_y,check_collision,battery_max,POI_LIST,POI_DICT,picture_authorized,COD_dict,battery_reset_event,wheels_check_status,sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled,battery_stack,battery_dict,POI_DICT,POI_LIST,SCAN_DICT,SCAN_LIST,COD_dict,indicator_dict,active_map,l2_run,l3_run,l4_run,l5_run,l6_1_run,l6_2_run,last_xPos,last_yPos,x_Update,y_Update,player_maxSpeed,player_maxRotationSpeed,oxygen_meter,battery_max,endEvent_dict,oxygen_reset_event

        if first_run:
            player_xDisplay,player_yDisplay = player_starting_x,player_starting_y
        
        sonar_view_run = True
        screenshake = False
        screenshake_timer = 0
        render_offset = [0,0]
        fall_start = False
        ycords = -48
        while sonar_view_run:
            if battery_reset_event:
                wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
                battery_stack = [1]
                battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
                battery_reset_event = False
                level1.player.move_forward,level1.player.move_backward,level1.player.move_forwardPressed,level1.player.move_backwardPressed = False,False,False,False

            screen.fill('#2A0700')
            screen.blit(sonar_view_surface,(0,0))
            level1.player.max_speed = player_maxSpeed
            level1.player.max_rotationSpeed = player_maxRotationSpeed

            timer.tick(fps)
            if GAME_OVER:
                game_over_screen()
            
            if active_map == 1:
                level1.run()
            elif active_map == 2:
                if not l2_run:
                    level2.sprite_initialize()
                    l2_run = True  
                level2.run()
            elif active_map == 3:
                if not l3_run:
                    level3.sprite_initialize()
                    l3_run = True
                level3.run()
            elif active_map == 4:
                if not l4_run:
                    level4.sprite_initialize()
                    l4_run = True
                level4.run()
            elif active_map == 5:
                if not l5_run:
                    level5.sprite_initialize()
                    l5_run = True
                level5.run()
            elif active_map == 6:
                if not l6_1_run:
                    level6_1.sprite_initialize()
                    l6_1_run = True
                level6_1.run()
            elif active_map == 7:
                if not l6_2_run:
                    level6_2.sprite_initialize()
                    l6_2_run = True
                level6_2.run()

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        indicator_dict['SONAR_ESCAPE'] = False
                        level1.player.move_forward,level1.player.move_forwardPressed,level1.player.move_backward,level1.player.move_backwardPressed = False,False,False,False
                        sonar_view_run = False
                    
                    #retrieve forward-backward speed
                    elif event.key in (pygame.K_w,pygame.K_UP) and not level1.player.move_forwardPressed and wheels_check_status:
                        if not level1.player.move_backward:
                            level1.player.move_forward = not level1.player.move_forward
                            if level1.player.move_forward:
                                level1.player.current_speed = level1.player.max_speed
                            else:
                                level1.player.current_speed = 0
                        level1.player.move_forwardPressed = True
                    if event.key in (pygame.K_s,pygame.K_DOWN) and not level1.player.move_backwardPressed and wheels_check_status:
                        if not level1.player.move_forward:
                            level1.player.move_backward = not level1.player.move_backward
                            if level1.player.move_backward:
                                level1.player.current_speed = -level1.player.max_speed//4
                            else:
                                level1.player.current_speed = 0
                        level1.player.move_backwardPressed = True
                    
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_w,pygame.K_UP):
                        level1.player.move_forwardPressed = False
                    elif event.key in (pygame.K_s,pygame.K_DOWN):
                        level1.player.move_backwardPressed = False
            
            #retrieve rotation angle
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and wheels_check_status:
                if level1.player.current_rotationSpeed < level1.player.max_rotationSpeed:
                    level1.player.current_rotationSpeed += 0.02
                level1.player.player_angle += level1.player.current_rotationSpeed
            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and wheels_check_status:
                if level1.player.current_rotationSpeed < level1.player.max_rotationSpeed:
                    level1.player.current_rotationSpeed += 0.02
                level1.player.player_angle -= level1.player.current_rotationSpeed
            else:
                level1.player.current_rotationSpeed = max(0,level1.player.current_rotationSpeed -0.01)
            
            #adjust velocity based on rotation and movement speeds
            if level1.player.move_forward or level1.player.move_backward:
                level1.player.player_velocity[0] = -level1.player.current_speed * math.sin(level1.player.player_angle)
                level1.player.player_velocity[1] = -level1.player.current_speed * math.cos(level1.player.player_angle)
            else:
                level1.player.player_velocity[0],level1.player.player_velocity[1] = 0,0
            
            #update player positions
            level1.player.rect.centerx += level1.player.player_velocity[0]
            level1.player.rect.centery += level1.player.player_velocity[1]
            player_xDisplay += level1.player.player_velocity[0]
            player_yDisplay += level1.player.player_velocity[1]

            #rotate image based on angle and put in at the center
            rotated_playerArrow = pygame.transform.rotate(level1.player.image,math.degrees(level1.player.player_angle))
            rotated_playerArrow_rect = rotated_playerArrow.get_rect(center = (600,300))
            screen.blit(rotated_playerArrow,rotated_playerArrow_rect.topleft)

            player_xDisplay_mod = round(player_xDisplay,2)
            player_yDisplay_mod = round(player_yDisplay,2)
            last_x,last_y = player_xDisplay,player_yDisplay
            first_run = False

            if active_map == 1:
                player_xUpdate,player_yUpdate = 0,0
                level1.visible_sprites.custom_draw(level1.player)
            elif active_map == 2:
                player_xUpdate,player_yUpdate = 1056,1344
                level2.visible_sprites.custom_draw(level2.player)
            elif active_map == 3:
                player_xUpdate,player_yUpdate = 2352,3168
                level3.visible_sprites.custom_draw(level3.player)
            elif active_map == 4:
                player_xUpdate,player_yUpdate = 4032,3360
                level4.visible_sprites.custom_draw(level4.player)
            elif active_map == 5:
                player_xUpdate,player_yUpdate = 5088,4608
                level5.visible_sprites.custom_draw(level5.player)
            elif active_map == 6:
                player_xUpdate,player_yUpdate = -1,-1
                level6_1.visible_sprites.custom_draw(level6_1.player)
            elif active_map == 7:
                player_xUpdate,player_yUpdate = -1,-1
                level6_2.visible_sprites.custom_draw(level6_2.player)

            if active_map == 1:
                player_zDisplay = 92
            elif active_map == 2:
                player_zDisplay = 108
            elif active_map == 3:
                player_zDisplay = 124
            elif active_map == 4:
                player_zDisplay = 168
            elif active_map == 5:
                player_zDisplay = 208
            elif active_map in (6,7):
                player_zDisplay = '?'
            
            player_newx = round(last_x+player_xUpdate,2) if player_xUpdate != -1 else '?'
            player_newy = round(last_y+player_yUpdate,2) if player_yUpdate != -1 else '?'
            x_Cord = base_text1.render('X: {0}m'.format(player_newx),True,'white')
            y_Cord = base_text1.render('Y: {0}m'.format(player_newy),True,'white')
            z_Cord = base_text1.render('Z: {0}m [APPROX.]'.format(player_zDisplay),True,'white') if (active_map not in (6,7)) else base_text1.render('Z: {0}m'.format(player_zDisplay),True,'white')

            if not sonar_check_status:
                if screenshake:
                    if screenshake_timer == 15:
                        screen.blit(sonar_offline_bg,(0,0))
                        screenshake = False
                    else:
                        screen.fill('#170200')
                        render_offset[0],render_offset[1] = random.randint(0,64) - 32,random.randint(0,64) - 32
                        screen.blit(sonar_offline_bg,(render_offset[0],render_offset[1]))
                        screenshake_timer += 1
                else:
                    screen.blit(sonar_offline_bg,(0,0))
            else:
                if battery_max == 5:
                    screen.blit(noise5,(0,0))
                elif battery_max == 4:
                    screen.blit(noise4,(0,0))
                elif battery_max == 3:
                    if active_map in (6,7):
                        screen.blit(noise1,(0,0))
                    else:
                        screen.blit(noise3,(0,0))

                screen.blit(vignette,(0,0))
                
            
            if main_Notif.active:
                    if main_Notif.type == 'IMPACT':
                        main_Notif.current_time = pygame.time.get_ticks()
                        screen.blit(impact_Text_img,(415,415))
                        main_Notif.update()
                    elif main_Notif.type == 'SCAN':
                        main_Notif.current_time = pygame.time.get_ticks()
                        screen.blit(scan_checkText_img,(475,30))
                        main_Notif.update()

            screen.blit(x_Cord,(1000,50))
            screen.blit(y_Cord,(1000,80))
            screen.blit(z_Cord,(1000,110))
            sonar_view_esc_indicator = Indicator('ESC',10,10,13,12,270,indicator_dict['SONAR_ESCAPE'])
            
            #playing sfx of moving
            if additionals1.get_busy():
                if not (level1.player.move_forward or level1.player.move_backward):
                    additionals1.fadeout(300)
            else:
                if level1.player.move_forward:
                    rv_moving.set_volume(0.4)
                    additionals1.play(rv_moving,-1,0,300)
                elif level1.player.move_backward:
                    rv_moving.set_volume(0.2)
                    additionals1.play(rv_moving,0,0,300)
                else:
                    additionals1.pause()
                
            #checking for POIs:
            intersect_POI = False
            for cords in POI_LIST:
                if (cords[1][0] <= player_xDisplay_mod  <= cords[1][1]) and (cords[2][0] <= player_yDisplay_mod <= cords[2][1]) and cords[3] == str(active_map):
                    current_poi = cords[0]
                    intersect_POI = True
                    picture_authorized = True
                    current_poi = cords[0]

                    if current_poi == '2':
                        if not battery_change_after_event:
                            battery_max = 4
                            battery_reset_event = True
                if not intersect_POI:
                    picture_authorized = False
            
            #checking for scans:
            intersect_SCAN = False
            for cords in SCAN_LIST:
                if (cords[1][0] <= player_xDisplay_mod  <= cords[1][1]) and (cords[2][0] <= player_yDisplay_mod <= cords[2][1]) and cords[3] == str(active_map):
                    current_SCAN = cords[0]
                    if scanner_check_status:
                        intersect_SCAN = True
                        current_SCAN = cords[0]
                        main_Notif.activate('SCAN',current_SCAN)
                        SCAN_DICT[current_SCAN] = True
                    elif current_SCAN in ('7','8','11'):
                        intersect_SCAN = True
                        main_Notif.activate('SCAN',current_SCAN)
                        SCAN_DICT[current_SCAN] = True

            #checking for other events:
            for cords in EVENT_LIST:
                if (cords[1][0] <= player_xDisplay_mod  <= cords[1][1]) and (cords[2][0] <= player_yDisplay_mod <= cords[2][1]) and cords[3] == str(active_map):
                    current_eventCords = cords[0]
                    if current_eventCords == '1' and active_map == 2 and not EVENT_DICT['1']:
                        oxygen_meter = 3
                        oxygen_reset_event = True
                        battery_max = 5
                        battery_reset_event = True
                        EVENT_DICT[current_eventCords] = True
                        screenshake = True
                        main_Notif.activate('IMPACT')
                        additionals2.play(impact_crash)
                        additionals2.fadeout(3500)
                    if current_eventCords == '2' and active_map == 3 and (not(POI_DICT['5']) and not(POI_DICT['6'])):
                        battery_max = 4
                        active_map = 4
                        oxygen_meter = 2
                        oxygen_reset_event = True
                        battery_reset_event = True
                        check_batteryReset[0] = True
                        level3.remove((player_xDisplay_mod,player_yDisplay_mod))
                        screenshake = True
                        main_Notif.activate('IMPACT')
                        additionals2.play(impact_crash)
                    if current_eventCords == '3' and active_map == 4 and (not(POI_DICT['7']) and not(POI_DICT['8'])):
                        oxygen_meter = 2
                        battery_max = 3
                        battery_reset_event = True
                        EVENT_DICT[current_eventCords] = True
                        active_map = 5
                        level4.remove((player_xDisplay_mod,player_yDisplay_mod))
                        screenshake = True
                        main_Notif.activate('IMPACT')
                        additionals2.play(impact_crash)
                    if current_eventCords == '4' and active_map == 5 and (not(POI_DICT['9']) and not(POI_DICT['10'])):
                        EVENT_LIST.append(('fall', (1488, 1872), (1680, 2112), '5'))
                        EVENT_DICT['fall'] = False
                    if current_eventCords == 'fall' and active_map == 5:
                        oxygen_meter = 1
                        oxygen_reset_event = True
                        battery_max = 3
                        active_map = 6
                        battery_reset_event = True
                        EVENT_DICT[current_eventCords] = True
                        level5.remove((player_xDisplay_mod,player_yDisplay_mod))
                        fall_start = True
                        EVENT_LIST.remove(('fall', (1488, 1872), (1680, 2112), '5'))
                        EVENT_DICT.pop('fall')
                    if current_eventCords == '5' and active_map == 7:
                        if ycords > 240:
                            if additionals3.get_busy():
                                pass
                            else:
                                additionals3.play(monster_breathing,-1,0,2000)
                            battery_reset_event = True
                            wheels_check_enabled = False
                            sonar_check_enabled = False
                            EVENT_LIST.remove(('5', (48, 384), (1152, 1776), '7'))
                            EVENT_DICT.pop('5')
                            screenshake = True
                            main_Notif.activate('IMPACT')
                            additionals2.play(rv_crash)
                            endEvent_dict['monstercrash_event'] = True
                            POI_LIST.append(('12', (48, 384), (1152, 1872), '7'))
                            POI_DICT['12'] = False
                        else:
                            if ycords != 260:
                                screen.blit(monster_tile,(576,ycords))
                                ycords += 15
            if endEvent_dict['monstercrash'] == True:
                endEvent_dict['monstercrash'] = False
                EVENT_LIST.append(('5', (48, 384), (1152, 1776), '7'))
                EVENT_DICT['5'] = False
            

            #checking for collision:
            if check_collision:
                additionals1.stop()
                additionals2.stop()
                COD_dict['crash'] = True
                additionals2.play(rv_crash)
                game_over_screen()
            
            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()
            
            if fall_start == True:
                cavefall_timer.activate()
                fall_start = False

            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

            pygame.display.update()
                

    def power_screen():
        global new_press, wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled, battery_stack, battery_dict, battery_max, battery_reset_event, battery_change_after_event,endEvent_dict,oxygen_reset_event
        ls_start = False
        
        power_run = True
        while power_run:
            if battery_reset_event:
                wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
                battery_stack = [1]
                battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
                battery_reset_event = False

            if oxygen_reset_event:
                additionals3.play(oxygen_alert)
                oxygen_reset_event = False

            timer.tick(fps)
            if lights_check_status:
                screen.blit(power_bg,power_bg_rect)
            else:
                screen.blit(power_bg_LO,power_bg_rect)
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

            tablet_w_indicator = Indicator('W',553,10,16,14,180,indicator_dict['tabletW'])
            tablet_a_indicator = Indicator('A',10,250,21,11,270,indicator_dict['tabletA'])

            wheels_check = powerButtons('WHEELS',650,240,(wheels_check_enabled and not cavefall_timer.active and not endEvent_dict['monstercrash_event']),wheels_check_status,64)
            sonar_check = powerButtons('SONAR',650,280,(sonar_check_enabled and not cavefall_timer.active and (not endEvent_dict['monstercrash_event'])),sonar_check_status,68)
            ls_check = powerButtons('LIFE SUPPORT',650,320,ls_check_enabled,ls_check_status,38)
            camera_check = powerButtons('CAMERA',650,360,camera_check_enabled,camera_check_status,61)
            scanner_check = powerButtons('SCANNERS',650,400,scanner_check_enabled,scanner_check_status,54)
            lights_check = powerButtons('LIGHTS',650,440,lights_check_enabled,lights_check_status,66)

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if sonar_button.invcheck_Click():
                    additionals1.play(button2)
                    sonar_screen()
                elif pda_button.invcheck_Click():
                    additionals1.play(button2)
                    pda_screen()
                
                if wheels_check.textcheck_click():
                    if wheels_check_status == False and len(battery_stack) <= 6:
                        wheels_check_status = True
                        battery_stack.append(1)
                        battery_dict['wheels'] = True
                        battery_change_after_event = True
                        additionals1.play(button1)
                    else:
                        wheels_check_status = False
                        battery_stack.pop()
                        battery_dict['wheels'] = False
                        additionals1.play(button1)

                if sonar_check.textcheck_click():
                    if sonar_check_status == False and len(battery_stack) <= 6:
                        sonar_check_status = True
                        battery_stack.append(1)
                        battery_dict['sonar'] = True
                        battery_change_after_event = True
                        additionals1.play(button1)
                    else:
                        sonar_check_status = False
                        battery_stack.pop()
                        battery_dict['sonar'] = False
                        additionals1.play(button1)

                if ls_check.textcheck_click():
                    if ls_check_status == False and len(battery_stack) <= 6:
                        ls_timer.timeout = False
                        ls_timer.deactivate()
                        ls_start = False
                        ls_check_status = True
                        battery_stack.append(1)
                        battery_dict['ls'] = True
                        battery_change_after_event = True
                        additionals1.play(button1)
                    else:
                        ls_start = True
                        ls_check_status = False
                        battery_stack.pop()
                        battery_dict['ls'] = False
                        additionals1.play(button1)

                if camera_check.textcheck_click():
                    if camera_check_status == False and len(battery_stack) <= 6:
                        camera_check_status = True
                        battery_stack.append(1)
                        battery_dict['camera'] = True
                        battery_change_after_event = True
                        additionals1.play(button1)
                    else:
                        camera_check_status = False
                        battery_stack.pop()
                        battery_dict['camera'] = False
                        additionals1.play(button1)

                if scanner_check.textcheck_click():
                    if scanner_check_status == False and len(battery_stack) <= 6:
                        scanner_check_status = True
                        battery_stack.append(1)
                        battery_dict['scanner'] = True
                        battery_change_after_event = True
                        additionals1.play(button1)
                    else:
                        scanner_check_status = False
                        battery_stack.pop()
                        battery_dict['scanner'] = False
                        additionals1.play(button1)

                if lights_check.textcheck_click():
                    if lights_check_status == False and len(battery_stack) <= 6:
                        lights_check_status = True
                        battery_stack.append(1)
                        battery_dict['lights'] = True
                        battery_change_after_event = True
                        additionals1.play(button1)
                    else:
                        lights_check_status = False
                        battery_stack.pop()
                        battery_dict['lights'] = False
                        additionals1.play(button1)
                        
            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

            if not ls_check_status and ls_start:
                ls_timer.activate()
                ls_start = False


            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()

            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

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
        global new_press,battery_reset_event,wheels_check_status,sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled,battery_stack,battery_dict
        
        pda_run = True
        while pda_run:
            if battery_reset_event:
                wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
                battery_stack = [1]
                battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
                battery_reset_event = False

            timer.tick(fps)
            if lights_check_status:
                screen.blit(pda_bg,pda_bg_rect)
            else:
                screen.blit(pda_bg_LO,pda_bg_rect)
            screen.blit(pda_surface,(0,0))

            sonar_button = invButton(168,95,273,74,pda_surface,0,True,'SONAR',21,8,'#01240b')
            power_button = invButton(463,95,273,74,pda_surface,0,True,'POWER',20,8,'#01240b')
            pda_text = pixeldub_1.render('COMMS',True,'#01240b')
            pda_surface.blit(pda_text,(776,103))

            tablet_w_indicator = Indicator('W',553,10,16,14,180,indicator_dict['tabletW'])
            tablet_a_indicator = Indicator('A',10,250,21,11,270,indicator_dict['tabletA'])
            data_logs_button = invButton(280,232,256,96,pda_surface,0,True)
            scan_logs_button = invButton(664,232,256,96,pda_surface,0,True)
            comms_button = invButton(472,384,256,88,pda_surface,0,True)
            data_logs_text = pixeldub_1.render('DATA',True,'#dfedf0')
            scan_logs_text = pixeldub_1.render('SCAN',True,'#dfedf0')
            comms_text = pixeldub_1.render('COMMS',True,'#dfedf0')
            logs_text = pixeldub_1.render('LOGS',True,'#dfedf0')
            screen.blit(data_logs_text,(320,229))
            screen.blit(scan_logs_text,(702,229))
            screen.blit(comms_text,(480,397))
            screen.blit(logs_text,(320,272))
            screen.blit(logs_text,(702,272))

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if sonar_button.invcheck_Click():
                    additionals1.play(button2)
                    sonar_screen()
                elif power_button.invcheck_Click():
                    additionals1.play(button2)
                    power_screen()
                elif data_logs_button.invcheck_Click():
                    additionals1.play(button3)
                    data_logs()
                elif scan_logs_button.invcheck_Click():
                    additionals1.play(button3)
                    scan_logs()
                elif comms_button.invcheck_Click():
                    additionals1.play(button3)
                    comms_logs()

            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True
            
            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()

            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

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


    def data_logs():
        global new_press,SCAN_DICT,scan_rect,SCAN_LIST
        current_scanPage = 0
        scan_logs_run_var = True
        while scan_logs_run_var:
            timer.tick(fps)
            screen.blit(base_data,base_data_rect)
            screen.blit(base_data_surface,(0,0))

            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()

            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

            data_logs_esc_indicator = Indicator('ESC',10,10,13,12,270,indicator_dict['LOGS_ESCAPE'])
            
            new_rectCords = [5,93]
            data_POI1 = logButton(True,'DATA') 
            data_POI2 = logButton(True,'DATA')
            data_POI3 = logButton(True,'DATA')
            data_POI4 = logButton(True,'DATA')
            data_POI5 = logButton(True,'DATA')
            data_POI6 = logButton(True,'DATA')
            data_POI7 = logButton(True,'DATA')
            data_POI8 = logButton(True,'DATA')
            data_POI9 = logButton(True,'DATA')
            data_POI10 = logButton(True,'DATA')


            for scan_check in DATASCAN_DICT:
                if DATASCAN_DICT[scan_check]:
                    if scan_check == '1':
                        data_POI1.create(new_rectCords[0],new_rectCords[1],base_data_surface,'GROVE',112,5,'#0b101c','octosquares')
                        new_rectCords[1] += 50
                    elif scan_check == '2':
                        data_POI2.create(new_rectCords[0],new_rectCords[1],base_data_surface,'SPIRALS',98,5,'#0b101c','octosquares')
                        new_rectCords[1] += 50
                    elif scan_check == '3':
                        data_POI3.create(new_rectCords[0],new_rectCords[1],base_data_surface,'METALLIC PLATE',45,5,'#0b101c','octosquares')
                        new_rectCords[1] += 50
                    elif scan_check == '4':
                        data_POI4.create(new_rectCords[0],new_rectCords[1],base_data_surface,'SKELETONS',79,5,'#0b101c','octosquares')
                        new_rectCords[1] += 50
                    elif scan_check == '5':
                        data_POI5.create(new_rectCords[0],new_rectCords[1],base_data_surface,'CAMPSITE',83,5,'#0b101c','octosquares')
                        new_rectCords[1] += 50
                    elif scan_check == '6':
                        data_POI6.create(new_rectCords[0],new_rectCords[1],base_data_surface,'TERRAIN 1',82,5,'#0b101c','octosquares')
                        new_rectCords[1] += 50
                    elif scan_check == '7':
                        data_POI7.create(new_rectCords[0],new_rectCords[1],base_data_surface,'HEMS19',98,5,'#0b101c','octosquares')
                        new_rectCords[1] += 50
                    elif scan_check == '8':
                        data_POI8.create(new_rectCords[0],new_rectCords[1],base_data_surface,'<REDACTED>',73,5,'#0b101c','octosquares')
                        new_rectCords[1] += 50
                    elif scan_check == '9':
                        data_POI9.create(new_rectCords[0],new_rectCords[1],base_data_surface,'UNKNOWN',82,5,'#0b101c','octosquares')
                        new_rectCords[1] += 50
                    elif scan_check == '10':
                        data_POI10.create(new_rectCords[0],new_rectCords[1],base_data_surface,'TERRAIN 2',82,5,'#0b101c','octosquares')
                        new_rectCords[1] += 50
            

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if data_POI1.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 1
                if data_POI2.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 2
                if data_POI3.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 3
                if data_POI4.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 4
                if data_POI5.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 5
                if data_POI6.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 6
                if data_POI7.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 7
                if data_POI8.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 8
                if data_POI9.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 9
                if data_POI10.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 10

            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

            if current_scanPage == 1:
                screen.blit(data1,(0,0))
            if current_scanPage == 2:
                screen.blit(data2,(0,0))
            if current_scanPage == 3:
                screen.blit(data3,(0,0))
            if current_scanPage == 4:
                screen.blit(data4,(0,0))
            if current_scanPage == 5:
                screen.blit(data5,(0,0))
            if current_scanPage == 6:
                screen.blit(data6,(0,0))
            if current_scanPage == 7:
                screen.blit(data7,(0,0))
            if current_scanPage == 8:
                screen.blit(data8,(0,0))
            if current_scanPage == 9:
                screen.blit(data9,(0,0))
            if current_scanPage == 10:
                screen.blit(data10,(0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    scan_logs_run_var = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        indicator_dict['LOGS_ESCAPE'] = False
                        pda_screen()

            pygame.display.update()
        pygame.quit()

    def scan_logs():
        global new_press,SCAN_DICT,scan_rect,SCAN_LIST,active_map

        current_scanPage = 0
        scan_logs_run_var = True
        while scan_logs_run_var:
            timer.tick(fps)
            screen.blit(base_scan,base_scan_rect)
            screen.blit(base_scan_surface,(0,0))

            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()

            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

            scan_logs_esc_indicator = Indicator('ESC',10,10,13,12,270,indicator_dict['LOGS_ESCAPE'])
            
            new_rectCords = [5,100]
            scan_POI1 = logButton(True,'SCAN') 
            scan_POI2 = logButton(True,'SCAN')
            scan_POI3 = logButton(True,'SCAN')
            scan_POI4 = logButton(True,'SCAN')
            scan_POI5 = logButton(True,'SCAN')
            scan_POI6 = logButton(True,'SCAN')
            scan_POI7 = logButton(True,'SCAN')
            scan_POI8 = logButton(True,'SCAN')
            scan_POI9 = logButton(True,'SCAN')
            scan_POI10 = logButton(True,'SCAN')
            scan_POI11 = logButton(True,'SCAN')

            for scan_check in SCAN_DICT:
                if SCAN_DICT[scan_check]:
                    if scan_check == '1':
                        scan_POI1.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'BOTANIC LIFE',62,0,'#0b101c','octosquares')
                        new_rectCords[1] += 45
                    elif scan_check == '2':
                        scan_POI2.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'PLANET INFO',66,0,'#0b101c','octosquares')
                        new_rectCords[1] += 45
                    elif scan_check == '3':
                        scan_POI3.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'UNDERGROUND SIGNS',11,0,'#0b101c','octosquares')
                        new_rectCords[1] += 45
                    elif scan_check == '4':
                        scan_POI4.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'CAVE STRUCTURES',37,0,'#0b101c','octosquares')
                        new_rectCords[1] += 45
                    elif scan_check == '5':
                        scan_POI5.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'POSSIBLE LIFE',55,0,'#0b101c','octosquares')
                        new_rectCords[1] += 45
                    elif scan_check == '6':
                        scan_POI6.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'OBJECTS OF INTEREST',10,0,'#0b101c','octosquares')
                        new_rectCords[1] += 45
                    elif scan_check == '7':
                        scan_POI7.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'SURFACE NATURE',44,0,'#0b101c','octosquares')
                        new_rectCords[1] += 45
                    elif scan_check == '8':
                        scan_POI8.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'-----------',100,-2,'#0b101c','octosquares')
                        new_rectCords[1] += 45
                    elif scan_check == '9':
                        scan_POI9.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'UNKNOWN CHAMBER',24,0,'#0b101c','octosquares')
                        new_rectCords[1] += 45
                    elif scan_check == '10':
                        scan_POI10.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'UNKNOWN DEVICE',40,0,'#0b101c','octosquares')
                        new_rectCords[1] += 45
                    elif scan_check == '11':
                        scan_POI11.create(new_rectCords[0],new_rectCords[1],base_scan_surface,'TERMINAL',84,0,'#0b101c','octosquares')
                        new_rectCords[1] += 45

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if scan_POI1.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 1
                if scan_POI2.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 2
                if scan_POI3.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 3
                if scan_POI4.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 4
                if scan_POI5.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 5
                if scan_POI6.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 6
                if scan_POI7.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 7
                if scan_POI8.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 8
                if scan_POI9.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 9
                if scan_POI10.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 10
                if scan_POI11.invcheck_Click():
                    additionals1.play(button1)
                    current_scanPage = 11

            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

            if current_scanPage == 1:
                screen.blit(log1,(0,0))
            if current_scanPage == 2:
                screen.blit(log2,(0,0))
            if current_scanPage == 3:
                screen.blit(log3,(0,0))
            if current_scanPage == 4:
                screen.blit(log4,(0,0))
            if current_scanPage == 5:
                screen.blit(log5,(0,0))
            if current_scanPage == 6:
                screen.blit(log6,(0,0))
            if current_scanPage == 7:
                screen.blit(log7,(0,0))
            if current_scanPage == 8:
                screen.blit(log8,(0,0))
            if current_scanPage == 9:
                screen.blit(log9,(0,0))
            if current_scanPage == 10:
                screen.blit(log10,(0,0))
            if current_scanPage == 11:
                screen.blit(log11,(0,0))

            if SCAN_DICT['9'] and SCAN_DICT['10'] and active_map == 6:
                active_map = 7
                level6_1.remove((player_xDisplay_mod,player_yDisplay_mod))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    scan_logs_run_var = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        indicator_dict['LOGS_ESCAPE'] = False
                        pda_screen()

            pygame.display.update()
        pygame.quit()

    def comms_logs():
        global new_press, user_text, active_frequency

        user_text = ''
        tb_hover = False
        tb_toggle = False
        invalid_flag = False
        load_var = 0
        load_var_flag = False
        comms_logs_run_var = True
        while comms_logs_run_var:
            timer.tick(fps)
            screen.fill('#875a44')
            screen.blit(base_comms_surface,(0,0))

            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()
            
            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

            comms_logs_esc_indicator = Indicator('ESC',10,10,13,12,270,indicator_dict['LOGS_ESCAPE'])

            comms_text = octosquares1.render('COMMS',True,'white')
            textbox_text = EType_2.render(user_text,True,'white')
            connecting_text = EType_2.render('FREQUENCY FOUND! CONNECTING...',True,'#2effc0')
            tutorial_text = EType_2.render('Enter text here (###.#)',True,'gray')
            invalid_text = EType_2.render('INVALID FORMAT OR SIGNAL',True,'#5d1121')
            khz_text = EType_2.render('kHz',True,'white')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    comms_logs_run_var = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        indicator_dict['LOGS_ESCAPE'] = False
                        pda_screen()

                    #checking for text input:
                    if tb_hover:
                        if event.key == pygame.K_BACKSPACE and len(user_text) >= 0:
                            user_text = user_text[:-1]
                        elif len(user_text) < 5 and event.key not in (pygame.K_RETURN,pygame.K_CAPSLOCK,pygame.K_TAB):
                            user_text += event.unicode
                        if event.key == pygame.K_RETURN:
                            if len(user_text) == 5:
                                if user_text in ('199.8','208.3','211.4','139.9','152.5','167.0','92913') or (user_text == '426.6' and SCAN_DICT['11']):
                                    active_frequency = user_text
                                    load_var_flag = True
                                else:
                                    invalid_flag = True
                                    load_var_flag = False
                                    
            
            if invalid_flag:
                screen.blit(invalid_text,(455,455))
            if load_var_flag:
                screen.blit(connecting_text,(425,455))
                if load_var == 80:
                    comms_logs_open()
                else:
                    load_var += 1
            screen.blit(comms_text,(460,50))
            tb_rect = pygame.rect.Rect((525,425),(100,25))
            pygame.draw.rect(base_comms_surface,(50,50,50),(520,420,110,35))
            pygame.draw.rect(base_comms_surface,(25,25,25),tb_rect)
            screen.blit(textbox_text,(545,425))
            screen.blit(khz_text,(640,425))
            if user_text == '':
                screen.blit(tutorial_text,(475,455))

            mouse_pos = pygame.mouse.get_pos()
            left_click = pygame.mouse.get_pressed()[0]
            if left_click:
                if tb_rect.collidepoint(mouse_pos):
                    tb_hover = True
                elif not tb_rect.collidepoint(mouse_pos):
                    tb_hover = False

            if len(user_text) != 5:
                invalid_flag = False
            pygame.display.update()
        pygame.quit()


    def comms_logs_open():
        global new_press, user_text,active_frequency, active_map, POI_DICT,endEvent_dict

        if active_frequency == '208.3' and active_map in (6,7):
            active_frequency = '199.8'
        if active_frequency == '199.8':
            alpha_val = 240
            direction = 0
        elif active_frequency in ('208.3','152.5'):
            alpha_val = 0
            active_page = 0
        elif active_frequency in ('139.9','167.0','211.4'):
            alpha_val = 0
        elif active_frequency == '426.6':
            active_page = 0
            alpha_val = 0


        comms_logs_run_var = True
        while comms_logs_run_var:
            timer.tick(fps)
            screen.fill('#875a44')

            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()

            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

            #performing required tasks as per frequency
            if active_frequency == '199.8':
                screen.fill('#36241b')
                rcso_screen.set_alpha(alpha_val)
                screen.blit(rcso_screen,(0,0))
                if alpha_val == 20:
                    direction = 1
                elif alpha_val == 240:
                    direction = -1

                if direction == 1:
                    alpha_val += 10
                elif direction == -1:
                    alpha_val -= 10
            
            elif active_frequency == '208.3':
                screen.blit(aero_chat_bg,(0,0))

                if active_page == 0:
                    alpha_val = 0
                elif active_page == 1:
                    alpha_val = 0
                    text21 = EType_2.render('Current Distance from surface of planet KR749 - 541,256km off the surface',True,'gray')
                    screen.blit(text21,((230,300)))
                elif active_page == 2:
                    alpha_val = 0
                    progress = 0.0
                    for i in POI_DICT:
                        if POI_DICT[i] == False:
                            progress += 7.14
                    text22 = EType_2.render('Current Mission Progress: {0}%'.format(round(progress,2)),True,'gray')
                    screen.blit(text22,((430,300)))
                elif active_page == 3:
                    alpha_val = 0
                    screen.blit(aero_chat_3,(-20,30))
                elif active_page == 4:
                    if alpha_val != 300:
                        alpha_val += 1

                    text241 = EType_2.render('[ATTEMPTING TO ESTABLISH DIRECT CONNECTION LINE BETWEEN FN34 AND AERONAUTIX STATION]',True,'light gray')
                    screen.blit(text241,((150,300)))
                    if alpha_val > 80:
                        text242 = EType_2.render('[CONNECTION ESTABLISHED! AWAITING ANSWER]',True,'green')
                        screen.blit(text242,((370,340)))
                    if alpha_val == 300:
                        text243 = EType_2.render(' [CONNECTION REJECTED]',True,'red')
                        screen.blit(text243,((470,380)))

            elif active_frequency == '139.9':
                screen.fill('black')
                if alpha_val == 80:
                    screen.blit(prescott_log,(0,0))
                else:
                    alpha_val += 1
                text3 = EType_2.render('[139.9kHz - TRANSCRIBING BROADCAST]',True,'gray')
                screen.blit(text3,((400,70)))
                
            elif active_frequency == '152.5':
                screen.fill('black')
                screen.blit(hems19_welcome,(0,0))

                if active_page == 0:
                    pass
                elif active_page == 1:
                    screen.blit(blumstein_journal,(0,0))
                elif active_page == 2:
                    screen.blit(marek_journal,(0,0))
                elif active_page == 3:
                    screen.blit(szarka_journal,(0,0))
                elif active_page == 4:
                    screen.blit(prescott_journal,(0,0))

            
            elif active_frequency == '167.0':
                screen.fill('black')
                if alpha_val == 80:
                    screen.blit(marek_log,(0,0))
                else:
                    alpha_val += 1
                text5 = EType_2.render('[167.0kHz - TRANSCRIBING BROADCAST]',True,'gray')
                screen.blit(text5,((400,70)))
            
            elif active_frequency == '211.4':
                screen.fill('black')
                if alpha_val == 80:
                    screen.blit(blumstein_log,(0,0))
                else:
                    alpha_val += 1
                text6 = EType_2.render('[211.4kHz - TRANSCRIBING BROADCAST]',True,'gray')
                screen.blit(text6,((400,70)))

            elif active_frequency == '426.6':
                endEvent_dict['monstercrash'] = True
                screen.fill('black')
                if alpha_val == 80:
                    screen.blit(alien_start_log,(0,0))
                    if active_page == 0:
                        pass
                    elif active_page == 1:
                        screen.blit(alien_lab_log,(0,0))
                    elif active_page == 2:
                        screen.blit(alien_device_log,(0,0))
                    elif active_page == 3:
                        screen.blit(alien_result_log,(0,0))
                else:
                    alpha_val += 1
                    text5 = EType_2.render('[426.6kHz - ATTEMPTING TO TRANSLATE ALIEN BROADCAST]',True,'gray')
                    screen.blit(text5,((330,270)))

            elif active_frequency == '92913':
                screen.blit(log92913,(0,0))
            
            comms_logs_esc_indicator = Indicator('ESC',10,10,13,12,270,indicator_dict['LOGS_ESCAPE'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    comms_logs_run_var = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        indicator_dict['LOGS_ESCAPE'] = False
                        comms_logs()
                    
                    if active_frequency in ('208.3','152.5'):
                        if event.key == pygame.K_1:
                            active_page = 1
                        elif event.key == pygame.K_2:
                            active_page = 2
                        elif event.key == pygame.K_3:
                            active_page = 3
                        elif event.key == pygame.K_4:
                            active_page = 4
                        else:
                            active_page = 0
                    elif active_frequency == '426.6' and alpha_val == 80:
                        if event.key == pygame.K_1:
                            active_page = 1
                        elif event.key == pygame.K_2:
                            active_page = 2
                        elif event.key == pygame.K_3:
                            active_page = 3
                        else:
                            active_page = 0
            pygame.display.update()
        pygame.quit()


    def notice_board_view():
        global new_press,POI_DICT,POI_DICT,endEvent_dict,battery_reset_event,wheels_check_status,sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled,battery_stack,battery_dict

        additionals2.stop()
        notice_board_var = True
        while notice_board_var:
            if battery_reset_event:
                wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
                battery_stack = [1]
                battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
                battery_reset_event = False

            timer.tick(fps)
            if lights_check_status:
                screen.blit(notice_board_bg,notice_board_bg_rect)
            else:
                screen.blit(notice_board_bg_LO,notice_board_bg_rect)
            screen.blit(notice_board_surface,(0,0))

            notice_board_button = invButton(228,108,744,280,notice_board_surface,0,lights_check_status)
            notice_board_d_indicator = Indicator('D',1130,250,15,11,90,indicator_dict['noticeD'])
            notice_board_LMB_indicator = Indicator('LMB',570,400,0,4,180,indicator_dict['noticeboardLMB'])

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if notice_board_button.invcheck_Click():
                    indicator_dict['noticeboardLMB'] = False
                    notice_board_open()

            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()

            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RIGHT,pygame.K_6,pygame.K_d):
                        indicator_dict['noticeD'] = False
                        main_view()
                if event.type == pygame.QUIT:
                    notice_board_var = False

            pygame.display.update()
        pygame.quit()
    
    def notice_board_open():
        global new_press,indicator_dict,battery_reset_event,wheels_check_status,sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled,battery_stack,battery_dict

        openNotice_dict = {'MB':(True,False),'RSB':(True,False),'TC':(True,False),'EI':(True,False),'LF':(True,False),'CN':(True,False)} #1-enabled,2-active
        page_open = False
        
        bg_audio.pause()
        notice_board_open_var = True
        while notice_board_open_var:
            if battery_reset_event:
                wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, scanner_check_status, lights_check_status = False,False,True,False,False,False
                wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, scanner_check_enabled, lights_check_enabled = True,True,True,True,True,True
                battery_stack = [1]
                battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'scanner':False,'lights':False}
                battery_reset_event = False

            timer.tick(fps)
            screen.blit(notice_board_bg,notice_board_bg_rect)
            darken.set_alpha(90)
            screen.blit(darken,(0,0))
            screen.blit(notice_board_open_surface,(0,0))
            screen.blit(sMissionB,(325,50))
            screen.blit(sRoverSB,(525,50))
            screen.blit(sTabletC1,(725,50))
            screen.blit(sEnvI1,(325,315))
            screen.blit(sLiabF,(525,315))
            screen.blit(sCrumpN1,(725,315))

            notice_board_escape_indicator = Indicator('ESC',10,10,13,12,270,indicator_dict['NOTICE_ESCAPE'])
            MB_button = invButton(325,50,144,256,notice_board_open_surface,0,openNotice_dict['MB'][0])
            RSB_button = invButton(525,50,144,256,notice_board_open_surface,0,openNotice_dict['RSB'][0])
            TC_button = invButton(725,50,144,256,notice_board_open_surface,0,openNotice_dict['TC'][0])
            EI_button = invButton(325,315,144,256,notice_board_open_surface,0,openNotice_dict['EI'][0])
            LF_button = invButton(525,315,144,256,notice_board_open_surface,0,openNotice_dict['LF'][0])
            CN_button = invButton(725,315,144,256,notice_board_open_surface,0,openNotice_dict['CN'][0])
            back_button = invButton(10,10,200,64,notice_board_open_surface,120,page_open,'BACK',10,2,'white')

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
                if MB_button.invcheck_Click():
                    additionals2.play(paper_shuffle)
                    openNotice_dict = {'MB':(False,True),'RSB':(False,False),'TC':(False,False),'EI':(False,False),'LF':(False,False),'CN':(False,False)}
                    page_open = True
                elif RSB_button.invcheck_Click():
                    additionals2.play(paper_shuffle)
                    openNotice_dict = {'MB':(False,False),'RSB':(False,True),'TC':(False,False),'EI':(False,False),'LF':(False,False),'CN':(False,False)}
                    page_open = True
                elif TC_button.invcheck_Click():
                    additionals2.play(paper_shuffle)
                    openNotice_dict = {'MB':(False,False),'RSB':(False,False),'TC':(False,True),'EI':(False,False),'LF':(False,False),'CN':(False,False)}
                    page_open = True
                elif EI_button.invcheck_Click():
                    additionals2.play(paper_shuffle)
                    openNotice_dict = {'MB':(False,False),'RSB':(False,False),'TC':(False,False),'EI':(False,True),'LF':(False,False),'CN':(False,False)}
                    page_open = True
                elif LF_button.invcheck_Click():
                    additionals2.play(paper_shuffle)
                    openNotice_dict = {'MB':(False,False),'RSB':(False,False),'TC':(False,False),'EI':(False,False),'LF':(False,True),'CN':(False,False)}
                    page_open = True
                elif CN_button.invcheck_Click():
                    additionals2.play(paper_shuffle)
                    openNotice_dict = {'MB':(False,False),'RSB':(False,False),'TC':(False,False),'EI':(False,False),'LF':(False,False),'CN':(False,True)}
                    page_open = True
                elif back_button.invcheck_Click():
                    page_open = False

            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True

            if page_open:
                if back_button.enabled:
                    pygame.draw.rect(notice_board_open_surface,(0,255,0,120),(210,10,20,20))
            else:
                openNotice_dict = {'MB':(True,False),'RSB':(True,False),'TC':(True,False),'EI':(True,False),'LF':(True,False),'CN':(True,False)}
                if back_button.enabled: 
                    pygame.draw.rect(notice_board_open_surface,(255,0,0,120),(210,10,20,20))


            if openNotice_dict['MB'][1]:
                screen.blit(notice_board_bg,notice_board_bg_rect)
                darken.set_alpha(180)
                screen.blit(darken,(0,0))
                screen.blit(notice_board_open_surface,(0,0))
                screen.blit(MissionB,(400,-7))
            elif openNotice_dict['RSB'][1]:
                screen.blit(notice_board_bg,notice_board_bg_rect)
                darken.set_alpha(180)
                screen.blit(darken,(0,0))
                screen.blit(notice_board_open_surface,(0,0))
                screen.blit(RoverSB,(400,-7))
            elif openNotice_dict['TC'][1]:
                screen.blit(notice_board_bg,notice_board_bg_rect)
                darken.set_alpha(180)
                screen.blit(darken,(0,0))
                screen.blit(notice_board_open_surface,(0,0))
                screen.blit(TabletC1,(330,-7))
                screen.blit(TabletC2,(730,-7))
            elif openNotice_dict['EI'][1]:
                screen.blit(notice_board_bg,notice_board_bg_rect)
                darken.set_alpha(180)
                screen.blit(darken,(0,0))
                screen.blit(notice_board_open_surface,(0,0))
                screen.blit(EnvI1,(330,-7))
                screen.blit(EnvI2,(730,-7))
            elif openNotice_dict['LF'][1]:
                screen.blit(notice_board_bg,notice_board_bg_rect)
                darken.set_alpha(180)
                screen.blit(darken,(0,0))
                screen.blit(notice_board_open_surface,(0,0))
                screen.blit(LiabF,(400,0))
            elif openNotice_dict['CN'][1]:
                screen.blit(notice_board_bg,notice_board_bg_rect)
                darken.set_alpha(180)
                screen.blit(darken,(0,0))
                screen.blit(notice_board_open_surface,(0,0))
                screen.blit(CrumpN1,(330,-7))
                screen.blit(CrumpN2,(730,-7))

            if ls_timer.active:
                ls_timer.current_time = pygame.time.get_ticks()
                ls_timer.update()

            if ls_timer.timeout:
                COD_dict['ls'] = True
                game_over_screen()

            if cavefall_timer.active:
                cavefall_timer.current_time = pygame.time.get_ticks()
                cavefall_timer.update()

            if cavefall_timer.timeout:
                additionals1.stop()
                cavefall_timer.timeout = False
                additionals1.play(fall_crash)
                blackout()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE,):
                        pygame.draw.rect(notice_board_open_surface,(255,0,0,120),(210,10,20,20))
                        indicator_dict['NOTICE_ESCAPE'] = False
                        bg_audio.unpause()
                        notice_board_view()
                if event.type == pygame.QUIT:
                    notice_board_open_var = False
            
            pygame.display.update()
        pygame.quit()

    #EXTRAS:  
    def blackout():
        global new_press,battery_reset_event,lights_check_status

        bg_audio.stop()
        timer_var = 0
        battery_reset_event = True
        lights_check_status = False if lights_check_status == True else False
        ls_timer.deactivate()
        run_var = True
        while run_var:
            timer.tick(fps)
            screen.fill('black')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_var = False

            if timer_var != 185:
                timer_var += 1
            else:
                fadeScreen.fade_flag = True
                main_view()

            pygame.display.update()
        pygame.quit()
    
    def animation_end():
        global new_press,COD_dict,end_animation
        additionals3.fadeout(2000)
        end_animation = Video(absolute_path + r'\assets\images\ds_animation.mp4')
        end_animation.set_size((1200,700))
        end_animation.set_volume(0.6)
        timer_var = 0
        render_offset = [0,0]
        animation_run_var = True
        while animation_run_var:
            timer.tick(fps)

            end_animation.draw(screen,(render_offset[0],render_offset[1]-50),False)
            if timer_var == 16:
                additionals1.play(warning_alert)
            if 18 < timer_var < 28:
                render_offset[0],render_offset[1] = random.randint(0,16) - 8,random.randint(0,16) - 8
            elif 28 < timer_var < 89:
                render_offset[0],render_offset[1] = random.randint(0,2) - 1,random.randint(0,2) - 1
            if timer_var == 30:
                additionals2.play(ending_fade)
                additionals3.play(ending_hardhit,0,0,2000)
            if timer_var == 89:
                end_animation.close()
                COD_dict['fin'] = True
                warning_alert.fadeout(2000)
                game_over_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_animation.close()
                    pygame.quit()
            timer_var += 1
            pygame.display.update()

    def game_over_screen():
        global COD_dict
        bg_audio.stop()
        enter_GO = True
        end_var = 0
        
        if enter_GO and not COD_dict['fin']:
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

        while True:
            timer.tick(fps)
            screen.fill('black')
            text = octosquares2.render('GAME OVER',True,'#9c1947')
            screen.blit(text,(490,250))
            if COD_dict['crash']:
                COD = octosquares3.render('You crashed into the canyon walls.',True,'#6e1232')
                screen.blit(COD,(456,300))
            if COD_dict['ls']:
                COD = octosquares3.render('You ran out of oxygen.',True,'#6e1232')
                screen.blit(COD,(504,300))

            if COD_dict['fin']:
                if end_var == 1:
                    pass
                if end_var == 210:
                    COD = octosquares3.render('THANKS FOR PLAYING.',True,'#6e1232')
                    screen.blit(COD,(495,300))
                else:
                    if end_var >= 127:
                        screen.blit(end_pic,(0,0))
                        end_var += 1
                    else:
                        screen.fill('black')
                        fade_img.set_alpha(((127-end_var)*2)-20)
                        screen.blit(end_pic,(0,0))
                        screen.blit(fade_img,(0,0))
                        end_var += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()
    
    title_screen()
main_gameLoop()

'''
TASKS:
(This section doesnt affect the code at all, its just notes made by the devs to add to the game)

[DONE]  --------------------    (PHASE 1: BASIC FUNCTIONS)
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

[DONE]  --------------------    (PHASE 2: MOVEMENT AND CAMERA)
* [DONE] (LONG) START WORKING ON:
    [DONE] MOVEMENT SYSTEM AND SONAR DISPLAY
    [DONE] ADD X,Y,Z COORDINATES TO THE SONAR DISPLAY
* [DONE] DECORATE THE NOTICE BOARD AND CAMERA VIEWS, THEN ADD AND TEST NOTICE BOARD FUNCTIONALITY EITHER THROUGH POP-UPS OR THROUGH WRITTEN TEXT FOR GAME CONTROLS AND OBJECTIVES
* [DONE] INTEGRATE AN X-Y-Z COORDINATE SYSTEM INTO THE SONAR VIEW SCREEN
* [DONE] FIX THE POIS SO THAT EACH OF THEM HAVE A UNIQUE IDENTIFIER AND ARE EITHER CREATED DIRECTLY ON THE MAP OR ARE STORED EXTERNALLY. THEY SHOULD ACTIVATE THE AUTHORIZATION SEQUENCE IF THE PLAYER OVERLAPS IN THEIR AREA
* [DONE] ADD CAMERA FUNCTIONALITY SO THAT IT TAKES PICTURES WITH SINE WAVES FOR THE RADIO WHENEVER THE PLAYER PRESSES THE 'CAPTURE' BUTTON. ALSO ONLY ALLOW PICTURE-TAKING WHEN PLAYERS ARE AUTHORIZED TO DO SO

[DONE]  --------------------    (PHASE 3: ADDITIONAL FEATURES AND TWEAKS)
* [DONE] CREATE THE BACKGROUND STORY AND ADD IT TO THE BACKSTORY PAGE
* [DONE] ADD THE OXYGEN METER TO THE FRONT IN THE MAIN VIEW. IT IS CONTAINED WITHIN A CLASS AND IT UPDATES WHEN CALLED SPECIFICALLY (based on in-game events). FOR TESTING PURPOSES, IT UPDATES WHEN THE BATTERY LEVEL GOES DOWN.
* [DONE] (OPTIONAL) CHANGE THE SONAR SCREEN SO THAT IT CAN ALWAYS BE ACTIVATED, BUT IF THE SONAR OPTION IN THE POWER SCREEN IS TURNED OFF IT WILL JUST SHOW THAT THE SONAR IS OFFLINE. THE PLAYER CAN STILL MOVE AROUND, BUT THEY CANT SEE WHERE THEY ARE GOING.
* [DONE] FIX THE OXYGEN METER SO THAT ITS COLOR MATCHES AND IT REACTS TO LIGHTING
* [DONE] FIX THE SONAR SCREEN SO THAT IT CAN ALWAYS BE ACTIVATED AND IT ONLY SHOWS ITS OFFLINE WHEN YOU DONT CLICK ANYTHING
* --[SCRAPPED,REDONE]-- ADD A CLASS TO IMPLEMENT NOTIFICATIONS TO THE GAME. IT SHOULD BLIT A TEXT BOX ON THE TOP OF THE SCREEN CONTAINING THE REQUIRED INFORMATION, AND SHOULD LEAVE AFTER A CERTAIN AMOUNT OF TIME.
* [DONE] FIX THE OXYGEN METER SO THAT ITS COLOR MATCHES AND IT REACTS TO LIGHTING

[DONE]  --------------------    (PHASE 4: SCANNING) 
* [DONE] (LONG) ADD A METHOD TO IMPLEMENT A SCAN FUNCTION INTO THE GAME. WHEN THE SCANNER OPTION IS TURNED ON IN THE POWER MENU AND THE PLAYER PASSES OVER A '4' OR '5' IN THE MAP, PROVIDE INFORMATION WITHIN THE SCANNER PORTION.
* [DONE] DEVELOP THE PDA/COMMS SCREEN. IT SHOULD CONTAIN THE OPTIONS TO SELECT DATA LOGS(from ship scans),SCAN LOGS(based on environmental data), AND COMMUNICATIONS(external help from the VC).
    [DONE] DATA LOGS SHOULD ONLY BE UPDATED WITH INFO SENT FROM WRECKAGE SCANS (scanning the HEMS, only adds entries based on the scanner button in the camera room)
    [DONE] COMMUNICATIONS SHOULD UPDATE RARELY (most significant instance is the external broadcast from an official on the mission team informing you wont be coming back)
    [DONE] SCAN LOGS SHOULD CONSTANTLY UPDATE WITH INFORMATION SO LONG AS THE SCANNER IS TURNED ON IN THE POWER SECTION. SPECIFIC ENVIRONMENTAL DETAILS AND SCANS OCCUR AS THE PLAYER MOVES FORWARD/PROGRESSES THROUGH THE GAME. MOST SIGNIFACT USES WOULD BE FOR WORLDBUILDING WHEN SCANNING THE MONSTER IN THE END OR THE CAVES IT CREATES THROUGHOUT THE GAME
* [DONE] ADD THE SCANNER IN THE CAMERA ROOM. IT ONLY WORKS WHEN TURNED ON AND WHEN AUTHORIZED (seperate from picture authorization). IT SCANS INFO AND PLACES IT UNDER THE "DATA LOGS" SECTION IN THE PDA.

[DONE]  --------------------    (PHASE 5: MAP GENERATION) 
* [DONE] TEST OUT CREATING NEW MAP CLASSES SO THAT DIFFERENT CHUNKS OF MAP CAN BE LOADED WHENEVER A PICTURE IS TAKEN.
* [DONE] (V. LONG) IMPLEMENT METHODS TO SWITCH THE GAME MAP INTO A NEW MAP CONTAINING THE ALIEN FACILITY SO THAT THE PLAYER MAY EXPLORE IT

[DONE]  --------------------    (PHASE 6: AUDIO IMPLEMENTATION)
* [DONE] ADD WAYS TO IMPLEMENT SOUND EFFECTS AND BACKGROUND AUDIO INTO THE GAME, SPECIFICALLY FOR:
    [DONE] TITLE SCREEN/BACKSTORY, AND ROVER BACKGROUND MUSIC
    [DONE] SOUND EFFECTS FOR MOVING THE ROVER
    [DONE] BUTTON PRESSES (POWER MENU BUTTONS, CAMERA BUTTON AND SCANNER BUTTON)
    [DONE] PAPER SHUFFLING (SOUNDS FOR THE NOTICE BOARD)
    [SCRAPPED] LIGHT BULB SOUND EFFECTS (DISAPPEARS WHEN BULB IS TURNED OFF)
    [DONE] CAMERA PICTURE SOUND (WHEN A PICTURE IS BEING DISPLAYED)
    [DONE] NOTIFICATION SOUND (ONE FOR THE SCANNER AND ONE FOR AN IMPACT)

 --------------------    (PHASE 7:EXTRA ADDITIONS)
* [DONE] (LONG) IMPLEMENT A NOTIFICATION CLASS. IT SHOULD HAVE TWO DIFFERENT TYPES (as of now):
    [DONE] 1. IMPACT - BLITS AN IMAGE ON THE SCREEN SAYING AN IMPACT HAS BEEN DETECTED. OCCURS DURING BATTERY RESET EVENTS WHILE INSIDE THE SONAR VIEW
    [DONE] 2. SCAN - BLITS A SMALL IMAGE ON THE TOP OF THE SCREEN IN THE SONAR VIEW WHEN RUNNING OVER A SCANNABLE AREA. ALL IT SHOULD SAY IS (NEW SCAN OBTAINED! ADDING TO LOG...)
* [DONE] CREATE AND ADD NOISE FILTERS OF VARIOUS DEGREES THAT GO OVER THE SONAR VIEW SCREEN. THE AMOUNT OF NOISE CORRESPONDS TO THE MAX AVAILABLE BATTERY
* [DONE] DRAW THE NOTICE BOARD AND MAP
* [DONE] DESIGN THE GAME WINDOW ICON
* [DONE] DESIGN THE FACILITY MAP (PHASE 5 LAST TASK)
* [DONE] (LONG) DRAW THE FACILITY PICTURE AND MONSTER PICTURE


PROBLEMS:
[DONE]  1. Fix the camera system to update POIs properly (problem with global values of player_xDisplay_mod and player_yDisplay_mod)
[DONE]  2. Fix the method to trigger a battery reset event when arriving at a POI. (related to battery_change_after_event)
[DONE]  3. Update all screen-blitted text to be built into the images itself so that when the lights turn off they get darkened as well (related to camButton text and activation rectangle, and main view oxygen meter)
[DONE]  4. Fix the issue where overlapped sound effects get distorted (related to playing the rover moving sfx over the background rover sound effect on seperate channels)


FINAL TO-DO LIST:
[DONE] MAKE THE SCANNED DOCUMENTS BLIT ONLY BASED IN ORDER 
[DONE] MAKE IT SO SCANNED DOCUMENTS ONLY APPEAR WHEN THE SCANNER OPTION IS TURNED ON
[DONE] ADD ALL 5 LEVELS TO THE GAME
[DONE] CHECK IF YOU CAN NAVIGATE ALL 5 LEVELS PROPERLY
[DONE] SEE IF YOU CAN ADD AN EVENT TO THE 4TH LEVEL TO CUT THE POWER RIGHT AT THE TRANSITION POINT
[DONE] REPLACE THE ENTRANCE TO THE 4TH POI SO THAT IT IS RIGHT OUTSIDE THE CAVE INSTEAD OF INSIDE IT. MAKE A NEW TRANSITION WHERE AN IMPACT OCCURS AND IT CHANGES TO THE OTHER SCREEN
[DONE] CREATE THE NOTIFICATION CLASS (PHASE 7 FIRST TASK)
[DONE] IMPLEMENT EVERY SCAN LOCATION, AND JUST USE SOME ADDITIONAL TEXT FOR THE BUTTONS TO SEE IF EACH OF THEM BLIT PROPERLY
[DONE] WORK ON THE COMMS SCREEN
[DONE] ADD THE CAMERA IMAGES INTO THE GAME
[DONE] ADD A SHAKE EFFECT FOR THE IMPACT SCREEN
[DONE] FINISH THE POI MARKER CLASS
[DONE] FIX THE 139.9 BROADCAST AND THE SCAN YOU GET WHEN FALLING INTO THE CAVE
[DONE] FIX THE TERRAIN ASSESSMENTS TO SAY PILOT INSTEAD OF PLAYER, AND MAKE MORE OF THE INITIAL SYSTEMS SHOW THEIR STATUS TO IMPROVE THE DIFFERENCE BETWEEN TA1 AND TA2
[DONE] ADD THE 456.6 BROADCAST
[DONE] ADD THE EVENT WHERE THE MONSTER FINDS YOU AND KILLS YOU (continue, event added, add the camera event where the picture is taken)
[DONE] FIX THE PRESCOTT AND BLUMSTEIN TEXT TO BE GRAMMATICALLY CORRECT
[DONE] FIX THE MAP AND SONAR COORDINATE SYSTEMS SO THEY ALIGN PROPERLY
[DONE] FINISH THE FINAL ANIMATION WHERE THE PLAYER GETS ATTACKED BY THE MONSTER (add a radiation fog effect, make the rover warning lights go off, add some camera shake, then improve the original camera picture to make the creature more disheveled and menacing.)
[DONE] FIX THE ISSUE WITH THE ENDING_FADE MUSIC NOT PLAYING ON ANY CHANNEL IN THE GAME OVER SCREEN
[DONE] ADD THE SOUND EFFECTS TO THE GAME(CAMERA SFX, OXYGEN ALERT, FACILITY AMBIENT NOISES, MAKE BLACKOUT LOUDER)
[DONE] START THE GAME FROM THE FIRST LEVEL, AND DO A CHECK ON EVERY MAJOR SYSTEM, LIST OR VARIABLES (POI_DICT,SCAN_DICT,EVENT_DICT,DATASCAN_DICT,OXYGEN_METER,BATTERY_MAX,MAP POSITIONS,POI MARKERS)
!END OF ALL TASKS - PROJECT COMPLETED!  ------- [DONE]


TOTAL LINES OF CODE - 4,263
'''