import pygame
import math

pygame.init()

pygame.display.set_caption("Andrew's A* Search Visualization")

columns, rows = (640,480)
screen = pygame.display.set_mode((columns,rows))

WHITE = (255,255,255) # screen color
BLACK = (0,0,0) # polygon color
ORANGE = (255,165,0) # line color
GREEN = (0,255,0) # goal color
RED = (255,0,0) # start color

start = (20,40)
goal = (630,470)

polygon1 = [(40,40),(170,100),(170,200),(40,200)]
polygon2 = [(70,220),(140,230),(100,400)]
polygon3 = [(300,300),(400,240),(400,450),(200,400)]
polygon4 = [(600,20),(500,30),(550,150)]
polygon5 = [(500,420),(500,400),(550,400),(550,460)]
polygon6 = [(450,420),(470,270),(450,270)]
polygon7 = [(300,10),(450,10),(450,200),(300,200)]
polygon8 = [(610,300),(540,300),(500,340),(620,350)]
polygons = [polygon1,polygon2,polygon3,polygon4,polygon5,polygon6,polygon7,polygon8]
nodes = polygon1 + polygon2 + polygon3 + polygon4 + polygon5 + polygon6 + polygon7 + polygon8
nodes.append(goal)

def getLines():
    linesList = []
    for polygon in polygons:
        for index in range(len(polygon) - 1):
            linesList.append((polygon[index],polygon[index+1]))
    return linesList
lines = getLines()

# draw static field stuff using SDL & OpenGL's weird coordinate system
def drawField():
    for polygon in polygons:
        pygame.draw.polygon(screen,BLACK,polygon,3)
    pygame.draw.circle(screen,RED,start,4)
    pygame.draw.circle(screen,GREEN,goal,4)

def calculateDist(node1,node2):
    return math.sqrt((node2[0]-node1[0])**2 + (node2[1]-node1[1])**2)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def findNeighbors(currNode):
    neighbors = []
    """
    for every node, shoot a line to it;
    if it intersects with a polygon line, disregard it
    """
    for node in nodes:
        neighbors.append(node)
        for line in lines:
            if intersect((currNode[0],currNode[1]),(node[0],node[1]),line[0],line[1]):
                neighbors.pop()
                break
    return neighbors

returnedPath = []
def aStar():
    currNode = start
    while currNode != goal:
        for neighbor in findNeighbors(currNode):
            # go to goal if it's in clear sight
            if neighbor == goal:
                returnedPath.append(goal)
                currNode = goal
                break
            # else pick the node closest to goal
            else:
                if calculateDist(neighbor,goal) < calculateDist(currNode,goal):
                    currNode = neighbor

        returnedPath.append(currNode)

aStar()

# draw the returned path from A*
def drawLines():
    lastNode = start
    for node in returnedPath:
        pygame.draw.line(screen,ORANGE,lastNode,node,2)
        lastNode = node

running = True
while running:
    # poll exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw background, then shapes and lines, and update screen
    screen.fill(WHITE)
    drawField()
    drawLines()
    pygame.display.update()

pygame.quit()