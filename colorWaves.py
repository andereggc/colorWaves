import pygame, math, sys, random
pygame.init() # initializing the constructor

# colors used globally
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TRANS = (1, 1, 1)
flow = False  # controls type of color flow
width = 900  
height = 600  # windows dimensions
screen = pygame.display.set_mode((width, height)) 

class Gradient():
    def __init__(self, palette, maximum):
        # constructor
        self.COLORS = palette # the colors used in the gradient
        self.N = len(self.COLORS) # amount of colors used
        self.SECTION = maximum // (self.N - 1)  # maximum (width) // amount of colors -1

    def gradientMaker(self, color):
        # returns a smooth color gradient with the list self.COLORS
        i = color // self.SECTION
        fraction = (color % self.SECTION) / self.SECTION
        c1 = self.COLORS[i % self.N]
        c2 = self.COLORS[(i+1) % self.N]
        col = [0, 0, 0] 
        for k in range(3): # creating the gradient
            col[k] = (c2[k] - c1[k]) * fraction + c1[k]

        return col

class Slider():
    def __init__(self, val, maxi, mini, pos):
        # constructor
        self.val = val  # slider's position
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = pos  # x-location on screen
        self.ypos = 550 # y-location
        self.surf = pygame.surface.Surface((100, 50))
        self.hit = False  # indicates slider movement due to mouse interaction

        pygame.draw.rect(self.surf, GREY, [0, 0, 100, 50], 3) # button outline
        pygame.draw.rect(self.surf, WHITE, [10, 30, 80, 5], 0) # line slider is on

        # dynamic graphics - button surface, outline, slider, background at the bottom of the screen
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(TRANS)  
        self.button_surf.set_colorkey(TRANS) 
        pygame.draw.circle(self.button_surf, WHITE, (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, ORANGE, (10, 10), 4, 0)

    def draw(self):
        #Uses a combination of static and dynamic graphics over a copy of the screen to draw the waves

        # static
        surf = self.surf.copy() # creates copy of surface

        # dynamic
        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33) # creates (x,y) variable
        self.button_rect = self.button_surf.get_rect(center=pos) # gets a rectangle from position pos
        surf.blit(self.button_surf, self.button_rect) # displays slider boxes
        self.button_rect.move_ip(self.xpos, self.ypos)  # moves slider boxes to correct screen position

        # screen
        screen.blit(surf, (self.xpos, self.ypos))

    def move(self):
        # dynamically reacts to movement of the slider button.
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini # gets current value of slider
        if self.val < self.mini:
            self.val = self.mini # keeps slider within confines of min/max value
        if self.val > self.maxi:
            self.val = self.maxi

