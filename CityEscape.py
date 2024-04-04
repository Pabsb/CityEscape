import pygame, random, sys, os
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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 191, 0)
RED = (191, 0, 0)

game_dir = os.path.dirname(__file__)
assets_dir = os.path.join(game_dir,"assets")
img_dir = os.path.join(assets_dir,"images")
snd_dir = os.path.join(assets_dir,"sounds")

pygame.init()
window = pygame.display.set_mode((960, 640))
pygame.display.set_caption("City Escape")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join(img_dir, 'DP_still.png')).convert()
        self.imgs = [pygame.transform.scale_by(img, sprite_scl)]
        for i in range(3):
            img = pygame.image.load(os.path.join(img_dir, 'DP_walk_left{}.png'.format(i))).convert()
            self.imgs.insert(0,pygame.transform.scale_by(img, sprite_scl))
            img = pygame.image.load(os.path.join(img_dir,'DP_walk_right{}.png'.format(i))).convert()
            self.imgs.append(pygame.transform.scale_by(img, sprite_scl))
        for img in self.imgs:
            img.set_colorkey(WHITE)
        self.state = [3, 0]
        self.image = self.imgs[self.state[0]]
        self.rect = self.image.get_rect()
        self.offset = 14
        r = self.rect
        self.hitbox = pygame.Rect(r.x + r.w * 0.33, r.y + r.h * 0.14, r.w * 0.34, r.w * 0.68)
        self.hitbox.center = (window.get_width() / 2, floor-self.hitbox.h / 2)
        self.rect.center = (self.hitbox.centerx, self.rect.centery - self.offset)
        self.speed_x = 0
        self.speed_y = 0
        self.last_step = 0
        self.last_jump = 0
    def update(self):
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
            elif now-self.last_step > delay:
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
        if self.hitbox.right > window.get_width():
            self.hitbox.right = window.get_width()
        if self.hitbox.left < 0:
            self.hitbox.left = 0
        if self.hitbox.bottom > floor:
            self.hitbox.bottom = floor
            self.speed_y = 0
        if self.hitbox.top < 0:
            self.hitbox.top = 0
        self.rect.center = self.hitbox.center
        self.rect.centery -= self.offset

class Mob(pygame.sprite.Sprite):
    def __init__(self,tag):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join(img_dir, '{}_still.png'.format(tag))).convert()
        self.imgs = [pygame.transform.scale_by(img, sprite_scl)]
        for i in range(2):
            img = pygame.image.load(os.path.join(img_dir, '{}_walk_left{}.png'.format(tag, i))).convert()
            self.imgs.insert(0,pygame.transform.scale_by(img, sprite_scl))
            img=pygame.image.load(os.path.join(img_dir, '{}_walk_right{}.png'.format(tag, i))).convert()
            self.imgs.append(pygame.transform.scale_by(img, sprite_scl))
        for img in self.imgs:
            img.set_colorkey(WHITE)
        self.state = [2]
        self.image = self.imgs[self.state[0]]
        self.rect = self.image.get_rect()
        self.offset = 14
        r = self.rect
        self.hitbox = pygame.Rect(r.x + r.w * 0.33, r.y + r.h * 0.14, r.w * 0.34, r.w * 0.68)
        self.hitbox.center = (window.get_width() / 2, floor-self.hitbox.h / 2)
        self.rect.center = (self.hitbox.centerx, self.rect.centery-self.offset)
        self.speed_x = 0
        self.speed_y = 0
        self.walking = 0
        self.last_jump = 0
        self.last_step = 0
    def move(self, dx, dy):
        self.hitbox.x += dx
        self.hitbox.y += dy
        if self.hitbox.right > window.get_width():
            self.hitbox.right = window.get_width()
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
        now = pygame.time.get_ticks()
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
        elif self.walking < 0 and now-self.last_step > delay:
            self.state[0] = (self.state[0] + 1) % 2
        elif self.walking > 0 and now-self.last_step > delay:
            self.state[0] = self.state[0] % 2 + 3
        self.speed_x = self.walking * player_speed
        if self.hitbox.bottom < floor:
            self.speed_y += gravity
        elif now-self.last_jump > 2 * delay and rand == 1:
            self.speed_y = -player_jump_strength
            self.last_jump = now
        self.image = self.imgs[self.state[0]]
        self.move(self.speed_x, self.speed_y)

