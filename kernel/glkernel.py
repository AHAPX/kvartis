from kernel import *
from glObjects import *
import random
from PySide import QtCore
from cPickle import dumps, loads

cube_size = 0.05
blind_y = 3

class glGameCube():
    def __init__(self, color = (1, 1, 1), blend = 1):
        self.color = color
        self.blend = blend

class glFigure(gameFigure, QtCore.QObject):
    rotated, moved, unmovable = QtCore.Signal(), QtCore.Signal(), QtCore.Signal()

    def __init__(self, area, x = None, y = 1, fig = None, color = (1, 1, 1)):
        QtCore.QObject.__init__(self)
        gameFigure.__init__(self, area, x, y, fig)
        self.cell = glGameCube(color)

    def rotate(self, direct = 1):
        try:
            gameFigure.rotate(self, direct)
            self.rotated.emit()
            return True
        except gameExceptMove:
            self.unmovable.emit()
            raise gameExceptMove

    def move(self, x = 0, y = 0):
        try:
            gameFigure.move(self, x, y)
#            self.moved.emit()
            return True
        except gameExceptMove:
            self.unmovable.emit()
            raise gameExceptMove

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
            ghost = moveFigure(self.figure, y = i)
            if not self.movable(ghost):
                for cell in figure:
                    drawCube(cube_size, cell[0]*cube_size + x, cell[1]*cube_size + y, -cube_size + z, self.cell.color, 0.3)
                break
            figure = ghost

    def dump(self):
        return dumps(self.figure)

    def load(self, dump):
        self.figure = loads(str(dump))

class glArea(gameArea, QtCore.QObject):
    cleared = QtCore.Signal(int)

    def __init__(self, len_x, len_y, pos_x, pos_y, pos_z):
        QtCore.QObject.__init__(self)
        gameArea.__init__(self, len_x, len_y + blind_y)
        self.x = pos_x
        self.y = pos_y
        self.z = pos_z

    def clearLines(self):
        count = gameArea.clearLines(self)
        if count:
            self.cleared.emit(count)
        return count

    def paint(self):
        drawFrame(cube_size, self.x, self.y + blind_y*cube_size, self.z, self.len_x, self.len_y - blind_y, 1, (0, 0.8, 0.5))
        for y in xrange(len(self.matrix)):
            for x in xrange(len(self.matrix[y])):
                cell = self.matrix[y][x]
                if cell:
#                    drawCube(cube_size, x*cube_size + self.x, y*cube_size + self.y, -cube_size + self.z, cell.color, cell.blend)
                    drawCube(cube_size, x*cube_size + self.x, y*cube_size + self.y, -cube_size + self.z, (0.2, 0.6, 0.9))

    def dump(self):
        return dumps(self.matrix)

    def load(self, dump):
        self.matrix = loads(str(dump))

class glZone(gameZone, QtCore.QObject):
    figRotated, figMoved, figUnmovable, areaCleared = QtCore.Signal(), QtCore.Signal(), QtCore.Signal(), QtCore.Signal(int)

    def __init__(self, x, y, z, len_x = 10, len_y = 20, next_count = 1):
        QtCore.QObject.__init__(self)
        self.area = glArea(len_x, len_y, x, y, z)
        self.next_count = next_count
        self.next_fig = self.getNextFigures(self.area, count = self.next_count + 1)
        self.figure = self.next_fig.pop(0)
        self.area.cleared.connect(self.areaCleared)
        self.figure.rotated.connect(self.figRotated)
        self.figure.moved.connect(self.figMoved)
        self.figure.unmovable.connect(self.figUnmovable)

    def newFigure(self):
#        self.figure.rotated.disconnect()
#        self.figure.moved.disconnect()
#        self.figure.unmovable.disconnect()
        gameZone.newFigure(self)
        self.figure.rotated.connect(self.figRotated)
        self.figure.moved.connect(self.figMoved)
        self.figure.unmovable.connect(self.figUnmovable)        

    def getNextFigures(self, area, next = [], count = 1):
        next_res = next[:]
        for i in xrange(count - len(next)):
            next_res.append(glFigure(area))
        return next_res

    def paint(self):
        self.area.paint()
        self.figure.paint()
#        self.figure.paintGhost()
        self.next_fig[0].paint(self.area.x, self.area.y - 0.2, 0, force = True)

    def dump(self):
        return dumps((self.area.dump(), self.figure.dump(), self.next_fig[0].dump()))

    def load(self, dump):
        area, figure, next_fig = loads(str(dump))
        self.area.load(area)
        self.figure.load(figure)
        self.next_fig = self.getNextFigures(self.area, count = self.next_count + 1)
        self.next_fig[0].load(next_fig) 

