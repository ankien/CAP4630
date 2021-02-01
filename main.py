import pygame

pygame.init()

pygame.display.set_caption("Andrew's A* Search Visualization")

columns, rows = (640,480)
screen = pygame.display.set_mode((columns,rows))

WHITE = (255,255,255) # screen color
BLACK = (0,0,0) # polygon color
YELLOW = (255,255,0) # line color
GREEN = (0,255,0) # goal color
RED = (255,0,0) # start color

start = (20,20)
goal = (630,470)

polygon1 = [(40,40),(170,100),(170,200),(40,200)]
polygon2 = [(70,220),(140,230),(100,400)]
polygon3 = [(300,300),(400,240),(400,450),(200,400)]
polygon4 = [(600,20),(500,30),(550,150)]
polygon5 = [(500,420),(500,400),(610,400),(610,460)]
polygon6 = [(450,420),(470,270),(450,270)]
polygon7 = [(300,10),(450,10),(450,200),(300,200)]
polygon8 = [(610,300),(540,300),(520,340),(540,370),(620,340)]
polygons = [polygon1,polygon2,polygon3,polygon4,polygon5,polygon6,polygon7,polygon8]

# draw static field stuff using SDL & OpenGL's weird coordinate system
def drawField():
    for polygon in polygons:
        pygame.draw.polygon(screen,BLACK,polygon,3)
    pygame.draw.circle(screen,RED,start,4)
    pygame.draw.circle(screen,GREEN,goal,4)

running = True
while running:
    # poll exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw background, then shapes and lines, and update screen
    screen.fill(WHITE)
    drawField()
    pygame.display.update()

pygame.quit()