from OpenGL.GL import *
import sprites, random

class gameMode:
    def __init__(self, zone, widget = None):
        self.score = 0
        self.zone = zone
        self.zone.areaCleared.connect(self.cleared)
        self.sprite_score = sprites.glSpriteText('/home/anarchy/shared/projects/tetris/data/number.jpg', 30, 0.2, 0.3, '0123456789', widget)

    def cleared(self, count):
        self.score += int(count * 0.5 * (count + 1))

    def paint(self):
        self.sprite_score.paint(self.zone.area.x, 0.7, str(self.score))
#        self.sprite_score.paint(self.zone.area.x, self.zone.area.y - 0.4, str(self.score))

