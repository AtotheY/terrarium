def mapGen(dimension):
  import numpy as np
  global_map =[[0 for x in range(dimension)] for y in range(dimension)]
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
  return global_map,(pos_y,pos_x)
