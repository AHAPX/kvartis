import math, sys

from OpenGL.GL import *
from OpenGL.GLU import *
from PySide import QtGui, QtCore
from PySide.QtOpenGL import *
from glObjects import *

class gameGLWidget(QGLWidget):
    zone = None

    def __init__(self, parent, width, height):
        QGLWidget.__init__(self, parent)
        self.width = width
        self.height = height
        self.setMinimumSize(width, height)
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glMultMatrixf(((1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
#        gluLookAt(self.rx, self.ry, self.rz, 0, 0, -self.rz, 0, 3, 0)
        glColor4f(1, 1, 1, 1)

#        glBegin(GL_TRIANGLES)
#        glVertex3f(-0.1, 0, -0.7)
#        glVertex3f(0.1, 0, -0.7)
#        if self.isServer:
#            glVertex3f(0, 0.1, -0.7)
#        else:
#            glVertex3f(0, -0.1, -0.7)
#        glEnd()
        if self.zone:
            self.zone.paint()
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
#        glViewport(0, 0, 1280, 768)
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
        glEnable(GL_NORMALIZE)
        glMatrixMode(GL_MODELVIEW)
