import math, sys

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtOpenGL import *
from glObjects import *
import glkernel
import kernel

d = 1

class gameWidget(QGLWidget):
    def __init__(self, parent, width, height):
        QGLWidget.__init__(self, parent)
        self.width = width
        self.height = height
        self.setMinimumSize(width, height)
        self.rx = 0
        self.ry = 0
        self.rz = 0.1
        self.zone = glkernel.glZone(-0.75, -0.5, -0.5, 10, 20)
        self.zone_op = glkernel.glZone(0.25, -0.5, -0.5, 10, 20)
        self.timer = QtCore.QTimer(self)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.moveDown)
        self.grabKeyboard()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glMultMatrixf(((1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
        glLineWidth(5)
#        gluLookAt(self.rx, self.ry, self.rz, 0, 0, -self.rz, 0, 3, 0)
        glRotate(self.rx, 1, 0, 0)
        glRotate(self.ry, 0, 1, 0)
        glTranslatef(0, 0, self.rz/100)
#        glRotate(self.rz, 0, 0, 1)
        self.zone.paint()
        self.zone_op.paint()
        glFlush()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(5.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 1, 0.1, 100.0)
#        glFrustum(-1.0, 1.0, -1.0, 1.0, 1, 10)
        glOrtho(-1, 1, -1, 1, 1, 2)
#        gluLookAt(1, 0, 0, 0, 0, 0, -1, 0, 0)
        glMatrixMode(GL_MODELVIEW)
    
    def initializeGL(self):
#        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glEnable(GL_DEPTH_TEST);
#        glEnable(GL_CULL_FACE);
#        glCullFace(GL_BACK)
        glLoadIdentity()
#        gluPerspective(45.0, self.width/self.height, 1.0, 100.0)
#        glFrustum(-1.0, 1.0, 1.0, -1.0, 1.0, 10.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glLightfv(GL_LIGHT2, GL_POSITION, (0.5, 1, -0.2))
        glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, (-1, -1, 0.3, 1))
        glLightfv(GL_LIGHT2, GL_DIFFUSE, (1, 1, 1, 1))
        glEnable(GL_LIGHT2)
        glLightfv(GL_LIGHT1, GL_POSITION, (-0.5, 1, -0.2))
        glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, (1, -1, 0.3, 1))
        glLightfv(GL_LIGHT1, GL_DIFFUSE, (1, 1, 1, 1))
        glEnable(GL_LIGHT1)
#        glLightfv(GL_LIGHT1, GL_POSITION, (0, -1, 0))
#        glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, (0, 1, 0, 0))
#        glLightfv(GL_LIGHT1, GL_DIFFUSE, (1, 1, 1, 1))
#        glEnable(GL_LIGHT1)
        glEnable(GL_NORMALIZE)
        glMatrixMode(GL_MODELVIEW)

    def keyPressEvent(self, event):
        try:
            if event.key() == QtCore.Qt.Key_Left:
                self.zone.figure.move(x = -1)
            elif event.key() == QtCore.Qt.Key_Right:
                self.zone.figure.move(x = 1)
            elif event.key() == QtCore.Qt.Key_Down:
                self.zone.figure.move(y = 1)
            elif event.key() == QtCore.Qt.Key_Up:
                self.zone.figure.rotate(-1)
            elif event.key() == QtCore.Qt.Key_Space:
                self.timer.stop()
                self.timer.start(10)
            elif event.key() == QtCore.Qt.Key_A:
                self.ry += d
            elif event.key() == QtCore.Qt.Key_D:
                self.ry -= d
            elif event.key() == QtCore.Qt.Key_W:
                self.rx += d
            elif event.key() == QtCore.Qt.Key_S:
                self.rx -= d
            elif event.key() == QtCore.Qt.Key_Z:
                self.rz += d
            elif event.key() == QtCore.Qt.Key_X:
                self.rz -= d
            elif event.key() == QtCore.Qt.Key_1:
                if glIsEnabled(GL_LIGHT1):
                    glDisable(GL_LIGHT1)
                else:
                    glEnable(GL_LIGHT1)
            elif event.key() == QtCore.Qt.Key_2:
                if glIsEnabled(GL_LIGHT2):
                    glDisable(GL_LIGHT2)
                else:
                    glEnable(GL_LIGHT2)
#            elif event.key() == QtCore.Qt.Key_A:
#                self.ry -= 20
#            elif event.key() == QtCore.Qt.Key_D:
#                self.ry += 20
#            elif event.key() == QtCore.Qt.Key_W:
#                self.rx -= 20
#            elif event.key() == QtCore.Qt.Key_S:
#                self.rx += 20
            self.updateGL()
        except:
            pass

    def moveDown(self):
        try:
            self.zone.moveDown()
            self.zone_op.moveDown()
        except kernel.gameExceptLose:
            self.timer.stop()
        except kernel.gameExceptNewFigure:
            self.timer.stop()
            self.timer.start(500)
        self.updateGL()

class mainWindow(QtGui.QMainWindow):
    def __init__(self, width, height):
        QtGui.QMainWindow.__init__(self)
        self.setFixedSize(width, height)
        widget = gameWidget(self, width, height)
        self.setCentralWidget(widget)
        widget.timer.start(500)
        
if __name__ == '__main__':
    app = QtGui.QApplication(['kvartis'])
    window = mainWindow(1000, 1000)
    window.show()
    app.exec_()
