import numpy as np
import mapGen as mg
import copy
import operator
from collections import defaultdict

def foodGen():
    x = np.random.randint(1,dimension-1)
    y = np.random.randint(1,dimension-1)
    while global_map[y][x] != 0:
        y = np.random.randint(1,dimension-1)
        x = np.random.randint(1,dimension-1)
    global_map[x][y] = 2


#Checking all the way left
def checkLeft(tpos_y, tpos_x):
    #print tpos_y, tpos_x
    node1 = 0
    node2 = 0
    distance = 0
    for i in range (-tpos_x, 0):
        die = False
        distance += 1
        #print "LEFT ITERATION: ", i , "IT IS A: ", global_map[tpos_y][-i-1]
        if global_map[tpos_y][-i-1] == 1:
            node1 = 0
            node2 = 1
            if distance == 1:
                die = True
            break
        elif global_map[tpos_y][-i-1] == 2:
            node1 = 1
            node2 = 1
            break
    if die:
        return node1, node2, -distance
    return node1, node2, distance

#Checking all the way right
def checkRight(tpos_y, tpos_x):
    node1 = 0
    node2 = 0
    distance = 0
    for i in range (tpos_x + 1, dimension):
        die = False
        distance += 1
        if global_map[tpos_y][i] == 1:
            node1 = 0
            node2 = 1
            if distance == 1:
                die = True
            break
        elif global_map[tpos_y][i] == 2:
            node1 = 1
            node2 = 1
            break
    if die:
        return node1, node2, -distance
    return node1, node2, distance

#Checking all the way up
def checkUp(tpos_y, tpos_x):
    node1 = 0
    node2 = 0
    distance = 0
    for i in range (-tpos_y, 0):
        die = False
        distance += 1
        if global_map[-i-1][tpos_x] == 1:
            node1 = 0
            node2 = 1
            if distance == 1:
                die = True
            break
        elif global_map[-i-1][tpos_x] == 2:
            node1 = 1
            node2 = 1
            break
    if die:
        return node1, node2, -distance
    return node1, node2, distance

#Checking all the way down
def checkDown(tpos_y, tpos_x):
    node1 = 0
    node2 = 0
    distance = 0
    for i in range (tpos_y + 1, dimension):
        die = False
        distance += 1
        if global_map[i][tpos_x] == 1:
            node1 = 0
            node2 = 1
            if distance == 1:
                die = True
            break
        elif global_map[i][tpos_x] == 2:
            node1 = 1
            node2 = 1
            break
    if die:
        return node1, node2, -distance
    return node1, node2, distance

def neuralNet(arr):
    #Initial node layout
    # initial1   initial2  distance
    #         hidden layer
    #         hidden layer
    #           output
    initial1 = arr[0]
    initial2 = arr[1]
    distance = arr[2]
    return w1*initial1 + w2*initial2 + w3*(1/distance)


def getMove(tpos_y, tpos_x):
    left = neuralNet(checkLeft(tpos_y, tpos_x))
    right = neuralNet(checkRight(tpos_y, tpos_x))
    up = neuralNet(checkUp(tpos_y, tpos_x))
    down = neuralNet(checkDown(tpos_y, tpos_x))
    myMax = max(left, right, up, down)
    #print left, right, up, down
    amount = ""
    if myMax == left:
        amount += "l"
    elif myMax == right:
        amount += "r"
    elif myMax == down:
        amount += "d"
    elif myMax == up:
        amount += "u"
    #print amount
    return amount

# ******************* PROGRAM ****************** #
dimension = 11
mapData = mg.mapGen(dimension)


max_moves = dimension * 5
max_hunger = dimension * 2
global_map = mapData[0]


scoreMap = {}


# Creates a map whos boarders are all covered by WATER
# Example for 4 by 4 (dimension of 4)
# 1 1 1 1
# 1 0 0 1
# 1 0 0 1
# 1 1 1 1
# Recommended map is NO LESS than 11 by 11
critterMap = defaultdict(list)

