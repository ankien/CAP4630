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

testCase = int(input("Enter a test case type:\n0 - No Objects\n1 - Static Objects\n2 - Random Objects\n"))
polygon1 = []
polygon2 = []
polygon3 = []
polygon4 = []
polygon5 = []
polygon6 = []
polygon7 = []
polygon8 = []

start = (195,408); goal = (961,48); goalRadius = 40
if testCase == 0:
    'do nothing'
elif testCase == 1:
    polygon1 = [(227,458),(227,347),(580,347),(580,458)]
    polygon2 = [(209,260),(330,280),(399,145),(318,31),(190,148)]
    polygon3 = [(408,300),(500,300),(450,123)]
    polygon4 = [(508,184),(508,45),(595,29),(659,97)]
    polygon5 = [(597,245),(632,403),(705,332)]
    polygon6 = [(678,275),(678,46),(825,46),(825,275)]
    polygon7 = [(761,341),(841,288),(902,339),(902,428),(832,463),(761,420)]
    polygon8 = [(845,74),(921,300),(941,85),(900,50)]
#elif testCase == 2:
# keep the start and goal static

polygons = [polygon1,polygon2,polygon3,polygon4,polygon5,polygon6,polygon7,polygon8]

def getLines():
    linesList = []
    for polygon in polygons:
        for index in range(len(polygon)):
            linesList.append((polygon[index],polygon[(index+1) % len(polygon)]))
    return linesList
lines = getLines()

def calculateDist(node1,node2):
    return sqrt((node2[0]-node1[0])**2 + ((rows-node2[1])-(rows-node1[1]))**2)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def intersectsWithLine(node1,node2):
    for line in lines:
        if intersect((node1[0],rows-node1[1]),(node2[0],rows-node2[1]),(line[0][0],rows-line[0][1]),(line[1][0],rows-line[1][1])):
            return True
    return False

# Tree dictionary that stores a vertex as key, and its edge as value
# no two keys can be the same!
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
    m = ((rows-rand[1])-(rows-near[1])) / (rand[0]-near[0])
    distance = 5 # increase for greater node traveling distance
    ratio = distance / calculateDist(rand,near)
    offsetX = (1-ratio) * near[0] + ratio * rand[0]
    offsetY = (1-ratio) * near[1] + ratio * rand[1]
    return (offsetX,offsetY)

def nodeWithinGoal(node):
    if calculateDist(goal,node) <= goalRadius:
        return True
    return False

finalPath = []
def generateRRT(k):
    for i in range(k):
        xrand = (randint(0,1280),randint(0,720))
        xnear = nearestNeighbor(xrand)
        xnew = selectInput(xrand,xnear)
        # xnew cannot be existing vertex, or collide with polygon line
        if (xnew in tree) or intersectsWithLine(xnear,xnew):
            continue
        tree[xnew] = (xnear,xnew)
        # check if xnew is in the goal radius
        if nodeWithinGoal(xnew):
            finalPath.clear(); node = xnew
            while node != start:
                finalPath.append(node)
                node = tree[node][0]
            finalPath.append(start)
    return

# draw start, goal, and objects
def drawField():
    if testCase != 0:
        for polygon in polygons:
            pygame.draw.polygon(screen,BLACK,polygon,4)
    pygame.draw.circle(screen,RED,start,5)
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
    # poll exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            generateRRT(50) # change value for number of nodes generated on keypress

    # draw background, then objects and trees, and update screen
    screen.fill(WHITE); drawField(); drawTree(); pygame.display.update()

pygame.quit()