# import modules for pygame template
import pygame, random, sys, os
# import event
import pygame.event as EVENTS

def to_do_list():
    s="""
    Problems:
    - ADD COMMENTS!!!!
    - mobs arent bound to the edge of the train cars                                       (fixed)
    - separate inputs for the different types of player movement                           (fixed)
    - train car goes a bit too far when the player walks all the way to the edge           (attempted) 
    potential optimizations/cleaning:
    - (medium/low priority) turn the background into a class (maybe?)                      (not started)
    additions:
    - (***MAXIMUM PRIORITY***)give the player a sanity meter                               (not started)  ***
    - (low priority) make the train multiple cars long                                     (not started)
      - (low priority) string several of the same train car image                          (not started)
      - (low priority) make a conductor car                                      
    - train station
      - should operate similar to the train car                                            (not started)
          - the exterior train car image replace the interior train car image              (not made)
          - the sky replaces the train tunnel image                                        ()
            - separate images depending on weather and day/night cycles (low priority)
            - sun object (low priority)
    - overworld 
        - should operate similar to the train car
          - the buildings replace the train car image
          - the sky replaces the train tunnel image
    - combat system
      - player vs mob?
    """
    print(s)
    return

# important variables
gravity=5
player_speed=7
player_jump_strength=35
max_train_speed=20
train_acceleration=5
delay=200
last_input=0
sprite_scl=3
floor=572
sprite_activity=1000

# variables for pygame window - space invaders vertical screen style
winWidth=960
winHeight=640
FPS=60

# variables for commonly used colours
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0,191,0)
RED=(191,0,0)

# game assets
game_dir=os.path.dirname(__file__)
assets_dir=os.path.join(game_dir,"assets") # relative path to assets dir
img_dir=os.path.join(assets_dir,"images") # relative path to image dir
snd_dir=os.path.join(assets_dir,"sounds") # relative path to music and sound effects dir

# initialise pygame settings and create game window
pygame.init()
window=pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("City Escape")
clock=pygame.time.Clock()

# create a default player sprite for the game
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load images
        img=pygame.image.load(os.path.join(img_dir,'DP_still.png')).convert()
        self.imgs=[pygame.transform.scale_by(img,sprite_scl)]
        for i in range(3):
            img=pygame.image.load(os.path.join(img_dir,'DP_walk_left{}.png'.format(i))).convert()
            self.imgs.insert(0,pygame.transform.scale_by(img,sprite_scl))
            img=pygame.image.load(os.path.join(img_dir,'DP_walk_right{}.png'.format(i))).convert()
            self.imgs.append(pygame.transform.scale_by(img,sprite_scl))
        for img in self.imgs:
            img.set_colorkey(WHITE)
        # set image (standing still at start)
        self.state=[3,0] # standing still by default
        self.image=self.imgs[self.state[0]] # player sprite image
        self.rect=self.image.get_rect()
        # set hitbox
        self.offset=14
        r=self.rect
        self.hitbox=pygame.Rect(r.x+r.w*0.33,r.y+r.h*0.14,r.w*0.34,r.w*0.68)
        self.hitbox.center=(winWidth/2,floor-self.hitbox.h/2)
        self.rect.center=(self.hitbox.centerx,self.rect.centery-self.offset)
        #pygame.draw.rect(self.image,RED,self.hitbox.copy().move(-self.rect.x,-self.rect.y),width=1)
        #self.hitbox=pygame.Rect(r.x+r.w*0.3,r.y+r.h*0.25,r.w*0.4,r.w*0.65)
        # set default speed
        self.speed_x=0
        self.speed_y=0
        # times of last player events
        self.last_step=0
        self.last_jump=0
        self.jump=0
    # update per loop iteration
    def update(self):
        # gravity
        if self.hitbox.bottom<floor:
            self.speed_y+=gravity
        # animate
        if player_dir==-1:
            if self.state[0]<4:
                self.state=[4,0]
            elif now-self.last_step>delay:
                self.last_step=now
                if self.state[1]%4<2:
                    self.state[0]+=1
                else:
                    self.state[0]-=1
                self.state[1]+=1
        elif player_dir==1:
            if self.state[0]>2:
                self.state=[2,0]
            elif now-self.last_step>delay:
                self.last_step=now
                if self.state[1]%4>1:
                    self.state[0]+=1
                else:
                    self.state[0]-=1
                self.state[1]+=1
        elif player_dir==0:
            self.state=[3,0]
        self.image=self.imgs[self.state[0]]
        # apply motion
        self.hitbox.x-=walk_mode*player_dir*player_speed #self.speed_x
        self.hitbox.y+=self.speed_y
        if self.hitbox.right>winWidth:
            self.hitbox.right=winWidth
        if self.hitbox.left<0:
            self.hitbox.left=0
        if self.hitbox.bottom>floor: #winHeight:
            self.hitbox.bottom=floor #winHeight
            self.speed_y=0
        if self.hitbox.top<0: # shouldn't be possible but just in case
            self.hitbox.top=0
        self.rect.center=self.hitbox.center
        self.rect.centery-=self.offset



