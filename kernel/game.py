import glWindow
from PySide import QtCore, QtGui, QtNetwork
import glkernel, kernel, server

class netException(kernel.gameException): pass
class netExceptRunServer(netException): pass
class netExceptConnectToHost(netException): pass

class mainWindow(QtGui.QMainWindow):
    def __init__(self, width, height):
        QtGui.QMainWindow.__init__(self)
        self.setFixedSize(width, height)
        self.widget = glWindow.gameWidget(self, width, height)
        self.setCentralWidget(self.widget)

        self.socket = None
        self.timer = QtCore.QTimer(self.widget)
        self.timer.timeout.connect(self.moveDown)

        self.zones = {'main': glkernel.glZone(-0.3, -0.5, -0.5, 10, 20)}
        self.widget.zones = self.zones
        self.timer.start(500)
        self.grabKeyboard()

    def newConnect(self, name):
#        self.setFixedSize(500*2, height)
#        self.widget.setFizedSize(500*2, height)
        x, y, z = 0 + (len(self.zones)-1)*0.2, -0.5, -0.5
        self.zones[name] = glkernel.glZone(x, y, z, 10, 20)
        self.send('%s,dump:%s|' % (name, self.zones['main'].dump()))

    def delConnect(self, name):
        del self.zones[name]

    def connectToHost(self, host, port = 8128):
        self.socket = QtNetwork.QTcpSocket()
        self.socket.connectToHost(host, port)
        if self.socket.waitForConnected(1000):
            self.socket.readyRead.connect(self.receiveMessage)
            self.socket.write('*,dump:%s|' % self.zones['main'].dump())
        else:
            raise netExceptConnectToHost

    def disconnectFromHost(self):
        self.zones['main'].socket.disconnectFromHost()
        del self.zones['main'].socket

    def receiveMessage(self):
        self.actionOp(str(self.socket.readAll()))

    def send(self, message):
        if self.socket:
            self.socket.write(message)

    def actionOp(self, message):
        for msg in message.split('|'):
            try:
                zone_id, msg = msg.split(',', 1)
                zone = self.zones[zone_id]
            except ValueError:
                pass
            except KeyError:
                pass
#                print zone_id, msg, self.zones
            try:
                if msg == 'newConnect':
#                    print zone_id, 'newConnect'
                    self.newConnect(zone_id)
                elif msg == 'delConnect':
                    self.delConnect(zone_id)
                elif msg == 'attach':
                    zone.figure.attachToArea()
                elif msg == 'move_left':
                    zone.figure.move(x = -1)
                elif msg == 'move_right':
                    zone.figure.move(x = 1)
                elif msg == 'move_down':
                    zone.figure.move(y = 1)
                elif msg == 'rotate':
                    zone.figure.rotate(-1)
                elif msg.startswith('next_figure:'):
                    zone.newFigure()
                    zone.next_figure.load(msg.split(':', 1)[1])
                elif msg == 'sync':
                    self.send('*,dump:%s|' % self.zones['main'].dump())
                elif msg.startswith('dump:'):
                    zone.load(msg.split(':', 1)[1])
            except kernel.gameExceptMove:
                self.send('%s,sync|' % zone_id)
            except:
                pass
        self.widget.updateGL()
 
    def moveDown(self):
        try:
            self.zones['main'].moveDown()
            self.send('*,move_down|')
        except kernel.gameExceptLose:
            self.timer.stop()
        except kernel.gameExceptNewFigure:
            self.send('*,attach|')
            self.send('*,next_figure:%s|' % self.zones['main'].next_figure.dump())
            self.timer.stop()
            self.timer.start(500)
        self.widget.updateGL()

    def keyPressEvent(self, event):
        try:
            if event.key() == QtCore.Qt.Key_Left:
                self.zones['main'].figure.move(x = -1)
                self.send('*,move_left|')
            elif event.key() == QtCore.Qt.Key_Right:
                self.zones['main'].figure.move(x = 1)
                self.send('*,move_right|')
            elif event.key() == QtCore.Qt.Key_Down:
                self.zones['main'].figure.move(y = 1)
                self.send('*,move_down|')
            elif event.key() == QtCore.Qt.Key_Up:
                self.zones['main'].figure.rotate(-1)
                self.send('*,rotate|')
            elif event.key() == QtCore.Qt.Key_Space:
                self.timer.stop()
                self.timer.start(10)
            elif event.key() == QtCore.Qt.Key_H:
                self.server = server.gameServer()
                self.server.runServer()
            elif event.key() == QtCore.Qt.Key_J:
                self.connectToHost('localhost')
            self.widget.updateGL()
        except:
            pass

if __name__ == '__main__':
    app = QtGui.QApplication(['kvartis'])
    window = mainWindow(500, 500)
    window.show()
    app.exec_()
