import numpy as np
dimension = 11
global_map =[[0 for x in range(dimension)] for y in range(dimension)]

# Creates a map whos boarders are all covered by WATER
# Example for 4 by 4 (dimension of 4)
# 1 1 1 1
# 1 0 0 1
# 1 0 0 1
# 1 1 1 1
# Reccomended map is NO LESS than 11 by 11

for i in range (dimension):
    global_map[i][0] = 1
    global_map[0][i] = 1
    global_map[dimension-1][i] = 1
    global_map[i][dimension-1] = 1

available_spots = (dimension-1) * (dimension-1)

#generating random water and food spots, 1 spot in each row (for now)
for i in range (1,dimension-1):
    x = np.random.randint(1,dimension-1)
    y = np.random.randint(1,dimension-1)
    while y == x:
        y = np.random.randint(0,dimension-1)
    global_map[i][x] = 1
    global_map[i][y] = 2



#Placing initial critter
pos_x = np.random.randint(1,dimension-1)
pos_y = np.random.randint(1,dimension-1)
while global_map[pos_x][pos_y] != 0:
    pos_x = np.random.randint(1,dimension-1)
    pos_y = np.random.randint(1,dimension-1)
global_map[pos_y][pos_x] = 9



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
while True:
    # Getting input for critter
    print "Where would you like the critter to go?"
    print "u, d, l, r"
    command  = raw_input()
    while command not in ["u","d","l","r"]:
        print "Command unreconized. u, d, l, r"
        command  = raw_input()
    moves += 1
    hunger += 1
    if moves == max_moves:
        print "You have died of old age! Congrats."
        break
    if hunger == max_hunger:
        print "You have died of hunger :("
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
        print "You fell into the water and lost"
        break
    elif global_map[pos_y][pos_x] == 2:
        print "Yum, some food!"
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
