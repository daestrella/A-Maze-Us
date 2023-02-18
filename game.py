import sys
import pygame as pg
from src.const import *
from src.node import *
from datetime import date

# initialize rows and columns (5 by 5 by default)
rows    = INIT_ROWS
columns = INIT_COLUMNS

# Game class to handle GUI
class Game:
    def __init__(self, width, height):
        pg.init()
        self.width = width
        self.height = height
        self.window = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.fps = 60
        self.state = False
        self.icon = pg.image.load("icon.jpg")

    def renderText(self, string, color, size, coordinates):
        font = pg.font.Font("Inter.ttf", size)
        text = font.render(string, False, color)
        self.window.blit(text, coordinates)
    
    # center-aligned text
    def renderCenteredText(self, string, color, size, y):
        font = pg.font.Font("Inter.ttf", size)
        text = font.render(string, False, color)
        x = (self.width - text.get_width()) / 2
        self.window.blit(text, (x, y))
        return [x, y, x+text.get_width(), y+text.get_height()]

    # right-aligned text
    def renderRightText(self, string, color, size, y):
        font = pg.font.Font("Inter.ttf", size)
        text = font.render(string, False, color)
        x = self.width - text.get_width()
        self.window.blit(text, (x, y))
        return [x, y, x+text.get_width(), y+text.get_height()]

    # tutorial screen
    def tutorial(self):
        while True:
            self.window.fill(SACCENT)
            self.renderCenteredText("Tutorial", MACCENT, 70, 50)
            self.renderCenteredText("Press R to generate another maze.", BLACK, 30, 200)
            self.renderCenteredText("Use the left and right arrow keys", BLACK, 30, 270)
            self.renderCenteredText("to adjust the column count.", BLACK, 30, 310)
            self.renderCenteredText("Use the up and down arrow keys", BLACK, 30, 380)
            self.renderCenteredText("to adjust the row count.", BLACK, 30, 420)
            self.renderCenteredText("Press S to export the maze.", BLACK, 30, 490)
            self.renderCenteredText("(Press any key to continue.)", GREY, 30, 560)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    return
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
            pg.display.update()

    # maze screen
    def generate_state(self):
        self.tutorial()
        self.canvas = pg.Surface((self.width, self.height))

        while True:
            nlist = generateNodes(rows, columns)
            currentNode = pickStartingNode(nlist)
            
            start_node, finish_node = pickStartFinish(nlist, rows, columns)
            proceed = True
            while proceed:
                proceed = genInputs()
                self.window.fill(WHITE)
                self.window.blit(self.canvas, (0, 0))
                self.canvas.fill(WHITE)

                displayStartFinish(self.canvas, start_node, finish_node)

                #if currentNode is not None:  #this is frame-dependent generation
                while currentNode is not None:
                    currentNode = nextNode(nlist, currentNode)

                self.renderText(f"Rows: {rows}, Columns: {columns}", MACCENT, 15, (0, self.width-15))
                displayGrids(self.canvas, nlist)
                pg.display.update()
                self.clock.tick(self.fps)

    # this screen starts at initialization
    def main_menu(self):
        global start_button
        global quit_button
        
        pg.display.set_caption("A-Maze Us")
        pg.display.set_icon(self.icon)

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

# this handles keyboard and mouse inputs in main menu
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

# this handles keyboard inputs in maze screen 
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
        # reset maze
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            return False
        # decrease column count
        if event.type == pg.KEYDOWN and event.key == pg.K_DOWN and columns > 1:
            columns = columns - 1
            return False
        # increase row count
        if event.type == pg.KEYDOWN and event.key == pg.K_UP:
            columns = columns + 1
            return False
        # decrease row count
        if event.type == pg.KEYDOWN and event.key == pg.K_LEFT and rows > 1:
            rows = rows - 1
            return False
        # increase row count
        if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            rows = rows + 1
            return False
        if event.type == pg.KEYDOWN and event.key == pg.K_s:
            pg.image.save(mzGen.canvas,f"{rows}x{columns}Maze{date.today()}.png")

    return True

# Checks mouse position when clicking an element
# This was used to determine whether the user click a button or not
def mousePosCompare(mousePos, range):
    mouseX, mouseY = mousePos
    x0, y0, x1, y1 = range
    if x0 > mouseX or x1 < mouseX or y0 > mouseY or y1 < mouseY:
        return False
    return True

# execution
mzGen = Game(W_WIDTH, W_HEIGHT)
mzGen.main_menu()
