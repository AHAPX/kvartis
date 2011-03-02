from OpenGL.GL import *

def drawCube(size, x, y, z, color = (1, 1, 1)):
    r, g, b = color
    glPushMatrix()
    glTranslated(x, y, z)

    glBegin(GL_QUADS)
    glColor4f(r*0.99, g*0.99, b*0.99, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(size, 0, 0)
    glVertex3f(size, size, 0)
    glVertex3f(0, size, 0)
        
    glColor4f(r*0.98, g*0.98, b*0.98, 0.0)
    glVertex3f(0, 0, size)
    glVertex3f(size, 0, size)
    glVertex3f(size, size, size)
    glVertex3f(0, size, size)

    glColor4f(r*0.97, g*0.97, b*0.97, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(size, 0, 0)
    glVertex3f(size, 0, size)
    glVertex3f(0, 0, size)
        
    glColor4f(r*0.96, g*0.96, b*0.96, 0.0)
    glVertex3f(0, size, 0)
    glVertex3f(size, size, 0)
    glVertex3f(size, size, size)
    glVertex3f(0, size, size)
        
    glColor4f(r*0.95, g*0.95, b*0.95, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, size)
    glVertex3f(0, size, size)
    glVertex3f(0, size, 0)
        
    glColor4f(r, g, b, 0.5)
    glVertex3f(size, 0, 0)
    glVertex3f(size, 0, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, 0)
    glEnd()

    glPopMatrix()

def drawFrame(size, x, y, z, len_x, len_y, len_z, color = (1, 1, 1)):
    r, g, b = color
    glPushMatrix()
    glTranslated(x, y, z)

    glBegin(GL_QUADS)
    glColor4f(r, g, b, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(size*len_x, 0, 0)
    glVertex3f(size*len_x, 0, size*len_z)
    glVertex3f(0, 0, size*len_z)

    glVertex3f(0, size*len_y, 0)
    glVertex3f(size*len_x, size*len_y, 0)
    glVertex3f(size*len_x, size*len_y, size*len_z)
    glVertex3f(0, size*len_y, size*len_z)

    glVertex3f(0, 0, 0)
    glVertex3f(0, size*len_y, 0)
    glVertex3f(0, size*len_y, size*len_z)
    glVertex3f(0, 0, size*len_z)

    glVertex3f(size*len_x, 0, 0)
    glVertex3f(size*len_x, size*len_y, 0)
    glVertex3f(size*len_x, size*len_y, size*len_z)
    glVertex3f(size*len_x, 0, size*len_z)

    glVertex3f(0, 0, 0)
    glVertex3f(size*len_x, 0, 0)
    glVertex3f(size*len_x, size*len_y, 0)
    glVertex3f(0, size*len_y, 0)

    glEnd()

    glPopMatrix()

