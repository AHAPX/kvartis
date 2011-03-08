import glWindow
from PySide import QtCore, QtGui, QtNetwork
import glkernel, kernel

class netException(kernel.gameException): pass
class netExceptRunServer(netException): pass
class netExceptConnectToHost(netException): pass

class mainWindow(QtGui.QMainWindow):
    def __init__(self, width, height):
        QtGui.QMainWindow.__init__(self)
        self.setFixedSize(width, height)
        self.widget = glWindow.gameWidget(self, width, height)
        self.setCentralWidget(self.widget)

        self.timer = QtCore.QTimer(self.widget)
        self.timer.timeout.connect(self.moveDown)

        self.zones = [glkernel.glZone(-0.75, -0.5, -0.5, 10, 20)]
        self.widget.zones = self.zones
        self.timer.start(500)
#
#        self.socket = socket.gameSocket()
#        try:
#            self.socket.connectToHost('localhost', 8128)
#            self.isServer = True
#        except socket.netExceptConnectToHost:
#            self.socket.runServer(8128)
#            self.isServer = False
#        self.socket.receive.connect(self.actionOp)
#        self.socket.newConnected.connect(self.newConnect)
#        self.socket.sendMessage('sync')
        self.grabKeyboard()

    def runServer(self, port = 8128):
        self.server = QtNetwork.QTcpServer()
        self.server.newConnection.connect(self.newConnect)
        if not self.server.listen(port = port):
            raise netExceptRunServer

    def stopServer(self):
        self.server.stop()

    def newConnect(self):
        print 'connect new client'
        x, y, z = 0, -0.5, -0.5
        self.zones.append(glkernel.glZone(x, y, z, 10, 20))
        self.zones[-1].socket = self.server.nextPendingConnection()
        self.zones[-1].socket.disconnected.connect(self.delConnect(len(self.zones)-1))
        self.zones[-1].socket.readyRead.connect(self.receiveMessage(self.zones[-1]))
        self.zones[-1].socket.write('sync|')

    def delConnect(self, zone_id):
        def temp():
            del self.zones[zone_id]
            # change window
        return temp

    def receiveMessage(self, zone):
        def temp():
            return self.actionOp(str(zone.socket.readAll()), zone)
        return temp

    def writeToAll(self, message):
        for zone in self.zones:
            try:
                zone.socket.write(message)
            except AttributeError:
                pass

    def connectToHost(self, host, port = 8128):
        self.zones[0].socket = QtNetwork.QTcpSocket()
        self.zones[0].socket.connectToHost(host, port)
        if self.zone[0].socket.waitForConnected(100):
            self.zone[0].socket.readyRead.connect(self.receiveMessage(self.zones[0]))
            self.zone[0].socket.write('sync|')
        else:
            raise netExceptConnectToHost

    def disconnectFromHost(self):
        self.zones[0].socket.disconnectFromHost()
        del self.zones[0].socket

    def actionOp(self, message, zone = None):
        if not zone:
            return None
        for msg in message.split('|'):
            try:
                if msg == 'attach':
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
                    zone.socket.write('dump:%s|' % self.zones[0].dump())
                elif msg.startswith('dump:'):
                    zone.load(msg.split(':', 1)[1])
            except kernel.gameExceptMove:
                zone.socket.write('sync|')
        self.widget.updateGL()
 
    def moveDown(self):
        try:
            self.zones[0].moveDown()
            self.writeToAll('move_down|')
        except kernel.gameExceptLose:
            self.timer.stop()
        except kernel.gameExceptNewFigure:
            self.writeToAll('attach|')
            self.writeToAll('next_figure:%s|' % self.zones[0].next_figure.dump())
            self.timer.stop()
            self.timer.start(500)
        self.widget.updateGL()

    def keyPressEvent(self, event):
        try:
            if event.key() == QtCore.Qt.Key_Left:
                self.zones[0].figure.move(x = -1)
                self.writeToAll('move_left|')
            elif event.key() == QtCore.Qt.Key_Right:
                self.zones[0].figure.move(x = 1)
                self.writeToAll('move_right|')
            elif event.key() == QtCore.Qt.Key_Down:
                self.zones[0].figure.move(y = 1)
                self.writeToAll('move_down|')
            elif event.key() == QtCore.Qt.Key_Up:
                self.zones[0].figure.rotate(-1)
                self.writeToAll('rotate|')
            elif event.key() == QtCore.Qt.Key_Space:
                self.timer.stop()
                self.timer.start(10)
            elif event.key() == QtCore.Qt.Key_H:
                self.runServer()
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
