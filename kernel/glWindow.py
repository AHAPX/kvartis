import math, sys

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtOpenGL import *
from glObjects import *
import glkernel
from kernel import gameException, gameExceptLose

class gameWidget(QGLWidget):
    def __init__(self, parent, width, height):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(width, height)
        self.zone = glkernel.glZone(-0.5, -0.8, 10, 20)
        self.timer = QtCore.QTimer(self)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.moveDown)
        action_left = QtGui.QAction(self)
        action_left.setShortcut('Ctrl+D')
        QtCore.QObject.connect(action_left, QtCore.SIGNAL('triggered()'), self.moveFigure)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotate(180, 0, 0, 1)
        self.zone.paint()
#        drawCube(0.2, 0, 0, 0)
        glFlush()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 1.0, 30.0)
    
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(5.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 1.0, 30.0)

    def moveDown(self):
        try:
            self.zone.moveDown()
        except gameExceptLose:
            self.timer.stop()
#            sys.exit()
        self.updateGL()

    def moveFigure(self, x = 1, y = 0):
        try:
            self.zone.figure.move(x, y)
        except gameException:
            pass

class mainWindow(QtGui.QMainWindow):
    def __init__(self, width, height):
        QtGui.QMainWindow.__init__(self)
        self.setFixedSize(width, height)
        widget = gameWidget(self, width, height)
        self.setCentralWidget(widget)
        widget.timer.start(100)
        
if __name__ == '__main__':
    app = QtGui.QApplication(['kvartis'])
    window = mainWindow(500, 500)
    window.show()
    app.exec_()
