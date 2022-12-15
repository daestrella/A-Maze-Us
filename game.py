import sys
import pygame as pg
from src.const import *
from src.node import *

rows    = INIT_ROWS
columns = INIT_COLUMNS

class Game:
    def __init__(self, width, height):
        pg.init()
        self.width = width
        self.height = height
        self.window = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.fps = 60
        self.state = False

    def renderText(self, string, color, size, coordinates):
        font = pg.font.Font("Inter.ttf", size)
        text = font.render(string, False, color)
        self.window.blit(text, coordinates)
    
    def renderCenteredText(self, string, color, size, y):
        font = pg.font.Font("Inter.ttf", size)
        text = font.render(string, False, color)
        x = (self.width - text.get_width()) / 2
        self.window.blit(text, (x, y))
        return [x, y, x+text.get_width(), y+text.get_height()]

    def renderRightText(self, string, color, size, y):
        font = pg.font.Font("Inter.ttf", size)
        text = font.render(string, False, color)
        x = self.width - text.get_width()
        self.window.blit(text, (x, y))
        return [x, y, x+text.get_width(), y+text.get_height()]
    
    def tutorial(self):
        while True:
            self.window.fill(SACCENT)
            self.renderCenteredText("Tutorial", MACCENT, 70, 100)
            self.renderCenteredText("Press R to generate another maze.", BLACK, 30, 250)
            self.renderCenteredText("Use the left and right arrow keys", BLACK, 30, 320)
            self.renderCenteredText("to adjust the column count.", BLACK, 30, 360)
            self.renderCenteredText("Use the up and down arrow keys", BLACK, 30, 430)
            self.renderCenteredText("to adjust the row count.", BLACK, 30, 470)
            self.renderCenteredText("(Press any key to continue.)", GREY, 30, 540)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    return
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
            pg.display.update()

    def generate_state(self):
        self.tutorial()
        self.canvas = pg.Surface((self.width, self.height))

        while True:
            nlist = generateNodes(rows, columns)
            currentNode = pickStartingNode(nlist)

            proceed = True
            while proceed:
                proceed = genInputs()
                self.window.fill(WHITE)
                self.window.blit(self.canvas, (0, 0))
                self.canvas.fill(WHITE)
            
                if currentNode is not None:
                    currentNode = nextNode(nlist, currentNode)

                self.renderText(f"Rows: {rows}, Columns: {columns}", MACCENT, 15, (0, self.width-15))
                displayGrids(self.canvas, nlist)
                pg.display.update()

    def main_menu(self):
        global start_button
        global quit_button
        
        pg.display.set_caption("A-Maze Us")

        while True:
            self.window.fill(BLACK)
            
            self.window.fill(WHITE, (0, 140, self.width, 140))
            self.renderCenteredText("A-Maze Us", MACCENT, 100, 150)
            self.renderCenteredText("A maze generator application", GREY, 30, 300)
            self.renderCenteredText("using depth-first search algorithm", GREY, 30, 330)
            
            start_button = self.renderCenteredText("Generate", WHITE, 50, 400)
            quit_button = self.renderCenteredText("Quit", WHITE, 50, 500)
            self.renderRightText("version 1.0", GREY, 15, self.height-15)
            
            state = mmInputs()

            if state:
                self.generate_state()

            pg.display.update()
            self.clock.tick(60)

def mmInputs():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            pg.quit()
            sys.exit(0)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if mousePosCompare(pg.mouse.get_pos(), start_button):
                return True
            if mousePosCompare(pg.mouse.get_pos(), quit_button):
                pg.quit()
                sys.exit(0)

def genInputs():
    global rows
    global columns

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            pg.quit()
            sys.exit(0)
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            return False
        if event.type == pg.KEYDOWN and event.key == pg.K_DOWN and columns > 1:
            columns = columns - 1
            return False
        if event.type == pg.KEYDOWN and event.key == pg.K_UP:
            columns = columns + 1
            return False
        if event.type == pg.KEYDOWN and event.key == pg.K_LEFT and rows > 1:
            rows = rows - 1
            return False
        if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            rows = rows + 1
            return False

    return True

def mousePosCompare(mousePos, range):
    mouseX, mouseY = mousePos
    x0, y0, x1, y1 = range
    if x0 > mouseX or x1 < mouseX or y0 > mouseY or y1 < mouseY:
        return False
    return True

mzGen = Game(W_WIDTH, W_HEIGHT)
mzGen.main_menu()

