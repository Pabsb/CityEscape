# import modules for pygame template
import pygame, random, sys, os
# import event
import pygame.event as EVENTS

a0, a1, sign = -1, -1, 1
gravity = 5
player_speed = 7
player_jump_strength = 35
train_speed = 10
delay = 200
last_input = 0
sprite_scl = 3
floor = 572
sprite_activity = 1000
FPS = 60

# variables for commonly used colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 191, 0)
RED = (191, 0, 0)

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
winWidth = window.get_width()
winHeight = window.get_height()

# create a default player sprite for the game
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load images
        img = pygame.image.load(os.path.join(img_dir, 'DP_still.png')).convert()
        self.imgs = [pygame.transform.scale_by(img, sprite_scl)]
        for i in range(3):
            img = pygame.image.load(os.path.join(img_dir, 'DP_walk_left{}.png'.format(i))).convert()
            self.imgs.insert(0,pygame.transform.scale_by(img, sprite_scl))
            img = pygame.image.load(os.path.join(img_dir, 'DP_walk_right{}.png'.format(i))).convert()
            self.imgs.append(pygame.transform.scale_by(img, sprite_scl))
        for img in self.imgs:
            img.set_colorkey(WHITE)
        # set image (standing still at start)
        self.state = [3, 0] # standing still by default
        self.image = self.imgs[self.state[0]] # player sprite image
        self.rect = self.image.get_rect()
        # set hitbox
        self.offset = 14
        r = self.rect
        self.hitbox = pygame.Rect(r.x + r.w * 0.33, r.y + r.h * 0.14, r.w * 0.34, r.w * 0.68)
        self.hitbox.center = ( winWidth / 2, floor - self.hitbox.h / 2)
        self.rect.center = (self.hitbox.centerx, self.rect.centery - self.offset)
        # set default speed
        self.speed_x = 0
        self.speed_y = 0
        # times of last player events
        self.last_step = 0
        self.last_jump = 0
    # update per loop iteration
    def update(self):
        # check key presses
        now = pygame.time.get_ticks()
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speed_x = -player_speed
        elif key_state[pygame.K_RIGHT]:
            self.speed_x = player_speed
        else:
            self.speed_x = 0
        if self.hitbox.bottom < floor:
            self.speed_y += gravity
        elif now-self.last_jump > 2 * delay and key_state[pygame.K_UP]:
            self.speed_y = -player_jump_strength
            self.last_jump = now
        if self.speed_x > 0 or key_state[pygame.K_d]:
            if self.state[0] < 4:
                self.state = [4, 0]
            elif now-self.last_step > delay:
                self.last_step = now
                if self.state[1] % 4 < 2:
                    self.state[0] += 1
                else:
                    self.state[0] -= 1
                self.state[1] += 1
        elif self.speed_x < 0 or key_state[pygame.K_a]:
            if self.state[0] > 2:
                self.state = [2, 0]
            elif now - self.last_step > delay:
                self.last_step = now
                if self.state[1] % 4 > 1:
                    self.state[0] += 1
                else:
                    self.state[0] -= 1
                self.state[1] += 1
        elif self.speed_x == 0:
            self.state = [3, 0]
        self.image = self.imgs[self.state[0]]
        self.hitbox.x += self.speed_x
        self.hitbox.y += self.speed_y
        if self.hitbox.right > winWidth:
            self.hitbox.right = winWidth
        if self.hitbox.left < 0:
            self.hitbox.left = 0
        if self.hitbox.bottom > floor: #winHeight:
            self.hitbox.bottom = floor #winHeight
            self.speed_y = 0
        if self.hitbox.top < 0:
            self.hitbox.top = 0
        self.rect.center = self.hitbox.center
        self.rect.centery -= self.offset

