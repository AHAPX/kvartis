import kernel
from glObjects import *
import random

cube_size = 0.08

class glFigure(kernel.gameFigure):
    def __init__(self, area, x = None, y = 1, fig_id = -1, color = (1, 1, 1)):
        kernel.gameFigure.__init__(self, area, x, y, fig_id)
        self.color = color

    def paint(self):
        for cell in self.figure:
            drawCube(cube_size, cell[0]*cube_size + self.area.x, cell[1]*cube_size + self.area.y, 0, self.color)

class glArea(kernel.gameArea):
    def __init__(self, len_x, len_y, pos_x, pos_y):
        kernel.gameArea.__init__(self, len_x, len_y)
        self.x = pos_x
        self.y = pos_y

    def paint(self):
        drawFrame(cube_size, self.x, self.y, 0, self.len_x, self.len_y, 1, (0, 0.8, 0.5))
        for y in xrange(len(self.matrix)):
            for x in xrange(len(self.matrix[y])):
                if self.matrix[y][x]:
                    drawCube(cube_size, x*cube_size + self.x, y*cube_size + self.y, 0, (0.2, 0.6, 0.9))

class glZone(kernel.gameZone):
    def __init__(self, x, y, len_x = 10, len_y = 20):
#        kernel.gameZone.__init__(self)
        self.area = glArea(len_x, len_y, x, y)
        self.newFigure()

    def newFigure(self, x = None, y = 1, fig_id = -1, color = (1, 1, 1)):
        self.figure = glFigure(self.area, x, y, fig_id, color = [random.random() for i in xrange(3)])

    def paint(self):
        self.area.paint()
        self.figure.paint()

    def moveDown(self):
        try:
            self.figure.moveDown()
        except kernel.gameExceptDestroy:
            self.area.clearLines()
            self.newFigure()

