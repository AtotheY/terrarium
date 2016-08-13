# terrarium


This program uses genetic programming to train "critters" to play a very simple game.

The game is structured as follows. You are givena 2D map which contains 4 elements -- Your character, Water, Food, and free spaces.
f - food
1 - water
0 - free space
X - character

1 1 1 1 1  
1 0 0 f 1  
1 f 0 0 1  
1 0 X 0 1  
1 1 1 1 1  

You can choose to move either up, down, left, or right. 

The objective of the game is to die of old age, by moving a fixed amount of steps without falling into water or dying of starvation.

# Genetic Programming
If you run  
```python genetic_terrarium.py```

you can see the game play itself. 64 Critters are initially spawned, and use a coefficient system to play the game.

Each critter judges the strength of moving in a direction using the equation Strength = C1X1 + C2X2 + C3*(1/d)
where c1,c2, and c3 are randomly generated coefficients specific to the critter, x1 and x2 correspond to the closest non empty tile type, and d corresponds to the distance that tile is from the critter.

After 64 critters play a specific map, the top 7 have "mate" (they reproduce a new critter with a mix of both parents coefficients) and the game is played again with the new critters. (the remaining 15 spots are newly generated critters)

Each epoch should have an increasingly larger average score, however, due to the limitations of the 2D 4-move system, the difference between each epoch is too volitile.
