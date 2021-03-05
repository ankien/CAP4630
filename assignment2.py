import math
import pygame

columns, rows = (1280,720)

WHITE = (255,255,255) # screen color
BLACK = (0,0,0) # polygon color
ORANGE = (255,165,0) # line color
GREEN = (0,255,0) # goal color
RED = (255,0,0) # start color

start = (195,408); goal = (961,48)

# enviroment 1
polygon1 = [(227,458),(227,347),(580,347),(580,458)]
polygon2 = [(209,260),(330,280),(399,145),(318,31),(190,148)]
polygon3 = [(408,300),(500,300),(450,123)]
polygon4 = [(508,184),(508,45),(595,29),(659,97)]
polygon5 = [(597,245),(632,403),(705,332)]
polygon6 = [(678,275),(678,46),(825,46),(825,275)]
polygon7 = [(761,341),(841,288),(902,339),(902,428),(832,463),(761,420)]
polygon8 = [(845,74),(921,300),(941,85),(900,50)]

# enviroment 2
polygon9 = [(227,658),(437,558),(330,207)]
polygon10 = [(350,0),(530,0),(470,258)]
polygon11 = [(650,300),(700,400),(825,300),(775,100),(725,100)]
polygon12 = [(850,600),(900,600),(900,300),(850,300)]
polygon13 = [(850,200),(900,200),(900,0),(850,0)]

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
def drawField(screen):
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
            if intersect((currNode[0]+offsetX1,rows-currNode[1]+offsetY1),(node[0]+offsetX2,rows-node[1]+offsetY2),(line[0][0],rows-line[0][1]),(line[1][0],rows-line[1][1])) and notLine(currNode,node):
                neighbors.pop()
                break
    return neighbors

# g(n) == cost of path from start node to goal
# C == some value
# h(n) == path from node to goal
def popHighestU(openList,cValue):
    currHighestNode = ()
    currHighest = 0
    for node in openList:
        # (C - g(n)) / h(n)
        if ((cValue - g[node])/calculateDist(node,goal)) > currHighest or currHighest == 0:
            currHighest = ((cValue - g[node])/calculateDist(node,goal))
            currHighestNode = node
    closed[currHighestNode] = openList[currHighestNode]
    del openList[currHighestNode]
    return currHighestNode

# nodes in openlist contain g(n) value, and previous node n
def potentialSearch(cValue):
    open = {start:start}
    global closed
    closed = {}
    global g
    g = {start:0}
    while len(open):
        n = popHighestU(open,cValue)
        neighbors = findNeighbors(n)
        for neighbor in neighbors:
            if neighbor in open or neighbor in closed:
                if g[neighbor] <= (g[n] + calculateDist(n,neighbor)):
                    continue

            newNeighborGN = g[n] + calculateDist(n,neighbor)

            if newNeighborGN + calculateDist(neighbor,goal) >= C:
                continue

            if neighbor == goal:
                closed[goal] = n
                return 1

            if neighbor in open:
                g[neighbor] = newNeighborGN
            else:
                open[neighbor] = n
                g[neighbor] = newNeighborGN

    return 0

def drawLines():
    lastNode = goal
    for node in closed:
        pygame.draw.line(screen,ORANGE,lastNode,closed[lastNode],2)
        lastNode = closed[lastNode]

print("Enter Ctrl+C to exit from this menu.\n")
running = False
while True:
    # read input variables
    enviroment = int(input("Enter enviroment # (1 - default, 2 - custom enviroment, 0 - exit program): "))
    C = ()
    if enviroment != 0:    
        C = int(input("Enter C value: "))

    if enviroment == 1:
        polygons = [polygon1,polygon2,polygon3,polygon4,polygon5,polygon6,polygon7,polygon8]
        nodes = polygon1 + polygon2 + polygon3 + polygon4 + polygon5 + polygon6 + polygon7 + polygon8
        nodes.append(goal)
        outcome = potentialSearch(C)
        running = True
    elif enviroment == 2:
        polygons = [polygon9,polygon10,polygon11,polygon12,polygon13]
        nodes = polygon9 + polygon10 + polygon11 + polygon12 + polygon13
        nodes.append(goal)
        outcome = potentialSearch(C)
        running = True
    elif enviroment == 0:
        break
    else:
        print("Invalid enviroment!\n")

    if outcome == 0:
        print("No path found.\n")
        continue
    
    # window main loop
    if running:
        pygame.init()
        pygame.display.set_caption("Andrew's Potential Search Visualization")
        screen = pygame.display.set_mode((columns,rows))
    while True:
        # poll exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if running == False:
            pygame.quit()
            break

        # draw background, then shapes and lines, and update screen
        screen.fill(WHITE); drawField(screen); drawLines(); pygame.display.update()