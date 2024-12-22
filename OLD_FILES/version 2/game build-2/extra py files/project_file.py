#IMPORT AND INITIALIZE PYGAME AND OS:
import pygame
import os

pygame.init()

#DECLARING SPECIFIC VARIABLES:
absolute_path = os.path.dirname(__file__)
SCREEN_WIDTH,SCREEN_HEIGHT = 1200,600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font(absolute_path + r"\assets\game_font\TT Octosquares Trial Condensed Black.ttf",18)
new_press = True
wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, radio_check_status, lights_check_status = False,False,True,False,False,True
wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, radio_check_enabled, lights_check_enabled = True,True,True,True,True,True
battery_stack = [1,1]
battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'radio':False,'lights':True}
battery_max = 6
battery_reset_event = False

outside_fadeFlag = False
#SURFACES:
title_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
backstory_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
play_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
sonar_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
power_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
pda_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
battery_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)

#IMAGES:
#backgrounds:
title_bg = pygame.image.load(absolute_path + r'\assets\images\title_screen.png').convert_alpha()
title_bg = pygame.transform.scale(title_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
play_bg = pygame.image.load(absolute_path + r'\assets\images\play_screen.png').convert_alpha()
play_bg = pygame.transform.scale(play_bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
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

fade_img = pygame.image.load(absolute_path + r'\assets\images\fade.png').convert_alpha()
fade_img = pygame.transform.scale(fade_img,(1200,600))

#CLASSES:

class Button:
    def __init__(self,text,x_pos,y_pos,x_offset,enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_offset = x_offset
        self.enabled = enabled
        self.draw()
    
    def draw(self):
        button_Text = font.render(self.text,True,'black')
        button_Rect = pygame.rect.Rect((self.x_pos,self.y_pos),(200,20))
        if self.enabled:
            if self.check_click():
                pygame.draw.rect(screen,'dark gray',button_Rect,0,5)
            else:
                pygame.draw.rect(screen,'gray',button_Rect,0,5)
        else:
            pygame.draw.rect(screen,'black',button_Rect,0,5)
        pygame.draw.rect(screen,'black',button_Rect,2,5)
        screen.blit(button_Text,(self.x_pos + self.x_offset,self.y_pos))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = button_rect = pygame.rect.Rect((self.x_pos,self.y_pos),(200,20))
        if left_click and self.enabled and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

class invButton:
    def __init__(self, x_pos, y_pos, b_width, b_height, b_surface, opacity,enabled):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.b_width = b_width
        self.b_height = b_height
        self.b_surface = b_surface
        self.opacity = opacity
        self.enabled = enabled
        self.draw()

    def draw(self):
        pygame.draw.rect(self.b_surface,(255,0,0,self.opacity),(self.x_pos,self.y_pos,self.b_width,self.b_height))

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
        button_disableText = font.render(self.text,True,'white')
        button_crossText = font.render('X',True,'red')
        if self.active:
            button_status = 'ON'
            button_statusText = font.render(button_status,True,'green')
        else:
            button_status = 'OFF'
            button_statusText = font.render(button_status,True,'dark red')
        button_Text = font.render(self.text,True,'black')
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

#FUNCTIONS TO RUN THE GAME (SCREENS):
def title_screen(): 
    global new_press
    pygame.display.set_caption('Title')
    title_run = True
    while title_run:
        timer.tick(fps)
        screen.blit(title_bg,title_bg_rect)
        screen.blit(title_surface,(0,0))


        play_button = invButton(451,332,336,53,title_surface,0,True)
        quit_button = invButton(452,475,336,53,title_surface,0,True)

        if pygame.mouse.get_pressed()[0] and new_press:
            new_press = False
            if play_button.invcheck_Click():
                fadeScreen.fadeIn()
                if fadeScreen.fade_flag:
                    backstory()

            if quit_button.invcheck_Click():
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
    back_text1 = font.render('oh no government sent u here bla bla bla land rover omg wow weird research team didnt come',True,'black')
    back_text2 = font.render('back no way so scary navigate a canyon spooky caves oh noes monster chasing you so spoopy',True,'black')

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

    testtext1 = font.render('main view',True,'black')
    if fadeScreen.fade_flag:
        fade_run = True
        alpha = 180
        while fade_run:
            screen.fill('dark gray')
            screen.blit(testtext1,(200,200))
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
        screen.fill('dark gray')
        screen.blit(testtext1,(200,200))
        

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN,pygame.K_2,pygame.K_s):
                    welcome_screen()
                elif event.key in (pygame.K_RIGHT,pygame.K_6,pygame.K_d):
                    camera_view()
                elif event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
                    notice_board_view()
            if event.type == pygame.QUIT:
                main_view_var = False

        pygame.display.update()
    pygame.quit()

def map_view():
    global new_press
    pygame.display.set_caption('Map')
    testtext2 = font.render('map view',True,'black')
    map_view_var = True
    while map_view_var:
        timer.tick(fps)
        screen.fill('orange')
        screen.blit(testtext2,(200,200))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP,pygame.K_8,pygame.K_w):
                    main_view()
                elif event.key in (pygame.K_RIGHT,pygame.K_6,pygame.K_d):
                    welcome_screen()
            if event.type == pygame.QUIT:
                map_view_var = False

        pygame.display.update()
    pygame.quit()

def camera_view():
    global new_press, battery_max, battery_reset_event
    pygame.display.set_caption('Camera')
    testtext3 = font.render('camera',True,'black')
    camera_var = True
    while camera_var:
        timer.tick(fps)
        screen.fill('purple')
        screen.blit(testtext3,(200,200))

        test_button1 = Button('battery toggle 5',400,200,20,True)
        test_button2 = Button('battery toggle 4',700,200,20,True)
        test_button3 = Button('battery toggle 3',1000,200,20,True)

        if pygame.mouse.get_pressed()[0] and new_press:
            new_press = False
            if test_button1.check_click():
                battery_max = 5
                battery_reset_event = True
            elif test_button2.check_click():
                battery_max = 4
                battery_reset_event = True
            elif test_button3.check_click():
                battery_max = 3
                battery_reset_event = True

        if not pygame.mouse.get_pressed()[0] and not new_press:
            new_press = True

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
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

        sonar_button = invButton(192,88,232,65,play_surface,0,True)
        power_button = invButton(488,88,232,65,play_surface,0,True)
        pda_button = invButton(768,88,232,65,play_surface,0,True)

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
                    main_view()
                elif event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
                    map_view()
            if event.type == pygame.QUIT:
                play_run = False
        

        pygame.display.update()
    pygame.quit()

def sonar_screen():
    global new_press
    pygame.display.set_caption('Sonar')
    sonar_run = True
    while sonar_run:
        timer.tick(fps)
        if sonar_check_status:
            screen.blit(sonar_bg,sonar_bg_rect)
            screen.blit(sonar_surface,(0,0))
        else:
            screen.blit(sonar_offline_bg,sonar_offline_bg_rect)
            screen.blit(sonar_surface,(0,0))

        power_button = invButton(488,88,232,65,sonar_surface,0,True)
        pda_button = invButton(768,88,232,65,sonar_surface,0,True)

        if pygame.mouse.get_pressed()[0] and new_press:
            new_press = False
            if power_button.invcheck_Click():
                power_screen()
            elif pda_button.invcheck_Click():
                pda_screen()

        if not pygame.mouse.get_pressed()[0] and not new_press:
            new_press = True

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP,pygame.K_8,pygame.K_w):
                    main_view()
                elif event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
                    map_view()
            if event.type == pygame.QUIT:
                sonar_run = False
        pygame.display.update()
    pygame.quit()

