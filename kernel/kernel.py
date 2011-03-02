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
    6: ((0, 0), (-1, 0), (1, 0), (0, -1))}

class gameException(Exception): pass
class gameExceptMove(gameException): pass
class gameExceptDestroy(gameException): pass
class gameExceptLose(gameException): pass

class gameFigure:
    def __init__(self, area, x = None, y = 1, fig_id = -1):
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
            return reduce(lambda a, b: a and b, map(lambda a: (0 <= a[0] < self.area.len_x) and (0 <= a[1] < self.area.len_y), figure)) and (reduce(lambda a, b: a + b, [self.area.matrix[cell[1]][cell[0]] for cell in figure]) == 0)
        except:
            print figure
            raise gameExceptMove

    def rotate(self, direct = 1):
        figure = self.figure[:]
        for i in xrange(1, len(figure)):
            figure[i] = (figure[0][0] + (figure[i][1] - figure[0][1])*direct, figure[0][1] + (figure[0][0] - figure[i][0])*direct)
        if not self.movable(figure):
            raise gameExceptMove
        self.figure = figure

    def move(self, x = 0, y = 0):
        figure = map(lambda a: (a[0] + x, a[1] + y), self.figure)
        if not self.movable(figure):
            raise gameExceptMove
        self.figure = figure

    def moveDown(self):
        try:
            self.move(y = 1)
        except gameExceptMove:
            for fig in self.figure:
                self.area.matrix[fig[1]][fig[0]] = 1
            raise gameExceptDestroy

class gameArea:
    def __init__(self, len_x, len_y):
        self.len_x = len_x
        self.len_y = len_y
        self.matrix = [[0 for i in xrange(len_x)] for i in xrange(len_y)]

    def clearLines(self):
        matrix = []
        for line in self.matrix:
            if reduce(lambda a, b: a * b, line) == 0:
                matrix.append(line)
        for i in xrange(self.len_y-len(matrix)):
            matrix.insert(0, [0 for j in xrange(self.len_x)])
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
        self.figure = gameFigure(self.area)

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
