import pygame
import math

pygame.init()
pygame.display.set_caption("Andrew's A* Search Visualization")

columns, rows = (1151,478)
screen = pygame.display.set_mode((columns,rows))

WHITE = (255,255,255) # screen color
BLACK = (0,0,0) # polygon color
ORANGE = (255,165,0) # line color
GREEN = (0,255,0) # goal color
RED = (255,0,0) # start color

start = (195,408); goal = (961,48)

polygon1 = [(227,458),(227,347),(580,347),(580,458)]
polygon2 = [(209,260),(330,290),(399,145),(318,31),(190,148)]
polygon3 = [(406,299),(501,301),(450,123)]
polygon4 = [(508,184),(508,45),(595,29),(659,97)]
polygon5 = [(597,245),(632,403),(705,332)]
polygon6 = [(678,275),(678,46),(825,46),(825,275)]
polygon7 = [(761,341),(841,288),(902,339),(902,428),(832,463),(761,420)]
polygon8 = [(845,74),(921,300),(941,85),(900,43)]
polygons = [polygon1,polygon2,polygon3,polygon4,polygon5,polygon6,polygon7,polygon8]
nodes = polygon1 + polygon2 + polygon3 + polygon4 + polygon5 + polygon6 + polygon7 + polygon8
nodes.append(goal)

def getLines():
    linesList = []
    for polygon in polygons:
        for index in range(len(polygon)):
            linesList.append((polygon[index],polygon[(index+1) % len(polygon)]))
    return linesList
lines = getLines()

# draw static field stuff using SDL & OpenGL's weird coordinate system
def drawField():
    for polygon in polygons:
        pygame.draw.polygon(screen,BLACK,polygon,3)
    pygame.draw.circle(screen,RED,start,4)
    pygame.draw.circle(screen,GREEN,goal,4)

# aka calculate h(n) for dist to goal, and g(n) for dist from currNode
# best path has the lowest h(n) + g(n)
def calculateDist(node1,node2):
    return math.sqrt((node2[0]-node1[0])**2 + ((rows-node2[1])-(rows-node1[1]))**2)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def notLine(currNode,node):
    for line in lines:
        if (line == (currNode,node)) or (line == (node,currNode)):
            return False
    return True

# because lines to nodes may overlap with node locations
def getOffset(p1,p2):
    if p1 > p2:
        return -1
    elif p1 == p2:
        return 0
    else:
        return 1

def findNeighbors(currNode):
    neighbors = []
    # for every node, shoot a line to it;
    # if it intersects with a polygon line, disregard it
    for node in nodes:
        neighbors.append(node)
        for line in lines:
            offsetX1 = getOffset(currNode[0],node[0])
            offsetY1 = getOffset(rows-currNode[1],rows-node[1])
            offsetX2 = getOffset(node[0],currNode[0])
            offsetY2 = getOffset(rows-node[1],rows-currNode[1])
            if intersect((currNode[0]+offsetX1,currNode[1]+offsetY1),(node[0]+offsetX2,node[1]+offsetY2),line[0],line[1]) and notLine(currNode,node):
                neighbors.pop()
                break
    return neighbors

# stores nodes we've already "expanded"
seenList = []
def aStar(currNode,currFn,currPath):
    global finalPath
    newPath = currPath + [currNode]
    neighbors = findNeighbors(currNode)
    neighborList = []
    shortestUnseenNeighbor = []
    smallestFn = 0
    for neighbor in neighbors:
        if neighbor == goal:
            newPath.append(neighbor)
            finalPath = newPath
            return
        newFn = currFn + calculateDist(currNode,neighbor) + calculateDist(neighbor,goal)
        if neighbor != currNode:
            neighborList.append([neighbor,newFn,newPath])

    for neighbor in neighborList:
        if (neighbor[1] < smallestFn) or (smallestFn == 0) and (neighbor[0] not in seenList):
            shortestUnseenNeighbor = neighbor
            smallestFn = neighbor[1]

    # A* the neighbor with the shortest f(n) that we haven't seen before
    seenList.append(shortestUnseenNeighbor[0])
    aStar(shortestUnseenNeighbor[0],shortestUnseenNeighbor[1],shortestUnseenNeighbor[2])

aStar(start,0,[])

# draw the shortest path from A*
def drawLines():
    lastNode = start
    for node in finalPath:
        pygame.draw.line(screen,ORANGE,lastNode,node,2)
        lastNode = node

running = True
while running:
    # poll exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw background, then shapes and lines, and update screen
    screen.fill(WHITE); drawField(); drawLines(); pygame.display.update()

pygame.quit()