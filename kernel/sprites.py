from OpenGL.GL import *
from OpenGL.GLU import *
from PySide import QtGui

class glSprite:
    def __init__(self, filename, size_one):
        self.image = QtGui.QImage(filename)
        x = self.image.size().width()
        self.count = x / size_one
        self.size = 1.0 / self.count

    def paint(self, x1, y1, x2, y2, number):
        glPushMatrix()
#        glLoadIdentity()
        gluOrtho2D(-1, 1, -1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(number * self.size, 0)
        glVertex3f(x1, y1, 0)
        glTexCoord2f(number * self.size, 1)
        glVertex3f(x1, y2, 0)
        glTexCoord2f((number + 1) * self.size, 1)
        glVertex3f(x2, y2, 0)
        glTexCoord2f((number + 1) * self.size, 0)
        glVertex3f(x2, y1, 0)
        glEnd()
        glPopMatrix()
        
class glSpriteText:
    def __init__(self, filename, size_one, width, height, text, parent = None):
        self.parent = parent
        self.sprite = glSprite(filename, size_one)
        self.width, self.height, self.text = width, height, text

    def paint(self, x, y, text):
        if self.parent:
            self.parent.bindTexture(self.sprite.image)
        for i in xrange(len(text)):
            k = self.text.find(text[i])
            if k > -1:
                self.sprite.paint(x + i * self.width, y, x  + (i + 1) * self.width, y + self.height, k)