def createMob(tag):
    mob = Mob(tag)
    game_sprites.add(mob)
    mob_sprites.add(mob)

def gameExit():
    pygame.quit()
    sys.exit()

train_dir = 0
player_dir = 0
bg0_img0 = pygame.image.load(os.path.join(img_dir,"tunnel.png")).convert()
bg_scl0 = window.get_height() / bg0_img0.get_rect().h
bg0_img0 = pygame.transform.scale_by(bg0_img0, bg_scl0)
bg_rect0 = bg0_img0.get_rect()
bg_img1 = pygame.image.load(os.path.join(img_dir, "train.png")).convert()
bg_scl1 = window.get_height() / bg_img1.get_rect().h
bg_img1 = pygame.transform.scale_by(bg_img1, bg_scl1)
bg_img1.set_colorkey(WHITE)
bg_rect1 = bg_img1.get_rect()
bg0_x0 = -(bg_rect0.w-window.get_width()) / 2
bg0_x1 = bg_rect0.w + bg0_x0
bg0_img1 = bg0_img0.copy()
bg1_x = -(bg_rect1.w-window.get_width()) / 2

game_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
npc_list = ["MrRat", "MsNymph"]
createMob(random.choice(npc_list))
player = Player()
game_sprites.add(player)

running = True
while running:
    clock.tick(FPS)
    for event in EVENTS.get():
        if event.type == pygame.QUIT:
            gameExit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameExit()
    now = pygame.time.get_ticks()
    key_state = pygame.key.get_pressed()
    if any(key_state) and now - last_input > delay:
        last_input = pygame.time.get_ticks()
        if key_state[pygame.K_SPACE]:
            train_speed = 0
        if key_state[pygame.K_w]:
            train_speed += 1
        if key_state[pygame.K_s]:
            train_speed -= 1
    if window.get_width() - bg_rect1.w < bg1_x and key_state[pygame.K_d]:
        player_dir =- 1
    elif bg1_x < 0 and key_state[pygame.K_a]:
        player_dir = 1
    else:
        player_dir = 0
    if player_dir != 0:
        bg1_x += player_dir * player_speed
        mob_list = pygame.sprite.Group.sprites(mob_sprites)
        for mob in mob_list:
            mob.move(player_dir * player_speed,0)
    if train_speed !=0 :
        sign = -sign if 25 == random.randrange(0, 500) else sign
        ts = random.randrange(1, 20)
        train_speed = sign * ts
        print("->", sign, ts, train_speed)
        s = "train_speed=" + str(train_speed) + ", a"
        if train_speed > 0:
            a0 = (a0 - 1) if window.get_width() - bg_rect0.w < bg0_x0 else 10
            s = s + "0=" + str(a0) + " (i.e. " + ("no " if a0 != 10 else "") + "shift)"
            if window.get_width() - bg_rect0.w < bg0_x0:
                bg0_x0 -= train_speed
                bg0_x1 -= train_speed
            else:
                bg0_x1 = bg0_x0
                bg0_x0 = bg0_x1 + bg_rect0.w
        else:
            a1 = (a1 - 1) if bg0_x0 < 0 else 10
            s = s + "1=" + str(a1) + " (i.e. " + ("no " if a1 != 10 else "") + "shift)"
            if bg0_x0 < 0:
                bg0_x0 -= train_speed
                bg0_x1 -= train_speed
            else:
                bg0_x1 = bg0_x0
                bg0_x0 = bg0_x1 + bg_rect0.w
        print(s)
        train_speed = 0 if a0 == 0 or a1 == 0 else train_speed
    game_sprites.update()
    window.blit(bg0_img0, (bg0_x0, 0))
    window.blit(bg0_img1, (bg0_x1, 0))
    window.blit(bg_img1, (bg1_x, 0))
    game_sprites.draw(window)
    pygame.display.update()