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

start = (195,408); goal = (961,48)
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

# Tree dictionary that stores a vertex as key, and its edge as value
# no two keys can be the same!
tree = {}
def nearestNeighbor(node):
    closestNeighborNode = ()
    shortestNeighborDist = 0
    for vertex in tree:
        if calculateDist(vertex,node) < shortestNeighborDist or shortestNeighborDist == 0:
            closestNeighborNode = vertex
    return closestNeighborNode


def generateRRT(k):
    for i in range(k):
        xrand = (randint(0,1280),randint(0,720))
        xnear = nearestNeighbor(xrand)
        u = selectState()
        xnew = newInput() # xnew cannot be an existing vertex in the tree
        # check if xnew is in the goal radius
    return

# draw start, goal, and objects
def drawField():
    for polygon in polygons:
        pygame.draw.polygon(screen,BLACK,polygon,3)
    pygame.draw.circle(screen,RED,start,4)
    pygame.draw.circle(screen,GREEN,goal,20)

def drawTrees():
    # draw grey line for every edge in tree
    
    # draw orange line for the shortest path in tree

    return

running = True
while running:
    # poll exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            generateRRT(50)

    # draw background, then objects and trees, and update screen
    screen.fill(WHITE); drawField(); drawTrees(); pygame.display.update()

pygame.quit()