# create a generic enemy sprite for the game - standard name is *mob*
class Mob(pygame.sprite.Sprite):
    def __init__(self,tag):
        pygame.sprite.Sprite.__init__(self)
        # set pristine original image for sprite object - random choice from list
        img=pygame.image.load(os.path.join(img_dir,'{}_still.png'.format(tag))).convert()
        self.imgs=[pygame.transform.scale_by(img,sprite_scl)]
        for i in range(2):
            img=pygame.image.load(os.path.join(img_dir,'{}_walk_left{}.png'.format(tag,i))).convert()
            self.imgs.insert(0,pygame.transform.scale_by(img,sprite_scl))
            img=pygame.image.load(os.path.join(img_dir,'{}_walk_right{}.png'.format(tag,i))).convert()
            self.imgs.append(pygame.transform.scale_by(img,sprite_scl))
        for img in self.imgs:
            img.set_colorkey(WHITE)
        self.state=[2]
        self.image=self.imgs[self.state[0]]
        self.rect=self.image.get_rect() # specify bounding rect for sprite
        # set hitbox
        self.offset=14
        r=self.rect
        self.hitbox=pygame.Rect(r.x+r.w*0.33,r.y+r.h*0.14,r.w*0.34,r.w*0.68)
        self.hitbox.center=(winWidth/2,floor-self.hitbox.h/2)
        self.rect.center=(self.hitbox.centerx,self.rect.centery-self.offset)
        #pygame.draw.rect(self.image,RED,self.hitbox,width=1)
        # set random start position
        #self.rect.x=0 # starting x-coordinate #random.randrange(winWidth-self.rect.width)
        #self.rect.y=0 # starting y-coordinate #random.randrange(winWidth-self.rect.height)
        # set default speed
        self.speed_x=0 #random.randrange(-3,3) # random speed along the x-axis
        self.speed_y=0 #random.randrange(1,7) # random speed along the y-axis
        self.walking=0
        # times of last mob events
        self.last_jump=0
        self.last_step=0
    def move(self,dx,dy):
        self.hitbox.x+=dx
        self.hitbox.y+=dy
        #if self.hitbox.right>:#winWidth:
        #    self.hitbox.right=winWidth
        #    self.walking=0
        #if self.hitbox.left<0:
        #    self.hitbox.left=0
        #    self.walking=0
        if self.hitbox.bottom>floor:
            self.hitbox.bottom=floor
            self.speed_y=0
        if self.hitbox.top<0:  # shouldn't be possible but just in case
            self.hitbox.top=0
        self.rect.center=self.hitbox.center
        self.rect.centery-=self.offset
    def update(self):
        # determine motion
        now=pygame.time.get_ticks()
        # walking
        if self.walking==0:
            rand=random.randrange(0,sprite_activity)
            if rand<10:
                if rand%2==0:
                    self.walking=-1
                else:
                    self.walking=1
        else:
            rand=random.randrange(0,sprite_activity//5)
            if rand<10:
                self.walking=0
        if self.walking==0:
            self.state=[2]
        elif self.walking<0 and now-self.last_step>delay:
            self.state[0]=(self.state[0]+1)%2
        elif self.walking>0 and now-self.last_step>delay:
            self.state[0]=self.state[0]%2+3
        self.speed_x=self.walking*player_speed
        # jumping
        if self.hitbox.bottom<floor:
            self.speed_y+=gravity
        elif now-self.last_jump>2*delay and rand==1:
            self.speed_y=-player_jump_strength
            self.last_jump=now
        # executing motion
        self.image=self.imgs[self.state[0]]
        self.move(self.speed_x,self.speed_y)

# create a mob object
def createMob(tag):
    mob=Mob(tag)
    game_sprites.add(mob) # add to game_sprites group to get object updated
    mob_sprites.add(mob) # add to mob_sprites group - use for collision detection &c.

# define game quit and program exit
def gameExit():
    pygame.quit()
    sys.exit()

# load graphics/images for the game
# background (2 layers)
train_speed,train_dir=0,1
player_dir=0
walk_mode=0
# background layer 1
bg0_img0=pygame.image.load(os.path.join(img_dir,"tunnel.png")).convert()
bg_scl0=winHeight/bg0_img0.get_rect().h
bg0_img0=pygame.transform.scale_by(bg0_img0,bg_scl0)
bg_rect0=bg0_img0.get_rect() # add rect for bg - helps locate background
# background layer 1 offsets
bg0_x0=-(bg_rect0.w-winWidth)/2 # starting x offset of the first background layer
bg0_x1=bg_rect0.w+bg0_x0
bg0_img1=bg0_img0.copy()
#background layer 2
bg_img1=pygame.image.load(os.path.join(img_dir,"train.png")).convert()
bg_scl1=winHeight/bg_img1.get_rect().h
bg_img1=pygame.transform.scale_by(bg_img1,bg_scl1)
bg_img1.set_colorkey(WHITE)
bg_rect1=bg_img1.get_rect()
# background layer 2 offsets
bg1_x=-(bg_rect1.w-winWidth)//2 # starting x offset of the second background layer

# sprite groups - player and mob
game_sprites=pygame.sprite.Group()
mob_sprites=pygame.sprite.Group()
# npcs
npc_list=["MrRat","MsCat","MsNymph","Chad","Kathy","Chicago","MrShrimp"]
createMob(random.choice(npc_list))
# player
player=Player() # create player object
game_sprites.add(player) # add an npc to game
key_state=None

running=True
# create game loop
while running:
    # check loop is running at set speed
    clock.tick(FPS)
    # 'processing' inputs (events)
    for event in EVENTS.get():
        # check click on window exit button
        if event.type==pygame.QUIT:
            gameExit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
        if event.type==pygame.KEYDOWN:
            # check for ESCAPE key
            if event.key==pygame.K_ESCAPE:
                gameExit()
    now=pygame.time.get_ticks()
    previous_key_state=key_state
    key_state=pygame.key.get_pressed()
    # check keyboard events - keydown
    if any(key_state):
        # controls for the train moving animation
        if now-last_input>delay:
            last_input=pygame.time.get_ticks()
            if key_state[pygame.K_e]: # accelerate train
                train_speed+=train_acceleration
            if key_state[pygame.K_q]: # decelerate train
                train_speed-=train_acceleration
            if key_state[pygame.K_w] and train_speed==0: # change train direction (only works if the train is stopped)
                #if previous_key_state is not None and previous_key_state[pygame.K_w]: # only executes one each time the key is pressed
                train_dir*=-1

    if key_state[pygame.K_d]:
        player_dir=-1
    elif key_state[pygame.K_a]:
        player_dir=1
    else:
        player_dir=0
    """
    if key_state[pygame.K_s] and now-player.last_jump>2*delay:
        player_speed_y=-player_jump_strength
        player.last_jump=now
    """
# move first background layer
    # confine train speed between zero an the speed limit
    if train_speed<0: # confines train to a non-negative speed
        train_speed=0
    if train_speed>max_train_speed: # confines train to a speed limit
       train_speed=max_train_speed
    # reposition background layer 1 image positions if required to cover the game window (two image leap frog thing)
    if (train_dir==1 and winWidth-bg_rect0.w>=bg0_x0) or (train_dir==-1 and bg0_x0>=0):
        bg0_x1=bg0_x0
        bg0_x0+=train_dir*bg_rect0.w
    # shift the background layer 1 images to simulate/show relative motion
    bg0_x0-=train_dir*train_speed
    bg0_x1-=train_dir*train_speed
# move second background layer (if necessary)
    # which animation mode
    if (winWidth-bg_rect1.w<bg1_x and player.rect.centerx>=winWidth/2) or (bg1_x<0 and player.rect.centerx<=winWidth/2):
        walk_mode=0
    else:
        walk_mode=1
    # move second background layer (if necessary)
    if player_dir!=0:
        if walk_mode==0:
            player_speed_x=0
            bg1_x+=player_dir*player_speed
            # prevent the train far from going to far
            if bg1_x>0:
                bg1_x=0
                walk_mode=1
            if winWidth-bg_rect1.w>bg1_x:
                bg1_x=winWidth-bg_rect1.w
                walk_mode=1
            mob_list=pygame.sprite.Group.sprites(mob_sprites)
            for mob in mob_list:
                mob.move(player_dir*player_speed,0)
        if walk_mode==1:
            player_speed_x=player_dir*player_speed

    #"""
# 'updating' the game
    # update all game sprites
    game_sprites.update()
    # draw background layers
    window.blit(bg0_img0,(bg0_x0,0)) # layer 1
    window.blit(bg0_img1,(bg0_x1,0)) # layer 1 (used to make the background mobile)
    window.blit(bg_img1,(bg1_x,0)) # layer 2
    # drawing the game sprites
    game_sprites.draw(window) # draw all sprites to the game window
    # reflecting changes in the game window
    pygame.display.update() # update the display window...

