import pygame
import random
import time
import math

def make_background(surface):
    #load images
    water = pygame.image.load('pirate/PNG/Default size/Tiles/tile_73.png').convert()
    tile_15 = pygame.image.load('pirate/PNG/Default size/Tiles/tile_15.png').convert_alpha()
    tile_19 = pygame.image.load('pirate/PNG/Default size/Tiles/tile_19.png').convert_alpha()
    tile_25 = pygame.image.load('pirate/PNG/Default size/Tiles/tile_25.png').convert_alpha()
    tile_66 = pygame.image.load('pirate/PNG/Default size/Tiles/tile_66.png').convert_alpha()
    tower_bottom = pygame.image.load('pirate/PNG/Default size/Tiles/tile_94.png').convert_alpha()
    tower_top = pygame.image.load('pirate/PNG/Default size/Tiles/tile_78.png').convert_alpha()
    tower = pygame.image.load('pirate/PNG/Default size/Tiles/tile_15.png').convert_alpha()
    print(water.get_width())
    print(water.get_height())

    # set dark pixels as transparent
    transparent = [tile_15, tile_19, tile_25, tile_66, tower_bottom, tower_top, tower]
    for x in transparent:
        x.set_colorkey((255,255,255))
        x.set_colorkey((0, 0, 0))

    #drawing the water (duplicaitng the image until it fills up screen)
    for x in range(0, surface.get_width(), water.get_width()):
        for y in range(0, surface.get_height(), water.get_height()):
            surface.blit(water,(x,y))

    #draw the sand
    for y in range(0, surface.get_height(), water.get_height()):
        surface.blit(tile_25, (0, y))

    for y in range(0, surface.get_height(), water.get_height()):
        surface.blit(tile_19, (tile_25.get_width()*.9, y))

    #drawing towers
    surface.blit(tower_top, (0,int(tile_19.get_height())))
    surface.blit(tower_bottom, (0, int(surface.get_height() - 2*tower_bottom.get_height())))
    for y in range(tower.get_height()*2, int(surface.get_height() - 2.9*tower.get_height())):
        surface.blit(tower, (0,y))

    #draw random obstacles
    #for _ in range(0, 5):
    #    x = random.randint(int(tile_19.get_width()*2), surface.get_width() - 64)
    #    y = random.randint(int(tile_19.get_width()*2), surface.get_height() - 64)
    #    surface.blit(tile_66,(x
def startscreen(background, words = "Raiders", words2 = "Click to Start"):
    # Screen dimensions
    scr_wid = 1000  # (px)
    scr_hgt = 600  # (px)

    # Create the screen
    scr = pygame.display.set_mode((scr_wid, scr_hgt))
    pygame.display.set_caption('Making a customized background')

    scr.blit(background, (0, 0))

    #makes the title word
    custom_font = pygame.font.Font('Black_Crayon.ttf', 128)
    text_title = custom_font.render(words, True, (255, 69, 0))
    scr.blit(text_title, ((scr.get_width() / 2 - text_title.get_width() / 2), (scr.get_height() / 2 - text_title.get_height() / 2) - 100))

    #makes the start word
    arial = pygame.font.SysFont('Arial', 32)
    text_start = arial.render(words2, True, (0,0,0))
    scr.blit(text_start, (scr.get_width() / 2 - text_start.get_width() / 2, (scr.get_height() / 2 - text_start.get_height() / 2) + 100))

    # Get the rectangle of the start text
    start_rect = text_start.get_rect(center=(scr.get_width() / 2, scr.get_height() / 2 + 100))
    pygame.draw.rect(scr, (255, 0, 0), start_rect, width=2)

    pygame.display.flip()

    # Plays the game when user clicks the play button
    waiting = True
    while waiting:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            # see if user presses the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_rect.collidepoint(event.pos):
                    waiting = False
    print('Running Game')