def wave(num, spaceBtwn, waveLength, sep, hgt, circSize, skew, xcolor):
    # the basic calculating and drawing function. The function uses slider values to variate the output.
    for x in range(0, width+10, int(spaceBtwn.val)): # x increases by spaceBtwn value each loop
        # calculations 
        ang_1 = (x + num) * math.pi * waveLength.val / 180 # wavelength change
        ang_2 = ang_1 - sep.val # separation change
        cos_1 = math.cos(ang_1)
        cos_2 = math.cos(ang_2)

        y_1 = int(cos_1 * hgt.val) + 250 # changes the height
        y_2 = int(cos_2 * hgt.val) + 250

        radius_1 = int(circSize.val + math.sin(ang_1 + skew.val) * circSize.val / 2) # changes circleSize and skew
        radius_2 = int(circSize.val + math.sin(ang_2 + skew.val) * circSize.val / 2)

        # drawing 
        if radius_1 > radius_2:  # draw the smaller circle before the larger one
            pygame.draw.circle(screen, xcolor(int(x + width//2) + num * flow), (x, y_2), radius_2, 0)
            pygame.draw.circle(screen, xcolor(x + num * flow), (x, y_1), radius_1, 0)
        else:
            pygame.draw.circle(screen, xcolor(x + num * flow), (x, y_1), radius_1, 0)
            pygame.draw.circle(screen, xcolor(int(x + width//2) + num * flow), (x, y_2), radius_2, 0)

def mainSlider(sliderChoice, colorChoice):
    # main method in project. Contains two 2D arrays which are combined with the Gradient and Slider class and the 
    # wave function to create the moving waves and dynamic sliders.
    pygame.display.set_caption('Color Waves')
    colorList = [ # 2D array of color values
        [MAGENTA, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE], # rainbow
        [BLACK, (48,48,48), (82,82,82), (122,122,122), (175,175,175), (219,219,219), WHITE], # black and white
        [(255, 0, 208), (255, 0, 89), RED, (255, 60, 0), (255, 170, 0), (242, 255, 0)], # hot
        [(0,255,21), (0,255,110), (0,255,226), (0,247,255), (0,140,255), (0,42,255), (89,0,255), (162, 0, 255)] # cold
        # using individual RGB's here since they're not used anywhere else besides these palettes 
        ]
        
    slideRanges = [ # 2D array that changes style of slider choice
        [10, 1, 10, 200, 3, 3.14, 50], # default
        [15, 3, 20, 200, 4.3, 6, 150], # max
        [1, 0.2, 1, 20, 1.8, 0.3, 10], # min
        [8, 1.6, 10.5, 110, 3.05, 3.3, 80], # avg
        [random.randint(1,15), random.uniform(0.2,3), random.randint(1,20), # random
        random.randint(20,200), random.uniform(1.8,4.3), random.uniform(0.3,6), random.randint(10,150) ]
        ]

    xcolor = Gradient(colorList[colorChoice], width).gradientMaker # calls Gradient class and passes our color choice

    # we get these variables from the Slider class and pass them into our wave function
    # to create the color waves (except for speed which is used on the clock at bottom of this function)
    circSize = Slider(slideRanges[sliderChoice][0], 15, 1, 25)
    waveLength = Slider(slideRanges[sliderChoice][1], 3, 0.2, 150)
    spaceBtwn = Slider(slideRanges[sliderChoice][2], 20, 1, 275)
    hgt = Slider(slideRanges[sliderChoice][3], 200, 20, 400)
    skew = Slider(slideRanges[sliderChoice][4], 4.3, 1.8, 525)
    sep = Slider(slideRanges[sliderChoice][5], 6, 0.3, 650)
    speed = Slider(slideRanges[sliderChoice][6], 150, 10, 775)
    slides = [circSize, waveLength, spaceBtwn, hgt, skew, sep, speed] # creates array which moves our slider
    screen = pygame.display.set_mode((width, height)) # creates our screen
    clock = pygame.time.Clock()
    num = 0 # continuously increments while True
    while True:
        for event in pygame.event.get(): # any action from user
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # wave changes
                if event.key == pygame.K_1:
                    mainSlider(0, colorChoice)
                if event.key == pygame.K_2:
                    mainSlider(1, colorChoice)
                if event.key == pygame.K_3:
                    mainSlider(2, colorChoice)
                if event.key == pygame.K_4:
                    mainSlider(3, colorChoice)
                if event.key == pygame.K_5:
                    mainSlider(4, colorChoice)
                # color changes
                if event.key == pygame.K_6:
                    mainSlider(sliderChoice, 0)
                if event.key == pygame.K_7:
                    mainSlider(sliderChoice, 1)
                if event.key == pygame.K_8:
                    mainSlider(sliderChoice, 2)
                if event.key == pygame.K_9:
                    mainSlider(sliderChoice, 3)
                if event.key == pygame.K_SPACE:
                    main(sliderChoice, colorChoice) # goes back to main menu
            elif event.type == pygame.MOUSEBUTTONDOWN:  
                mouse = pygame.mouse.get_pos() # returns x,y coordinates
                for s in slides:  
                    if s.button_rect.collidepoint(mouse):
                        s.hit = True # allows slider to move
            elif event.type == pygame.MOUSEBUTTONUP: 
                for s in slides:
                    s.hit = False # stops slider from moving

        # Move slides
        for s in slides:
            if s.hit:
                s.move()

        # Updates screen, creates waves
        screen.fill(BLACK)
        num += 2 # continues to increment so wave's value will be changed
        wave(num, spaceBtwn, waveLength, sep, hgt, circSize, skew, xcolor) # creates waves
        for s in slides:
            s.draw() # draws slides

        label = pygame.font.SysFont("Verdana", 12) # font and color for slider's text
        txtColor = (255,116,3)
        circSizeBut = label.render("Circle Size ", True, txtColor) 
        waveLengthBut = label.render("Wavelength", True, txtColor)
        spaceBtwnBut = label.render("Space Between", True, txtColor)
        heightBut = label.render("Height ", True, txtColor)
        skewBut = label.render("Skew", True, txtColor)
        sepBut = label.render("Separation", True, txtColor)    
        speedBut = label.render("Speed", True, txtColor)
        # superimposing the text
        screen.blit(circSizeBut, (45, 555))
        screen.blit(waveLengthBut, (165, 555))
        screen.blit(spaceBtwnBut, (280, 555))
        screen.blit(heightBut, (430, 555))
        screen.blit(skewBut, (557, 555))
        screen.blit(sepBut, (667, 555))
        screen.blit(speedBut, (805, 555))
        pygame.display.flip() # updates screen
        clock.tick(speed.val) # speed changes the clock's tick

def main(sliderChoice, colorChoice):
    # main menu, explains program to user
    pygame.init() # initializing the constructor   
    pygame.display.set_caption("Main Menu")
    screen = pygame.display.set_mode((width,height)) # creates window 
    screen.fill(BLACK) # makes screen black
    title = pygame.font.SysFont('Georgia', 70)
    txt = pygame.font.SysFont('Verdana', 25) # font and color for text
    txtColor = (255,116,3) 
    titleCard = title.render("Cam's Color Waves", True, txtColor)
    info1 = txt.render('Press the SPACEBAR to start the program', True, txtColor) 
    info2 = txt.render('and click it again to return to this menu', True, txtColor) 
    info3 = txt.render('To select a preset, click the key while the program is running', True, txtColor) 
    wavDef = txt.render('1 = default', True, txtColor)
    wavMax = txt.render('2 = max', True, txtColor)
    wavMin = txt.render('3 = min', True, txtColor)
    wavAvg = txt.render('4 = avg', True, txtColor)
    wavRan = txt.render('5 = random', True, txtColor)
    colRain = txt.render('6 = rainbow', True, txtColor)
    colBW = txt.render('7 = black & white', True, txtColor)
    colHot = txt.render('8 = hot', True, txtColor)
    colCold = txt.render('9 = cold', True, txtColor)
    colPre = txt.render('COLOR PRESETS:', True, txtColor) 
    wavPre = txt.render('WAVE PRESETS:', True, txtColor) 
    # superimposing the text  
    screen.blit(info1, (185,160)) 
    screen.blit(info2, (185,190)) 
    screen.blit(info3, (50,280)) 
    screen.blit(wavPre, (160,340)) 
    screen.blit(colPre, (520,340)) 
    screen.blit(wavDef, (190, 370))
    screen.blit(wavMax, (190, 400))
    screen.blit(wavMin, (190, 430))
    screen.blit(wavAvg, (190, 460))
    screen.blit(wavRan, (190, 490))
    screen.blit(colRain, (550, 370))
    screen.blit(colBW, (550, 400))
    screen.blit(colHot, (550, 430))
    screen.blit(colCold, (550, 460))
    screen.blit(titleCard, (150, 60))  

    while True: 
        for event in pygame.event.get(): # any action from user
            if event.type == pygame.QUIT:
                pygame.quit()       
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mainSlider(sliderChoice, colorChoice) 
        pygame.display.update() # updates the frames of the game 
        
main(0,0) # default settings, starts program