# create a generic enemy sprite for the game - standard name is *mob*
class Mob(pygame.sprite.Sprite):
    def __init__(self, tag):
        pygame.sprite.Sprite.__init__(self)
        # set pristine original image for sprite object - random choice from list
        img = pygame.image.load(os.path.join(img_dir, '{}_still.png'.format(tag))).convert()
        self.imgs = [pygame.transform.scale_by(img, sprite_scl)]
        for i in range(2):
            img = pygame.image.load(os.path.join(img_dir, '{}_walk_left{}.png'.format(tag,i))).convert()
            self.imgs.insert(0,pygame.transform.scale_by(img, sprite_scl))
            img = pygame.image.load(os.path.join(img_dir, '{}_walk_right{}.png'.format(tag,i))).convert()
            self.imgs.append(pygame.transform.scale_by(img, sprite_scl))
        for img in self.imgs:
            img.set_colorkey(WHITE)
        self.state = [2]
        self.image = self.imgs[self.state[0]]
        self.rect = self.image.get_rect() # specify bounding rect for sprite
        # set hitbox
        self.offset = 14
        r = self.rect
        self.hitbox = pygame.Rect(r.x + r.w * 0.33, r.y + r.h * 0.14, r.w * 0.34, r.w * 0.68)
        self.hitbox.center = (winWidth / 2, floor - self.hitbox.h / 2)
        self.rect.center = (self.hitbox.centerx, self.rect.centery-self.offset)
        # set default speed
        self.speed_x = 0
        self.speed_y = 0
        self.walking = 0
        # times of last mob events
        self.last_jump = 0
        self.last_step = 0
    def move(self, dx, dy):
        self.hitbox.x += dx
        self.hitbox.y += dy
        if self.hitbox.right > winWidth:
            self.hitbox.right = winWidth
            self.walking = 0
        if self.hitbox.left < 0:
            self.hitbox.left = 0
            self.walking = 0
        if self.hitbox.bottom > floor:
            self.hitbox.bottom = floor
            self.speed_y = 0
        if self.hitbox.top < 0:
            self.hitbox.top = 0
        self.rect.center = self.hitbox.center
        self.rect.centery -= self.offset
    def update(self):
        # determine motion
        now = pygame.time.get_ticks()
        # walking
        if self.walking == 0:
            rand = random.randrange(0, sprite_activity)
            if rand < 10:
                if rand % 2 == 0:
                    self.walking = -1
                else:
                    self.walking = 1
        else:
            rand = random.randrange(0, sprite_activity // 5)
            if rand < 10:
                self.walking = 0
        if self.walking == 0:
            self.state = [2]
        elif self.walking < 0 and now - self.last_step > delay:
            self.state[0] = (self.state[0] + 1) % 2
        elif self.walking > 0 and now - self.last_step > delay:
            self.state[0] = self.state[0] % 2 + 3
        self.speed_x = self.walking * player_speed
        # jumping
        if self.hitbox.bottom < floor:
            self.speed_y += gravity
        elif now - self.last_jump > 2 * delay and rand == 1:
            self.speed_y = -player_jump_strength
            self.last_jump = now
        # executing motion
        self.image = self.imgs[self.state[0]]
        self.move(self.speed_x, self.speed_y)


# create a mob object
def createMob(tag):
    mob = Mob(tag)
    game_sprites.add(mob) # add to game_sprites group to get object updated
    mob_sprites.add(mob) # add to mob_sprites group - use for collision detection &c.

# define game quit and program exit
def gameExit():
    pygame.quit()
    sys.exit()

#Text output and render function
def textRender(surface, text, size, color, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
    textOL = font.render(text, True, BLACK)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRectOL = textOL.get_rect()
    textRect.center = x, y

    #Outline top left
    textRectOL.center = x - 2, y - 2
    surface.blit(textOL, textRectOL)

    #Outline bottom left
    textRectOL.center = x - 2, y + 2
    surface.blit(textOL, textRectOL)

    #Outline top right
    textRectOL.center = x + 2, y - 2
    surface.blit(textOL, textRectOL)

    #Outline bottom right
    textRectOL.center = x + 2, y + 2
    surface.blit(textOL, textRectOL)

    surface.blit(text, textRect)

# load graphics/images for the game
train_dir = 0
player_dir = 0
# background layer 1
bg0_img0 = pygame.image.load(os.path.join(img_dir, "tunnel.png")).convert()
bg_scl0 = winHeight / bg0_img0.get_rect().h
bg0_img0 = pygame.transform.scale_by(bg0_img0, bg_scl0)
bg_rect0 = bg0_img0.get_rect() # add rect for bg - helps locate background
#background layer 2
bg_img1 = pygame.image.load(os.path.join(img_dir, "train.png")).convert()
bg_scl1 = winHeight / bg_img1.get_rect().h
bg_img1 = pygame.transform.scale_by(bg_img1, bg_scl1)
bg_img1.set_colorkey(WHITE)
bg_rect1 = bg_img1.get_rect()
# background offsets
bg0_x0 = -(bg_rect0.w - winWidth) / 2
bg0_x1 = bg_rect0.w + bg0_x0
bg0_img1 = bg0_img0.copy()
bg1_x = -(bg_rect1.w - winWidth) / 2

# sprite groups - player and mob
game_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
# npcs
npc_list = ["MrRat", "MsNymph"]
createMob(random.choice(npc_list))
# player
player = Player() # create player object
game_sprites.add(player) # add an npc to game

running = True
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
            print(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            # check for ESCAPE key
            if event.key == pygame.K_ESCAPE:
                gameExit()
    now = pygame.time.get_ticks()
    key_state = pygame.key.get_pressed()
    # check keyboard events - keydown
    if any(key_state) and now - last_input > delay:
        last_input = pygame.time.get_ticks()
        # stop and start the train moving animation
        if key_state[pygame.K_SPACE]:
            train_speed = 0
            #train_dir=(train_dir+2)%3-1
        if key_state[pygame.K_w]:
            train_speed += 1
        if key_state[pygame.K_s]:
            train_speed -= 1
    # move second background layer (if necessary)
    # determine direction of motion and determine if it is allowed
    if winWidth - bg_rect1.w < bg1_x and key_state[pygame.K_d]:
        player_dir = -1
    elif bg1_x < 0 and key_state[pygame.K_a]:
        player_dir = 1
    else:
        player_dir = 0
    # move second background layer (if necessary)
    if player_dir != 0:
        bg1_x += player_dir * player_speed
        mob_list = pygame.sprite.Group.sprites(mob_sprites)
        for mob in mob_list:
            mob.move(player_dir * player_speed,0)
    # move first background layer
    if train_speed != 0:
        sign = -sign if 25 == random.randrange(0, 500) else sign
        ts = random.randrange(1, 20)
        train_speed = sign * ts
        print("->", sign, ts, train_speed)
        s = "train_speed=" + str(train_speed) + ", a"
        if train_speed > 0:
            a0 = (a0 - 1) if winWidth - bg_rect0.w < bg0_x0 else 10
            s = s + "0=" + str(a0) + " (i.e. " + ("no " if a0 != 10 else "") + "shift)"
            if winWidth - bg_rect0.w < bg0_x0:
                bg0_x0 -= train_speed
                bg0_x1 -= train_speed
            else:
                bg0_x1 = bg0_x0
        else:
            a1 = (a1 - 1) if bg0_x0 < 0 else 10
            s = s + "1=" + str(a1) + " (i.e. " + ("no " if a1 != 10 else "") + "shift)"
            if bg0_x0 < 0:
                bg0_x0 -= train_speed
                bg0_x1 -= train_speed
            else:
                bg0_x1 = bg0_x0
        print(s)
        train_speed = 0 if a0 == 0 or a1 == 0 else train_speed
    # 'updating' the game
    game_sprites.update() # update all game sprites
    # draw background layers
    window.blit(bg0_img0, (bg0_x0,0)) # layer 1
    window.blit(bg0_img1, (bg0_x1,0))  # layer 1
    window.blit(bg_img1, (bg1_x,0)) # layer 2
    game_sprites.draw(window) # draw all sprites to the game window

    winX = winWidth / 2
    winY = winHeight - 100
    test_text = "Hello there! This is a long text to check if wrap works"
    
	#Main text
    textRender(window, str(test_text), 32, WHITE, winX, winY)
    pygame.display.update() # update the display window...