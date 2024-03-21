# import modules for pygame template
import pygame, random, sys, os
# import event
import pygame.event as EVENTS

# important variables
player_speed = 5
train_speed = 10
is_train_moving = False
input_delay = 200
last_input = 0
sprite_scl = 3

# variables for pygame window - space invaders vertical screen style
FPS = 60

# variables for commonly used colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,191,0)
RED = (191,0,0)

# game assets
game_dir = os.path.dirname(__file__)
assets_dir = os.path.join(game_dir, "assets") # relative path to assets dir
img_dir = os.path.join(assets_dir, "images") # relative path to image dir
snd_dir = os.path.join(assets_dir, "sounds") # relative path to music and sound effects dir

# initialise pygame settings and create game window
pygame.init()
window = pygame.display.set_mode((960, 640))
pygame.display.set_caption("City Escape")
clock = pygame.time.Clock()

# create a default player sprite for the game
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load standing still image
        self.image = pygame.transform.scale_by(player_img,sprite_scl) # load and scale player sprite image
        self.image.set_colorkey(WHITE) # set colorkey to remove black background for player's rect
        self.rect = self.image.get_rect()
        self.rect.center = (window.get_width() / 2, window.get_height() / 2)
        # set hitbox
        print(self.rect)
        self.offset = 14
        r=self.rect
        self.hitbox = pygame.Rect(r.x+r.w*0.33,r.y+r.h*0.14,r.w*0.34,r.w*0.68)
        self.hitbox.center = self.rect.center
        self.hitbox.centery += self.offset
        #pygame.draw.rect(self.image,RED,self.hitbox.copy().move(-self.rect.x,-self.rect.y),width=1)
        #self.hitbox=pygame.Rect(r.x+r.w*0.3,r.y+r.h*0.25,r.w*0.4,r.w*0.65)
        # set default speed
        self.speed_x = 0
        self.speed_y = 0
    # update per loop iteration
    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        # check key presses
        key_state=pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:# or key_state[pygame.K_a]:
            self.speed_x = -5
        if key_state[pygame.K_RIGHT]:# or key_state[pygame.K_d]:
            self.speed_x = 5
        if key_state[pygame.K_UP]:# or key_state[pygame.K_w]:
            self.speed_y = -5
        if key_state[pygame.K_DOWN]:# or key_state[pygame.K_s]:
            self.speed_y = 5
        self.hitbox.x += self.speed_x
        self.hitbox.y += self.speed_y
        if self.hitbox.right > window.get_width():
            self.hitbox.right = window.get_width()
        if self.hitbox.left < 0:
            self.hitbox.left = 0
        if self.hitbox.bottom > window.get_height():
            self.hitbox.bottom = window.get_height()
        if self.hitbox.top < 0:
            self.hitbox.top = 0
        self.rect.center = self.hitbox.center
        self.rect.centery -= self.offset

# create a generic enemy sprite for the game - standard name is *mob*
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # set pristine original image for sprite object - random choice from list
        self.image_original = random.choice(npc_imgs)
        self.image_original.set_colorkey(WHITE)  # set colour key for original image
        self.image = pygame.transform.scale_by(self.image_original.copy(),sprite_scl) # set scaled copy image for sprite rendering
        self.rect = self.image.get_rect() # specify bounding rect for sprite
        # set hitbox
        r = self.rect
        self.hitbox = (r.x+r.w*0.3,r.y+r.h*0.24,r.w*0.4,r.w*0.65)
        #pygame.draw.rect(self.image,RED,self.hitbox,width=1)
        # set random start position
        self.rect.x = 0 # starting x-coordinate #random.randrange(window.get_width()-self.rect.width)
        self.rect.y = 0 # starting y-coordinate #random.randrange(window.get_width()-self.rect.height)
        # set default speed
        self.speed_x = 0 #random.randrange(-3,3) # random speed along the x-axis
        self.speed_y = 0 #random.randrange(1,7) # random speed along the y-axis
    def update(self):
        # move
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # check if enemy sprite leaves the bottom of the game window - then randomise at the top...
        #if self.rect.top>window.get_height()+15 or self.rect.left<-15 or self.rect.right>window.get_width()+15:

# create a mob object
def createMob():
    mob = Mob()
    game_sprites.add(mob) # add to game_sprites group to get object updated
    mob_sprites.add(mob) # add to mob_sprites group - use for collision detection &c.

# define game quit and program exit
def gameExit():
    pygame.quit()
    sys.exit()

# load graphics/images for the game
# background (2 layers)
# background layer 1
bg_img0 = pygame.image.load(os.path.join(img_dir, "tunnel.png")).convert()
bg_scl0 = window.get_height() / bg_img0.get_rect().h
bg_img0 = pygame.transform.scale_by(bg_img0,bg_scl0)
bg_rect0 = bg_img0.get_rect() # add rect for bg - helps locate background
#background layer 2
bg_img1 = pygame.image.load(os.path.join(img_dir, "train.png")).convert()
bg_scl1 = window.get_height() / bg_img1.get_rect().h
bg_img1 = pygame.transform.scale_by(bg_img1,bg_scl1)
bg_img1.set_colorkey(WHITE)
bg_rect1 = bg_img1.get_rect()
# background offsets
bg0_x = -(bg_rect0.w-window.get_width()) / 2 # starting x offset of the first background layer
bg1_x = -(bg_rect1.w-window.get_width()) / 2 # starting x offset of the second background layer
# player
player_img = pygame.image.load(os.path.join(img_dir, "mc.png")).convert()
# npcs
npc_imgs = []
npc_list = ["mrRat.png", "msNymph.png"]
for img in npc_list:
    npc_imgs.append(pygame.image.load(os.path.join(img_dir,img)).convert())

# sprite groups - game, mob, projectiles...
game_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
createMob() # create a new npc object
player = Player() # create player object
game_sprites.add(player) # add an npc to game

running=True
# create game loop
while running:
    # check loop is running at set speed
    clock.tick(FPS)
    # 'processing' inputs (events)
    for event in EVENTS.get():
        # check click on window exit button
        if event.type == pygame.QUIT:
            gameExit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            # check for ESCAPE key
            if event.key == pygame.K_ESCAPE:
                gameExit()
    now = pygame.time.get_ticks()
    key_state = pygame.key.get_pressed()
    # check keyboard events - keydown
    if any(key_state) and now-last_input>input_delay:
        last_input = pygame.time.get_ticks()
        # stop and start the train moving animation
        if key_state[pygame.K_SPACE]:
            is_train_moving = not is_train_moving
            print(bg0_x)
        if key_state[pygame.K_w]:
            train_speed += 1
        if key_state[pygame.K_s]:
            train_speed -= 1
    # move second background layer (if necessary)
    if window.get_width()-bg_rect1.w < bg1_x and key_state[pygame.K_a]:
        bg1_x -= player_speed
    if bg1_x < 0 and key_state[pygame.K_d]:
        bg1_x += player_speed
    # move first background layer
    if is_train_moving:
        if window.get_width() - bg_rect0.w < bg0_x < 0: #bg0_x-window.get_width()>-bg_rect0.w
            bg0_x -= train_speed
        else:
            bg0_x = (window.get_width() - bg_rect0.w) / 2
    # 'updating' the game
    game_sprites.update() # update all game sprites
    # draw background layers
    window.blit(bg_img0, (bg0_x,0)) # layer 1
    window.blit(bg_img1, (bg1_x,0)) # layer 2
    game_sprites.draw(window) # draw all sprites to the game window
    pygame.display.update() # update the display window...