from math import *
from random import *
import pygame

pygame.init()
pygame.display.set_caption("Andrew's RRT Visualization")

columns, rows = (1280,720)
screen = pygame.display.set_mode((columns,rows))

WHITE = (255,255,255) # screen color
BLACK = (0,0,0) # object color
GREY = (128,128,128) # tree color
ORANGE = (255,165,0) # tree path color
GREEN = (0,255,0) # goal color
RED = (255,0,0) # start color

testCase = int(input("Enter a test case type:\n0 - No Objects\n1 - Static Objects\n2 - 100x100\n3 - 200x200\n4 - 300x300\n"))

# global variables
goal = (961,48)
start = (195,408); startRadius = 5; goalRadius = 40
polygons = []
distance = 5 # increase for greater node traveling distance
polygonWidth = 4

def createRandomSquares(numOfShape, sideLength):
    for i in range(numOfShape):
        p1 = (randint(0,rows),randint(0,columns))
        p2 = (p1[0]+sideLength,p1[1])
        p3 = (p2[0],p1[1]+sideLength)
        p4 = (p1[0],p3[1])

        polygons.append([p1,p2,p3,p4])

def calculateDist(node1,node2):
    return sqrt((node2[0]-node1[0])**2 + ((rows-node2[1])-(rows-node1[1]))**2)

def nodeWithinDist(node,nodeWithRadius,radius):
    if calculateDist(nodeWithRadius,node) <= radius:
        return True
    return False

if testCase == 0:
    'do nothing'
elif testCase == 1:
    polygons.append([(227,458),(227,347),(580,347),(580,458)])
    polygons.append([(209,260),(330,280),(399,145),(318,31),(190,148)])
    polygons.append([(408,300),(500,300),(450,123)])
    polygons.append([(508,184),(508,45),(595,29),(659,97)])
    polygons.append([(597,245),(632,403),(705,332)])
    polygons.append([(678,275),(678,46),(825,46),(825,275)])
    polygons.append([(761,341),(841,288),(902,339),(902,428),(832,463),(761,420)])
    polygons.append([(845,74),(921,300),(941,85),(900,50)])
else:
    columns, rows = (100*testCase,100*testCase)
    screen = pygame.display.set_mode((columns,rows))
    distance = 3
    polygonWidth = 1*testCase
    start = (randint(0,columns),randint(0,rows))
    goalRadius = 10
    goal = (randint(0,columns),randint(0,rows))
    while nodeWithinDist(start,goal,goalRadius):
        goal = (randint(0,columns),randint(0,rows))
    createRandomSquares(5*testCase,8*testCase)

polygons.append([(0,0),(columns,0),(columns,rows),(0,rows)])

def getLines():
    linesList = []
    for polygon in polygons:
        for index in range(len(polygon)):
            linesList.append((polygon[index],polygon[(index+1) % len(polygon)]))
    return linesList
lines = getLines()

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def intersectsWithLine(node1,node2):
    for line in lines:
        if intersect((node1[0],rows-node1[1]),(node2[0],rows-node2[1]),(line[0][0],rows-line[0][1]),(line[1][0],rows-line[1][1])):
            return True
    return False

tree = {start:((0,0),(0,0))}
def nearestNeighbor(node):
    closestNeighborNode = ()
    shortestNeighborDist = 0
    for vertex in tree:
        neighborDist = calculateDist(vertex,node)
        if neighborDist < shortestNeighborDist or shortestNeighborDist == 0:
            closestNeighborNode = vertex; shortestNeighborDist = neighborDist
    return closestNeighborNode

def getSign(v1,v2):
    if v1 < v2:
        return 1
    elif v1 == v2:
        return 1
    else:
        return -1

def selectInput(rand,near):
    if(rand[0]-near[0]) != 0:
        m = ((rows-rand[1])-(rows-near[1])) / (rand[0]-near[0])
        ratio = distance / calculateDist(rand,near)
        offsetX = (1-ratio) * near[0] + ratio * rand[0]
        offsetY = (1-ratio) * near[1] + ratio * rand[1]
        return (offsetX,offsetY)
    return (0,0)

finalPath = []
def generateRRT(k):
    i = 0
    while i < k:
        xrand = (randint(0,1280),randint(0,720))
        xnear = nearestNeighbor(xrand)
        xnew = selectInput(xrand,xnear)
        # xnew cannot be existing vertex, or collide with polygon line
        if (xnew in tree) or intersectsWithLine(xnear,xnew):
            continue
        tree[xnew] = (xnear,xnew)
        # check if xnew is in the goal radius
        if nodeWithinDist(xnew,goal,goalRadius):
            finalPath.clear(); node = xnew
            while node != start:
                finalPath.append(node)
                node = tree[node][0]
            finalPath.append(start)
        i+=1
    return

# draw start, goal, and objects
def drawField():
    if testCase != 0:
        for i in range(len(polygons)):
            if i == len(polygons) - 1:
                pygame.draw.polygon(screen,WHITE,polygons[i],polygonWidth)
            else:
                pygame.draw.polygon(screen,BLACK,polygons[i],polygonWidth)
    pygame.draw.circle(screen,RED,start,startRadius)
    pygame.draw.circle(screen,GREEN,goal,goalRadius)

def drawTree():
    # draw grey line for every edge in tree
    for value in tree:
        pygame.draw.line(screen,GREY,tree[value][0],tree[value][1],2)
    # draw orange line for the shortest path in tree
    for i in range(len(finalPath) - 1):
        pygame.draw.line(screen,ORANGE,finalPath[i],finalPath[i+1],3)
    return

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            generateRRT(50) # change value for number of nodes generated on keypress

    screen.fill(WHITE); drawField(); drawTree(); pygame.display.update()

pygame.quit()