class Boat(pygame.sprite.Sprite):

    count = 0
    def __init__(self, scr, ship_type = 1):
        super().__init__()
        fname = f'pirate/PNG/Default size/Ships/ship ({ship_type}).png'
        self.oriboat_img = pygame.image.load(fname).convert_alpha()
        self.oriboat_img = pygame.transform.scale(self.oriboat_img, (int(self.oriboat_img.get_width()),int(self.oriboat_img.get_height())))
        self.rect = self.oriboat_img.get_rect()
        self.oriboat_img = pygame.transform.rotate(self.oriboat_img, 270)
        self.oriboat_img.set_colorkey((0,0,0))
        self.boat_x = scr.get_width()
        self.boat_y = random.randint(0,scr.get_height())
        self.up = False
        self.forward = False
        self.boat_xspeed = scr.get_width()/(random.randint(20,40)*60)
        self.boat_yspeed = scr.get_height()/(random.randint(20,40)*60)
        self.num_update_run = 0
        self.num_update_run2 = random.randint(200, 500)
        self.boat_hp = 2
        self.ship_type = ship_type
        self.boat_img = self.oriboat_img

        #unique identifier
        Boat.count += 1
        self.boat_id = Boat.count

        #damaged boat
        fdname = f'pirate/PNG/Default size/Ships/ship ({int(self.ship_type) + 6}).png'
        self.dmgboat_img = pygame.image.load(fdname).convert_alpha()
        self.dmgboat_img = pygame.transform.scale(self.dmgboat_img,(int(self.dmgboat_img.get_width()), int(self.dmgboat_img.get_height())))
        self.rect = self.dmgboat_img.get_rect()
        self.dmgboat_img = pygame.transform.rotate(self.dmgboat_img, 270)
        self.dmgboat_img.set_colorkey((0, 0, 0))


    def update_pos(self, scr, multiplier):

        lower_boundspd = int(20 - multiplier)
        upper_boundspd = int(40 - multiplier)

        #increment
        self.num_update_run += 1
        if (self.num_update_run >= self.num_update_run2):
            self.up = not self.up
            #self.forward = not self.forward
            self.num_update_run2 = random.randint(200,1000)
            self.boat_xspeed = scr.get_width() / (random.randint(lower_boundspd, upper_boundspd) * 60)
            self.boat_yspeed = scr.get_height() / (random.randint(lower_boundspd, upper_boundspd) * 60)
            self.num_update_run = 0


        # update boat position
        if self.forward:
            self.boat_x += self.boat_xspeed
        else:
            self.boat_x -= self.boat_xspeed
        if self.up:
            self.boat_y -= self.boat_yspeed
        else:
            self.boat_y += self.boat_yspeed


        # check position of the boat
        if self.boat_y > (scr.get_height() - self.boat_img.get_height()):
            self.up = True
        if self.boat_y < 0:
            self.up = False


        # draws the Boat
        arial = pygame.font.SysFont('Arial', 16)
        text_hp = arial.render(f"{self.boat_hp}", True, (0, 0, 0))
        scr.blit(text_hp, (self.boat_x,self.boat_y))
        scr.blit(self.boat_img, (self.boat_x, self.boat_y))

    def get_boatx(self):
        return(self.boat_x)

    def get_boaty(self):
        return(self.boat_y)

    def bullet_hit_boat(self):
        self.boat_hp -= 1

    def check_hp(self):
        # updates boat based on HP
        if self.boat_hp == 2:

            return(False)
        if self.boat_hp == 1:
            self.boat_img = self.dmgboat_img

            return(False)

        if self.boat_hp <= 0:
            return(True)

#ships = pygame.sprite.Group()

class Box():
    def __init__(self, scr, x,y):
        self.box_img = pygame.draw.rect(scr, (195,195,195),(x,y,40, 40), width = 2)
        scr.blit(self.box_img, (x,y))

