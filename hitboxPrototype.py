import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
width,height=1280,720
window=pygame.display.set_mode((width,height))
pygame.display.set_caption("City Escape")

# Colors
white=(255,255,255)
grey=(127,127,127)
black=(0,0,0)
blue=(0,191,0)
#invisible=(225,225,225,0)

#useful constants
speed=5

# Define player class
class Player:
    def __init__(self,w,h):
        self.rect=pygame.Rect((width-w)//2,(height-h)//2,w,h)
        self.rect.center=(width//2,height//2)
        #self.color=white
        #self.v=pygame.Vector2()
        #self.v[:]=0,0
    def draw(self):
        #pygame.draw.rect(window,self.color,self.rect)
        pygame.draw.rect(window,white,self.rect)
    def move(self,dx,dy,walls):
        self.rect.x+=dx #self.v[0]
        self.rect.y+=dy #self.v[1]
        self.check_collisions()
        walls.check_collisions(self)
    def check_collisions(self):
        # check the border of the screen
        if self.rect.top<0:                 # top border of the window
            self.rect.top=0
        if self.rect.bottom>height:         # bottom border of the window
            self.rect.bottom=height
        if self.rect[0]<0:                  # left border of the window
            self.rect[0]=0;
        if width<self.rect[0]+self.rect[2]: # left border of the window
            self.rect[0]=width-self.rect[2]

class Walls:
    def __init__(self):
        self.values=[]
    def add(self,x,y,w,h):
        self.values.append(pygame.Rect(x,y,w,h))
    def draw(self):
        for i in range(len(self.values)):
            pygame.draw.rect(window,grey,self.values[i])
    def check_collisions(self,player):
        p=player.rect
        colliding=p.collidelistall(self.values) # find all wall collisions
        for wall_i in range(len(colliding)): # for each wall collision
            # determine the direction and distance needed to snap the outer edges together
            r=self.values[colliding[0]]
            to=[r.x-p.x-p.w,r.x+r.w-p.x,r.y-p.y-p.h,r.y+r.h-p.y] # distance to move to the [left, right, top, bottom] side of r
            dir=min(range(len(to)),key=lambda i:abs(to[i])) # which index of to holds the shortest distance
            # resolve collision
            if dir//2==0: # change to the x-coordinate needed
                p.x+=to[dir]
            else: # change to the x-coordinate needed
                p.y+=to[dir]

# initialize important variables
walls=Walls()
walls.add(50,100,100,400)
walls.add(650,100,100,400)
player=Player(40,80)

def main(walls,player):
    # setup
    clock=pygame.time.Clock()
    running=True
    # game loop
    while running:
        # end game
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        # get input
        keys=pygame.key.get_pressed()

        if keys[pygame.K_w]:
            player.move(0,-speed,walls)
        if keys[pygame.K_s]:
            player.move(0,speed,walls)
        if keys[pygame.K_d]:
            player.move(speed,0,walls)
        if keys[pygame.K_a]:
            player.move(-speed,0,walls)
        # Drawing
        window.fill(black)
        walls.draw()
        player.draw()
        #pygame.draw.aaline(WIN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main(walls,player)