for i in range (0,64):
    real_map = copy.deepcopy(mapData[0])
    global_map = copy.deepcopy(real_map)
    pos_y = copy.deepcopy(mapData[1][0])
    pos_x = copy.deepcopy(mapData[1][1])
    w1 = np.random.uniform(0,1)
    w2 = np.random.uniform(0,1)
    w3 = np.random.uniform(0,1)
    critterMap[i].append([w1,w2,w3])
    lastMove = ""
    dead = False
    moves = 0
    hunger = 0
    while not dead:
        command = getMove(pos_y, pos_x)
        #print "***** steps: ", moves, "/", max_moves, " ***** hunger: ", hunger, "/",max_hunger, " *****"
        #print "MOVING: ", command
        moves += 1
        hunger += 1
        if moves == max_moves:
            scoreMap[i] = moves
            break
        if hunger == max_hunger:
            scoreMap[i] = moves
            break
        old_pos_y = pos_y
        old_pos_x = pos_x
        if command == "d":
            pos_y += 1
        elif command == "u":
            pos_y -= 1
        elif command == "l":
            pos_x -= 1
        elif command == "r":
            pos_x += 1
        else:
            print ""
        if global_map[pos_y][pos_x] == 1:
            scoreMap[i] = moves
            dead = True
        elif global_map[pos_y][pos_x] == 2:
            if hunger >= 5:
                hunger -= 5
            else:
                hunger = 0
            foodGen()
            global_map[pos_y][pos_x] = 9
            global_map[old_pos_y][old_pos_x] = 0

        else:
            global_map[pos_y][pos_x] = 9
            global_map[old_pos_y][old_pos_x] = 0
avg = 0
for i in scoreMap:
    avg += scoreMap[i]
    #print i,scoreMap[i]
print "Average for first epoch: ", avg/len(scoreMap)

sorted_x = sorted(scoreMap.items(), key=operator.itemgetter(1))
#print sorted_x[63]
counterz = 0
newCritterMap = defaultdict(list)
repreductionList = []
for i in range (-63,-56):
    counterz += 1
    #print " RANK #", counterz, " is critter : ", sorted_x[-i][0], " with a score of ", sorted_x[-i][1], " and weights of W1: " , critterMap[sorted_x[-i][0]][0][0], " W2: ", critterMap[sorted_x[-i][0]][0][1] , " W3: ", critterMap[sorted_x[-i][0]][0][2]
    repreductionList.append(sorted_x[-i][0])
#print "REP LIST: ", repreductionList

countChildren = 0
for q in range (len(repreductionList)):

    parentA = repreductionList[q]
    #print "first parent is: ",repreductionList[q], " with values ",  critterMap[sorted_x[parentA][0]][0][0],  critterMap[sorted_x[parentA][0]][0][1],  critterMap[sorted_x[parentA][0]][0][2]
    for v in repreductionList:
        parentB = v
        #print "second parent is: ",parentB, " with values ",  critterMap[sorted_x[parentB][0]][0][0],  critterMap[sorted_x[parentB][0]][0][1],  critterMap[sorted_x[parentB][0]][0][2]
        newCritterMap[countChildren].append([critterMap[sorted_x[parentA][0]][0][0],critterMap[sorted_x[parentB][0]][0][1],critterMap[sorted_x[parentA][0]][0][2]])
        countChildren += 1

for q in range (45,64):
    w1 = np.random.uniform(0,1)
    w2 = np.random.uniform(0,1)
    w3 = np.random.uniform(0,1)
    newCritterMap[q].append([w1,w2,w3])
#print "DONE REP RODUCING. RESULTS: ", newCritterMap