class Tank(pygame.sprite.Sprite):
    def __init__(self, scr, cannon_type = "blue"):
        super().__init__()

        fname = f'tanksA/PNG/Default size/tank_{cannon_type}.png'
        self.tank_img = pygame.image.load(fname).convert_alpha()
        self.tank_img = pygame.transform.rotate(self.tank_img,90)
        self.rect = self.tank_img.get_rect()
        self.tank_x = 20
        self.tank_y = int(scr.get_height()/2)

        #bullets
        self.bullet_img = pygame.image.load("tanksA/PNG/Default size/bulletBlue1.png").convert_alpha()
        self.bullet_x = -100
        self.bullet_y = 0
        self.bullet_rect = 0
        self.bullet_xspd = 1
        self.bullet_yspd = 1
        self.bullet_multiplier = 1000
        self.mouse_x = 0
        self.mouse_y = 0

        # Keys.
        self.key_up = 'not pressed'
        self.bullet_fired = False

    def update_bullet_pos(self, scr, events, boats):
        for event in events:

            # see if user presses a key
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('bullet fired!')
                if self.bullet_fired == False:
                    self.bullet_x = self.tank_x
                    self.bullet_y = self.tank_y
                    mouse_xy = pygame.mouse.get_pos()
                    self.mouse_x = mouse_xy[0]
                    self.mouse_y = mouse_xy[1]

                    #calculate hypotenuse to get angle of bullet
                    hypontenuse = math.sqrt((self.mouse_x - self.tank_x) ** 2 + (self.mouse_y - self.tank_y) ** 2)

                    #calculate angle and then rotate bullet in that direction.
                    theta = -1*(90+(100*math.atan((self.mouse_y - self.tank_y)/(self.mouse_x - self.tank_x))))

                    self.bullet_img = pygame.transform.rotate(self.bullet_img, theta)
                    print(theta)

                    self.bullet_fired = True

        hypontenuse = math.sqrt((self.mouse_x - self.tank_x)**2 + (self.mouse_y - self.tank_y)**2)


        self.bullet_xspd = (self.mouse_x - self.tank_x)*10 / hypontenuse
        self.bullet_yspd = (self.mouse_y - self.tank_y)*10 / hypontenuse

        # Update bullet position.
        self.bullet_x += self.bullet_xspd
        self.bullet_y += self.bullet_yspd

        #updates the bullet rect
        self.bullet_rect = pygame.Rect(self.bullet_x, self.bullet_y, self.bullet_img.get_width(), self.bullet_img.get_height())
        pygame.draw.rect(scr, (255, 0, 0), self.bullet_rect, width=1)

        #check for collusions

        offscreen = False
        if self.bullet_fired:
            offscreen = (int(self.bullet_x < 0) or int(self.bullet_x) > scr.get_width()) or (int(self.bullet_y) < 0 or int(self.bullet_y) > scr.get_height())

        boats_rect = []

        for shipss in boats:
            boats_rect.append(pygame.Rect(shipss.get_boatx()+20, shipss.get_boaty()+10, 70, 40))
            pygame.draw.rect(scr,(255,0,0),pygame.Rect(shipss.get_boatx()+20, shipss.get_boaty()+10, 70, 40), width=1)

        ship_hit = len(self.bullet_rect.collidelistall(boats_rect)) > 0

        for shipss in boats:
            if ship_hit:
                num = self.bullet_rect.collidelistall(boats_rect)[0]
                print(num)
                boats[num].bullet_hit_boat()
                ship_hit = False

        if offscreen or ship_hit:
            #print("hit")

            #reset bullet
            self.bullet_fired = False
            self.bullet_img = pygame.image.load("tanksA/PNG/Default size/bulletBlue1.png").convert_alpha()

        # Update screen.
        if self.bullet_fired:
            scr.blit(self.bullet_img, (self.bullet_x, self.bullet_y))


    def draw_tank(self,scr):
        scr.blit(self.tank_img, (self.tank_x,self.tank_y))


