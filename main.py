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
ORANGE = (255,165,0) # expansion color

"""
draw the screen buffer of polygons and stuff (not the screen bg though)
0 = nothing
1 = polygon
2 = line
3 = goal
4 = start
5 = expanded path
"""
# use with screenBuffer[columns-1][rows-1]
screenBuffer = [[0 for i in range(rows)] for j in range(columns)]  
def drawBuffer():
    for i in range(len(screenBuffer)):
        for j in range(len(screenBuffer[i])):
            if screenBuffer[i][j] == 1:
                pygame.draw.circle(screen,BLACK,(i,rows-j),4)

# add a line :)
def addLine(x1,y1,x2,y2):
    slope = (y2 - y1) / (x2 - x1)
    # draw for every x, with y calculated using slope
    for


# we run this bad boi once
def doAStar():
    print(":)")

running = True
while running:
    # poll exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw background, then shapes and lines, and update screen
    screen.fill(WHITE)
    drawBuffer()
    pygame.display.update()

pygame.quit()