epoches = 100
for e in range(1,epoches):
    mapData = mg.mapGen(dimension)


    max_moves = dimension * 5
    max_hunger = dimension * 2
    global_map = mapData[0]
    for i in range (0,63):
        real_map = copy.deepcopy(mapData[0])
        global_map = copy.deepcopy(real_map)
        pos_y = copy.deepcopy(mapData[1][0])
        pos_x = copy.deepcopy(mapData[1][1])
        w1 = newCritterMap[i][0][0]
        w2 = np.random.uniform(0,1)
        w3 = np.random.uniform(0,1)
        critterMap[i].append([w1,w2,w3])
        lastMove = ""
        dead = False
        moves = 0
        hunger = 0
        while not dead:
            command = getMove(pos_y, pos_x)
            #print "***** steps: ", moves, "/", max_moves, " ***** hunger: ", hunger, "/",max_hunger, " *****"
            #print "MOVING: ", command
            moves += 1
            hunger += 1
            if moves == max_moves:
                scoreMap[i] = moves
                break
            if hunger == max_hunger:
                scoreMap[i] = moves
                break
            old_pos_y = pos_y
            old_pos_x = pos_x
            if command == "d":
                pos_y += 1
            elif command == "u":
                pos_y -= 1
            elif command == "l":
                pos_x -= 1
            elif command == "r":
                pos_x += 1
            else:
                print ""
            if global_map[pos_y][pos_x] == 1:
                scoreMap[i] = moves
                dead = True
            elif global_map[pos_y][pos_x] == 2:
                if hunger >= 5:
                    hunger -= 5
                else:
                    hunger = 0
                foodGen()
                global_map[pos_y][pos_x] = 9
                global_map[old_pos_y][old_pos_x] = 0

            else:
                global_map[pos_y][pos_x] = 9
                global_map[old_pos_y][old_pos_x] = 0
    avg = 0
    for i in scoreMap:
        avg += scoreMap[i]
        #print i,scoreMap[i]
    print "Epoch ", e, " average lifespan is : ", avg/len(scoreMap), " steps per critter"

    sorted_x = sorted(scoreMap.items(), key=operator.itemgetter(1))
    #print sorted_x[63]
    counterz = 0
    newCritterMap = defaultdict(list)
    repreductionList = []
    for i in range (-63,-56):
        counterz += 1
        #print " RANK #", counterz, " is critter : ", sorted_x[-i][0], " with a score of ", sorted_x[-i][1], " and weights of W1: " , critterMap[sorted_x[-i][0]][0][0], " W2: ", critterMap[sorted_x[-i][0]][0][1] , " W3: ", critterMap[sorted_x[-i][0]][0][2]
        repreductionList.append(sorted_x[-i][0])
    #print "REP LIST: ", repreductionList

    countChildren = 0
    for q in range (len(repreductionList)):

        parentA = repreductionList[q]
        #print "first parent is: ",repreductionList[q], " with values ",  critterMap[sorted_x[parentA][0]][0][0],  critterMap[sorted_x[parentA][0]][0][1],  critterMap[sorted_x[parentA][0]][0][2]
        for v in repreductionList:
            parentB = v
            #print "second parent is: ",parentB, " with values ",  critterMap[sorted_x[parentB][0]][0][0],  critterMap[sorted_x[parentB][0]][0][1],  critterMap[sorted_x[parentB][0]][0][2]
            newCritterMap[countChildren].append([critterMap[sorted_x[parentA][0]][0][0],critterMap[sorted_x[parentB][0]][0][1],critterMap[sorted_x[parentA][0]][0][2]])
            countChildren += 1

    for q in range (45,64):
        w1 = np.random.uniform(0,1)
        w2 = np.random.uniform(0,1)
        w3 = np.random.uniform(0,1)
        newCritterMap[q].append([w1,w2,w3])

#
# print "***** steps: ", moves, "/", max_moves, " ***** hunger: ", hunger, "/",max_hunger, " *****"
    #printing the map properly
    # w = water, f = food, x for critter
    #for v in range (dimension):
    #    for j in range (dimension):
    #        if global_map[v][j]==1:
    #            print "w",
    #        elif global_map[v][j]==2:
    #            print "f",
    #        elif global_map[v][j]==9:
    #            print "X",
    #        else:
    #            print " ",
    #    print ""
