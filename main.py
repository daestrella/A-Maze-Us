# Maze generator using depth-first search and stack backtracking
import pygame as pg
from src.const import *
from src.node import *

# temporary rows and columns
rows = int(input("How many rows:\t"))
columns = int(input("How many columns:\t"))

# initialize pygame window
pg.init()
win = pg.display.set_mode((W_WIDTH, W_HEIGHT))
pg.display.set_caption("MzGen - Pre-Alpha, v. 0.3")
cl = pg.time.Clock()

# canvas for the maze
mzCanvas = pg.Surface((W_WIDTH, W_HEIGHT))
mzCanvas.fill(WHITE)

# generate (rows x columns) nodes of the maze
nlist = generateNodes(rows, columns)

# for debugging purposes only. to be deleted later.
for i in range(len(nlist)):
    for j in range(len(nlist[i])):
        print(f"{(nlist[i][j].x, nlist[i][j].y)}{nlist[i][j].neighbours}")

# pick a random starting node for the depth-search
currentNode = pickStartingNode(nlist)


# loop until the game is stopped
while True:
    if pg.event.get() == pg.QUIT:
        pg.quit()
        break

    win.fill(WHITE)
    win.blit(mzCanvas, (0, 0))
    mzCanvas.fill(WHITE)
    
    if currentNode is not None:
        print(f"Current: {(currentNode.x, currentNode.y)}")
        currentNode = nextNode(nlist, currentNode)
 
    displayGrids(mzCanvas, nlist)
    pg.display.update()
    cl.tick(60)
