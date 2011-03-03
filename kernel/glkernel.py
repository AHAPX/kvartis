import kernel
from glObjects import *
import random
from PyQt4 import QtCore

cube_size = 0.05
blind_y = 3

class glGameCube():
    def __init__(self, color = (1, 1, 1), blend = 1):
        self.color = color
        self.blend = blend

class glFigure(kernel.gameFigure):
    def __init__(self, area, x = None, y = 1, fig_id = -1, color = (1, 1, 1)):
        kernel.gameFigure.__init__(self, area, x, y, fig_id)
        self.cell = glGameCube(color)

    def paint(self, x = None, y = None, z = None, force = None):
        if not x: x = self.area.x
        if not y: y = self.area.y
        if not z: z = self.area.z
        for cell in self.figure:
            if force or cell[1] >= blind_y:
                drawCube(cube_size, cell[0]*cube_size + x, cell[1]*cube_size + y, -cube_size + z, self.cell.color, self.cell.blend)

    def paintGhost(self):
        x, y, z = self.area.x, self.area.y, self.area.z
        figure = self.figure
        for i in xrange(1, self.area.len_y):
            ghost = kernel.moveFigure(self.figure, y = i)
            if not self.movable(ghost):
                for cell in figure:
                    drawCube(cube_size, cell[0]*cube_size + x, cell[1]*cube_size + y, -cube_size + z, self.cell.color, 0.3)
                break
            figure = ghost

class glArea(kernel.gameArea):
    def __init__(self, len_x, len_y, pos_x, pos_y, pos_z):
        kernel.gameArea.__init__(self, len_x, len_y + blind_y)
        self.x = pos_x
        self.y = pos_y
        self.z = pos_z

    def paint(self):
        drawFrame(cube_size, self.x, self.y + blind_y*cube_size, self.z, self.len_x, self.len_y - blind_y, 1, (0, 0.8, 0.5))
        for y in xrange(len(self.matrix)):
            for x in xrange(len(self.matrix[y])):
                cell = self.matrix[y][x]
                if cell:
#                    drawCube(cube_size, x*cube_size + self.x, y*cube_size + self.y, -cube_size + self.z, cell.color, cell.blend)
                    drawCube(cube_size, x*cube_size + self.x, y*cube_size + self.y, -cube_size + self.z, (0.2, 0.6, 0.9))

class glZone(kernel.gameZone):
    def __init__(self, x, y, z, len_x = 10, len_y = 20):
#        kernel.gameZone.__init__(self)
        self.area = glArea(len_x, len_y, x, y, z)
        self.next_figure = glFigure(self.area)
        self.newFigure()

    def newFigure(self, x = None, y = 2, fig_id = -1, color = (1, 1, 1)):
        self.figure = self.next_figure
        self.next_figure = glFigure(self.area, x, y, fig_id, color = [random.random() for i in xrange(3)])
        for i in xrange(random.randint(0, 3)):
            self.next_figure.rotate()

    def paint(self):
        self.area.paint()
        self.figure.paint()
#        self.figure.paintGhost()
        self.next_figure.paint(self.area.x, self.area.y - 0.2, 0, force = True)