def power_screen():
    global new_press, wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, radio_check_status, lights_check_status,wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, radio_check_enabled, lights_check_enabled, battery_stack, battery_dict, battery_max, battery_reset_event

    if battery_reset_event:
        wheels_check_status, sonar_check_status, ls_check_status, camera_check_status, radio_check_status, lights_check_status = False,False,True,False,False,False
        wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, radio_check_enabled, lights_check_enabled = True,True,True,True,True,True
        battery_stack = [1]
        battery_dict = {'wheels':False,'sonar':False,'ls':True,'camera':False,'radio':False,'lights':False}
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
                screen.blit(battery_img0,(213,230))
            elif len(battery_stack) == 5:
                screen.blit(battery_img1,(213,230))
            elif len(battery_stack) == 4:
                screen.blit(battery_img2,(213,230))
            elif len(battery_stack) == 3:
                screen.blit(battery_img3,(213,230))
            elif len(battery_stack) == 2:
                screen.blit(battery_img4,(213,230))
            elif len(battery_stack) == 1:
                screen.blit(battery_img5,(213,230))
            elif len(battery_stack) == 0:
                screen.blit(battery_img6,(213,230))
        elif battery_max == 5:
            if len(battery_stack) == 5:
                screen.blit(battery_img0,(213,230))
            elif len(battery_stack) == 4:
                screen.blit(battery_img1,(213,230))
            elif len(battery_stack) == 3:
                screen.blit(battery_img2,(213,230))
            elif len(battery_stack) == 2:
                screen.blit(battery_img3,(213,230))
            elif len(battery_stack) == 1:
                screen.blit(battery_img4,(213,230))
            elif len(battery_stack) == 0:
                screen.blit(battery_img5,(213,230))
        elif battery_max == 4:
            if len(battery_stack) == 4:
                screen.blit(battery_img0,(213,230))
            elif len(battery_stack) == 3:
                screen.blit(battery_img1,(213,230))
            elif len(battery_stack) == 2:
                screen.blit(battery_img2,(213,230))
            elif len(battery_stack) == 1:
                screen.blit(battery_img3,(213,230))
            elif len(battery_stack) == 0:
                screen.blit(battery_img4,(213,230))
        elif battery_max == 3:
            if len(battery_stack) == 3:
                screen.blit(battery_img0,(213,230))
            elif len(battery_stack) == 2:
                screen.blit(battery_img1,(213,230))
            elif len(battery_stack) == 1:
                screen.blit(battery_img2,(213,230))
            elif len(battery_stack) == 0:
                screen.blit(battery_img3,(213,230))
        elif battery_max == 2:
            if len(battery_stack) == 2:
                screen.blit(battery_img0,(213,230))
            elif len(battery_stack) == 1:
                screen.blit(battery_img1,(213,230))
            elif len(battery_stack) == 0:
                screen.blit(battery_img2,(213,230))
        elif battery_max == 1:
            if len(battery_stack) == 1:
                screen.blit(battery_img0,(213,230))
            elif len(battery_stack) == 0:
                screen.blit(battery_img1,(213,230))
        
        if len(battery_stack) == battery_max:
            wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, radio_check_enabled, lights_check_enabled = battery_dict['wheels'],battery_dict['sonar'],battery_dict['ls'],battery_dict['camera'],battery_dict['radio'],battery_dict['lights']
        else:
            wheels_check_enabled, sonar_check_enabled, ls_check_enabled, camera_check_enabled, radio_check_enabled, lights_check_enabled = True,True,True,True,True,True
        sonar_button = invButton(192,88,232,65,power_surface,0,True)
        pda_button = invButton(768,88,232,65,power_surface,0,True)

        wheels_check = powerButtons('WHEELS',625,240,wheels_check_enabled,wheels_check_status,64)
        sonar_check = powerButtons('SONAR',625,280,sonar_check_enabled,sonar_check_status,68)
        ls_check = powerButtons('LIFE SUPPORT',625,320,ls_check_enabled,ls_check_status,38)
        camera_check = powerButtons('CAMERA',625,360,camera_check_enabled,camera_check_status,62)
        radio_check = powerButtons('RADIO',625,400,radio_check_enabled,radio_check_status,70)
        lights_check = powerButtons('LIGHTS',625,440,lights_check_enabled,lights_check_status,66)

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

            if radio_check.textcheck_click():
                if radio_check_status == False and len(battery_stack) <= 6:
                    radio_check_status = True
                    battery_stack.append(1)
                    battery_dict['radio'] = True
                else:
                    radio_check_status = False
                    battery_stack.pop()
                    battery_dict['radio'] = False

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
                    main_view()
                elif event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
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

        sonar_button = invButton(192,88,232,65,pda_surface,0,True)
        power_button = invButton(488,88,232,65,pda_surface,0,True)

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
                    main_view()
                elif event.key in (pygame.K_LEFT,pygame.K_4,pygame.K_a):
                    map_view()
            if event.type == pygame.QUIT:
                pda_run = False
        pygame.display.update()
    pygame.quit()

