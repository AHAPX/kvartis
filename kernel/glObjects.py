from OpenGL.GL import *
import random

def drawCube(size, x, y, z, color = (1, 1, 1), blend = 1):
    r, g, b = color
    glPushMatrix()
    glTranslated(x, y, z)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0, 0, 1))
    glMaterialfv(GL_BACK, GL_DIFFUSE, (0, 1, 0))

    glBegin(GL_QUADS)
    glColor4f(1, 1, 1, blend)
#    glColor4f(r, g, b, blend)

    glNormal(0, 0, 1)

    glTexCoord2f(0, 0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(0, 1)
    glVertex3f(size, 0, 0)
    glTexCoord2f(1, 1)
    glVertex3f(size, size, 0)
    glTexCoord2f(1, 0)
    glVertex3f(0, size, 0)
        
    glNormal(0, -1, 0)
    glTexCoord2f(0, 0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(0, 1)
    glVertex3f(size, 0, 0)
    glTexCoord2f(1, 1)
    glVertex3f(size, 0, size)
    glTexCoord2f(1, 0)
    glVertex3f(0, 0, size)
        
    glNormal(1, 0, 0)
    glTexCoord2f(0, 0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(0, 1)
    glVertex3f(0, 0, size)
    glTexCoord2f(1, 1)
    glVertex3f(0, size, size)
    glTexCoord2f(1, 0)
    glVertex3f(0, size, 0)
        
    glNormal(-1, 0, 0)
    glTexCoord2f(0, 0)
    glVertex3f(size, 0, 0)
    glTexCoord2f(0, 1)
    glVertex3f(size, 0, size)
    glTexCoord2f(1, 1)
    glVertex3f(size, size, size)
    glTexCoord2f(1, 0)
    glVertex3f(size, size, 0)

    glNormal(0, 1, 0)
    glTexCoord2f(0, 0)
    glVertex3f(0, size, 0)
    glTexCoord2f(0, 1)
    glVertex3f(size, size, 0)
    glTexCoord2f(1, 1)
    glVertex3f(size, size, size)
    glTexCoord2f(1, 0)
    glVertex3f(0, size, size)
        
    glNormal(0, 0, -1)
    glTexCoord2f(0, 0)
    glVertex3f(0, 0, size)
    glTexCoord2f(0, 1)
    glVertex3f(size, 0, size)
    glTexCoord2f(1, 1)
    glVertex3f(size, size, size)
    glTexCoord2f(1, 0)
    glVertex3f(0, size, size)
    glEnd()

    glPopMatrix()

def drawFrame(size, x, y, z, len_x, len_y, len_z, color = (1, 1, 1)):
    r, g, b = color
    dt = -0.001
    glPushMatrix()
    glTranslated(x, y, z)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.2, 0.2, 0.2))
    glMaterialfv(GL_BACK, GL_DIFFUSE, (0.4, 0.2, 0.2))

    glBegin(GL_QUADS)
    glColor4f(r, g, b, 1)
    glNormal(0, -1, 0)
    glVertex3f(dt, dt, -dt)
    glVertex3f(size*len_x-dt, dt, -dt)
    glVertex3f(size*len_x-dt, dt, -(size*len_z-dt))
    glVertex3f(dt, dt, -(size*len_z-dt))

    glNormal(0, 1, 0)
    glVertex3f(dt, size*len_y-dt, -dt)
    glVertex3f(size*len_x-dt, size*len_y-dt, -dt)
    glVertex3f(size*len_x-dt, size*len_y-dt, -(size*len_z-dt))
    glVertex3f(dt, size*len_y-dt, -(size*len_z-dt))

    glNormal(1, 0, 0)
    glVertex3f(dt, dt, -dt)
    glVertex3f(dt, size*len_y-dt, -dt)
    glVertex3f(dt, size*len_y-dt, -(size*len_z-dt))
    glVertex3f(dt, dt, -(size*len_z-dt))

    glNormal(-1, 0, 0)
    glVertex3f(size*len_x-dt, dt, -dt)
    glVertex3f(size*len_x-dt, size*len_y-dt, -dt)
    glVertex3f(size*len_x-dt, size*len_y-dt, -(size*len_z-dt))
    glVertex3f(size*len_x-dt, dt, -(size*len_z-dt))

    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.5, 0.5, 0.5))
    glMaterialfv(GL_BACK, GL_DIFFUSE, (1, 0.5, 0.5))
    glColor4f(0, g*0.2, b*0.6, 1)
    glNormal(0, 0, 1)
    glVertex3f(dt, dt, -dt)
    glVertex3f(size*len_x-dt, dt, -dt)
    glVertex3f(size*len_x-dt, size*len_y-dt, -dt)
    glVertex3f(dt, size*len_y-dt, -dt)

    glEnd()

    glPopMatrix()

