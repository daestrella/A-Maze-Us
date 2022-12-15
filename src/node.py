from src.const import *
import pygame as pg
import random
import math

class Node:
    stack  = []
    rows = columns = 0
    width = height = 0

    def __init__(self, x, y):
        self.x = x              # this node is in column (x+1)
        self.y = y              # this node is in row (y+1)
        self.visited = False
        width = Node.width
        height = Node.height
        columns = Node.columns
        rows = Node.rows

        # for drawing
        self.gridpoints = [
                ((x+1) * width, (y+1) * height),    # top-left
                ((x+2) * width, (y+1) * height),    # top-right
                ((x+2) * width, (y+2) * height),    # bottom-right
                ((x+1) * width, (y+2) * height)     # bottom-left
        ]

        self.neighbours = [
                [x  , y-1, True],         # top
                [x+1, y  , True],         # right
                [x  , y+1, True],         # bottom
                [x-1, y  , True]          # left
        ]

        # checks for invalid neighbours
        for i in range(4):
            valid = Node.outOfBounds(self.neighbours[i][0], self.neighbours[i][1])
            if (self.neighbours[i][0] >= columns or self.neighbours[i][1] >= rows) or self.neighbours[i][0] < 0 or self.neighbours[i][1] < 0:
               self.neighbours[i][2] = False

    def display(self, canvas):
        width = Node.width
        height = Node.height
        x = self.x * width
        y = self.y * height
        
        if not self.visited:
           canvas.fill(GREY, (self.gridpoints[0][0], self.gridpoints[0][1], width, height))

        for i in range(4):
            if self.neighbours[i-1][2]:
                pg.draw.line(canvas, BLACK, self.gridpoints[i], self.gridpoints[i-1], 3)

    def markAsVisited(self):
        Node.stack.append(self)
        self.visited = True

    def unNeighbour(self, pos):
        self.neighbours[pos][2] = False

    @classmethod
    def outOfBounds(cls, x, y):
        if 0 > x or 0 > y or cls.columns <= x or cls.rows <= y:
            return True
        return False

    @classmethod
    def addtoStack(cls, node):
        cls.stack.append(node)

    @classmethod
    def popStack(cls):
        cls.stack.pop()

    @classmethod
    def topOfStack(cls):
        return cls.stack[-1]

    @classmethod
    def stackIsEmpty(cls):
        if len(cls.stack) == 0:
            return True
        return False

def displayGrids(canvas, li):
    width = Node.width
    height = Node.height
    rows = Node.rows
    columns = Node.columns

    for i in range(len(li)):
        for j in range(len(li[i])):
            li[i][j].display(canvas)

    pg.draw.rect(canvas, BLACK, (width, height, columns*width, rows*height), 3)

def pickStartingNode(li):
    while True:
        x = random.randrange(0, Node.columns)
        y = random.randrange(0, Node.rows)
        if not li[y][x].visited:
            li[y][x].markAsVisited()
            break

    return li[y][x]

def generateNodes(rows, columns):
    Node.rows = rows
    Node.columns = columns
    Node.width  = W_WIDTH / (Node.columns + 2)
    Node.height = W_HEIGHT / (Node.rows + 2)
    li = []
    
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(Node(j, i))
    
        li.append(row)

    return li

def nextNode(li, node1):
    pos = ["up", "right", "bottom", "left"]
    length = len(node1.neighbours)
    x1 = node1.x
    y1 = node1.y
    neighbours = list(range(0, length))

    while not len(neighbours) == 0:
        # check for available neighbour of the current node
        i = random.choice(neighbours)
        neighbours.remove(i)
        x2 = node1.neighbours[i][0]
        y2 = node1.neighbours[i][1]
        available = node1.neighbours[i][2]
        
        if Node.outOfBounds(x2, y2):
            continue

        if available and not li[y2][x2].visited:
            li[y1][x1].unNeighbour(i)
            li[y2][x2].markAsVisited()
            li[y2][x2].unNeighbour(i-2)

            return li[y2][x2]

    Node.popStack()
    if not Node.stackIsEmpty():
        return Node.topOfStack()