def notice_board_view():
    global new_press
    pygame.display.set_caption('Notice Board')
    testtext5 = font.render('notice board view',True,'white')

    notice_board_var = True
    while notice_board_var:
        timer.tick(fps)
        screen.fill('dark blue')
        screen.blit(testtext5,(200,200))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT,pygame.K_6,pygame.K_d):
                    main_view()
            if event.type == pygame.QUIT:
                notice_board_var = False

        pygame.display.update()
    pygame.quit()

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
main_view()

'''
TASKS:
* [DONE] UPDATE THE POWER MENU - CREATE CLICKABLE OPTIONS FOR (Wheels, Sonar, Life Support, Camera, Radio, Lights)
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
* ADJUST THE BATTERY SO THAT:
    [DONE] THE TOTAL AVAILABLE BATTERY LEVEL CAN DECREASE (available power can go down as the game progresses)
    [DONE] THE BATTERY STACK RESETS WHEN MAX AVAILABLE BATTERY GOES DOWN, AND THAT LIFE SUPPORT IS ON BY DEFAULT
    [DONE] THE BUTTONS CANNOT BE ACTIVATED AND GET DISABLED IF THE BATTERY STACK IS FULL
* ADD INDICATORS THAT POP UP ONLY AT THE START OF THE GAME TO SHOW WHAT THE CONTROLS ARE
* TEST OUT ADDING THE ENTIRE GAME WITHIN ANOTHER FUNCTION SO THAT EXTERNAL EFFECTS LIKE FADING AND CONTROL INDICATORS ONLY POP UP FOR A CERTAIN TIME
* REDO AND ANIMATE THE TITLE SCREEN IMAGE AND BUTTON LAYOUTS (visual effects on press can be done later)
* DECORATE THE NOTICE BOARD AND CAMERA VIEWS, THEN ADD AND TEST NOTICE BOARD FUNCTIONALITY EITHER THROUGH POP-UPS OR THROUGH WRITTEN TEXT FOR GAME CONTROLS AND OBJECTIVES
'''