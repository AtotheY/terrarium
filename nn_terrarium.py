import numpy as np
import mapGen as mg

dimension = 11
mapData = mg.mapGen(dimension)
global_map = mapData[0]
pos_y = mapData[1][0]
pos_x = mapData[1][1]


scoreMap = []
# Creates a map whos boarders are all covered by WATER
# Example for 4 by 4 (dimension of 4)
# 1 1 1 1
# 1 0 0 1
# 1 0 0 1
# 1 1 1 1
# Reccomended map is NO LESS than 11 by 11
w1 = np.random.uniform(0,1)
w2 = np.random.uniform(0,1)
w3 = np.random.uniform(0,1)
lastMove = ""
def foodGen():
    x = np.random.randint(1,dimension-1)
    y = np.random.randint(1,dimension-1)
    while global_map[y][x] != 0:
        y = np.random.randint(1,dimension-1)
        x = np.random.randint(1,dimension-1)
    global_map[x][y] = 2

moves = 0
hunger = 0
max_moves = dimension * 5
max_hunger = dimension * 2


#printing the map properly
# w = water, f = food, x for critter
print "***** steps: ", moves, "/", max_moves, " ***** hunger: ", hunger, "/",max_hunger, " *****"
for i in range (dimension):
    for j in range (dimension):
        if global_map[i][j]==1:
            print "w",
        elif global_map[i][j]==2:
            print "f",
        elif global_map[i][j]==9:
            print "X",
        else:
            print " ",
    print ""

#Checking all the way left
def checkLeft(tpos_y, tpos_x):
    print tpos_y, tpos_x
    node1 = 0
    node2 = 0
    distance = 0
    for i in range (-tpos_x, 0):
        distance += 1
        #print "LEFT ITERATION: ", i , "IT IS A: ", global_map[tpos_y][-i-1]
        if global_map[tpos_y][-i-1] == 1:
            node1 = 0
            node2 = 1
            break
        elif global_map[tpos_y][-i-1] == 2:
            node1 = 1
            node2 = 1
            break
    return node1, node2, distance

#Checking all the way right
def checkRight(tpos_y, tpos_x):
    node1 = 0
    node2 = 0
    distance = 0
    for i in range (tpos_x + 1, dimension):
        distance += 1
        if global_map[tpos_y][i] == 1:
            node1 = 0
            node2 = 1
            break
        elif global_map[tpos_y][i] == 2:
            node1 = 1
            node2 = 1
            break
    return node1, node2, distance

#Checking all the way up
def checkUp(tpos_y, tpos_x):
    node1 = 0
    node2 = 0
    distance = 0
    for i in range (-tpos_y, 0):
        distance += 1
        if global_map[-i-1][tpos_x] == 1:
            node1 = 0
            node2 = 1
            break
        elif global_map[-i-1][tpos_x] == 2:
            node1 = 1
            node2 = 1
            break
    return node1, node2, distance

#Checking all the way down
def checkDown(tpos_y, tpos_x):
    node1 = 0
    node2 = 0
    distance = 0
    for i in range (tpos_y + 1, dimension):
        distance += 1
        if global_map[i][tpos_x] == 1:
            node1 = 0
            node2 = 1
            break
        elif global_map[i][tpos_x] == 2:
            node1 = 1
            node2 = 1
            break
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
    print w1, w2, w3
    print initial1, initial2, distance
    return w1*initial1 + w2*initial2 + w3*(1/distance)


def getMove(tpos_y, tpos_x):
    left = neuralNet(checkLeft(tpos_y, tpos_x))
    right = neuralNet(checkRight(tpos_y, tpos_x))
    up = neuralNet(checkUp(tpos_y, tpos_x))
    down = neuralNet(checkDown(tpos_y, tpos_x))
    myMax = max(left, right, up, down)
    print left, right, up, down
    amount = ""
    if myMax == left:
        amount += "l"
    elif myMax == right:
        amount += "r"
    elif myMax == down:
        amount += "d"
    elif myMax == up:
        amount += "u"
    print amount
    return amount



for i in range (0,64):

    score = 0
    while True:
        command = getMove(pos_y, pos_x)
        print "MOVING: ", command
        moves += 1
        hunger += 1
        if moves == max_moves:
            score = moves
            break
        if hunger == max_hunger:
            score = moves
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

        if global_map[pos_y][pos_x] == 1:
            score = moves
            break
        elif global_map[pos_y][pos_x] == 2:
            if hunger >= 5:
                hunger -= 5
            else:
                hunger = 0
            foodGen()
            global_map[pos_y][pos_x] = 9
            global_map[old_pos_y][old_pos_x] = 0

        else:
            print "new pos: ", pos_x, pos_y
            global_map[pos_y][pos_x] = 9
            global_map[old_pos_y][old_pos_x] = 0



#
# print "***** steps: ", moves, "/", max_moves, " ***** hunger: ", hunger, "/",max_hunger, " *****"
# for i in range (dimension):
#     for j in range (dimension):
#         if global_map[i][j]==1:
#             print "w",
#         elif global_map[i][j]==2:
#             print "f",
#         elif global_map[i][j]==9:
#             print "X",
#         else:
#             print " ",
#     print ""
