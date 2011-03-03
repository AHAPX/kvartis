# -*- coding: utf8 -*-

import random, sys, time
import os

default_figures = {
    0: ((0, 0), (-1, 0), (1, 0), (2, 0)),
    1: ((0, 0), (-1, 0), (1, 0), (1, 1)),
    2: ((0, 0), (-1, 0), (1, 0), (-1, 1)),
    3: ((0, 0), (-1, 0), (0, 1), (1, 1)),
    4: ((0, 0), (1, 0), (0, 1), (-1, 1)),
    5: ((0, 0), (1, 0), (0, 1), (1, 1)),
    6: ((0, 0), (-1, 0), (1, 0), (0, 1))}

def moveFigure(figure, x = 0, y = 0):
    return map(lambda a: (a[0] + x, a[1] + y), figure)

def rotateFigure(figure, direct = 1):
    newfigure = figure[:]
    for i in xrange(1, len(newfigure)):
        newfigure[i] = (newfigure[0][0] + (newfigure[i][1] - newfigure[0][1])*direct, newfigure[0][1] + (newfigure[0][0] - newfigure[i][0])*direct)
    return newfigure

class gameException(Exception): pass
class gameExceptMove(gameException): pass
class gameExceptDestroy(gameException): pass
class gameExceptLose(gameException): pass
class gameExceptNewFigure(gameException): pass

class gameFigure:
    def __init__(self, area, x = None, y = 0, fig_id = -1):
        self.cell = 1
        self.area = area
        if not x: x = int(area.len_x/2)
        figure = default_figures.get(fig_id)
        if not figure:
            figure = random.choice(default_figures)
        self.figure = map(lambda cell: (cell[0] + x, cell[1] + y), figure)
        if not self.movable(self.figure):
            raise gameExceptLose

    def __call__(self):
        return self.figure
        
    def movable(self, figure):
        try:
            return reduce(lambda a, b: a and b, map(lambda a: (0 <= a[0] < self.area.len_x) and (0 <= a[1] < self.area.len_y), figure)) and (not reduce(lambda a, b: a or b, [self.area.matrix[cell[1]][cell[0]] for cell in figure]))
        except:
            print figure
            raise gameExceptMove

    def rotate(self, direct = 1):
        for i in (0, -1, 1):
            figure = rotateFigure(moveFigure(self.figure, x = i), direct)
            if self.movable(figure):
                self.figure = figure
                return 1
        raise gameExceptMove

    def move(self, x = 0, y = 0):
        figure = moveFigure(self.figure, x, y)
        if not self.movable(figure):
            raise gameExceptMove
        self.figure = figure

    def moveDown(self):
        try:
            self.move(y = 1)
        except gameExceptMove:
            for fig in self.figure:
                self.area.matrix[fig[1]][fig[0]] = self.cell
            raise gameExceptDestroy

class gameArea:
    def __init__(self, len_x, len_y):
        self.len_x = len_x
        self.len_y = len_y
        self.matrix = [[None for i in xrange(len_x)] for i in xrange(len_y)]

    def clearLines(self):
        matrix = []
        for line in self.matrix:
            if not reduce(lambda a, b: a and b, line):
                matrix.append(line)
        for i in xrange(self.len_y-len(matrix)):
            matrix.insert(0, [None for j in xrange(self.len_x)])
        self.matrix = matrix

    def paint(self):
        for i in self.matrix:
            line = ''
            for j in i:
                if j:
                    line += '*'
                else:
                    line += ' '
            print '|', line, '|'

class gameZone:
    def __init__(self):
        self.area = gameArea(10, 20)
        self.next_figure = gameFigure(self.area)
        self.newFigure()

    def paint(self):
        os.system('clear')
        for fig in self.figure():
            self.area.matrix[fig[1]][fig[0]] = 1
        for i in self.area.matrix:
            line = ''
            for j in i:
                if j:
                    line += '#'
                else:
                    line += ' '
            print '|', line, '|'
        for fig in self.figure():
            self.area.matrix[fig[1]][fig[0]] = 0

    def newFigure(self, x = None, y = 2, fig_id = -1):
        self.figure = self.next_figure
        self.next_figure = gameFigure(self.area, x, y, fig_id)
        for i in xrange(random.randint(0, 3)):
            self.next_figure.rotate()

    def moveDown(self):
        try:
            self.figure.moveDown()
        except gameExceptDestroy:
            self.area.clearLines()
            self.newFigure()
            raise gameExceptNewFigure

    def run(self, timeout):
        while True:
            self.paint()
            time.sleep(timeout)
            try:
                if random.randint(0, 2):
                    self.figure.move(random.randint(0, 2)-1)
                else:
                    self.figure.rotate()
            except gameException:
                pass
            try:
                self.figure.moveDown()
            except gameExceptDestroy:
                self.area.clearLines()
                try:
                    self.figure = gameFigure(self.area)
                except gameExceptLose:
                    print 'You loser!!!'
                    sys.exit()
