import glWindow
from PySide import QtCore, QtGui, QtNetwork
import glkernel, kernel, server, random

class netException(kernel.gameException): pass
class netExceptRunServer(netException): pass
class netExceptConnectToHost(netException): pass

class gameWidget(QtGui.QWidget):
    socket, begin_widgets = None, []

    def __init__(self, width, height, len_x, len_y, count_op = 0):
        QtGui.QWidget.__init__(self)
#        QtGui.QMainWindow.__init__(self)
        self.setFixedSize(width*(count_op + 1), height)
#        self.setMinimumSize(width, height)       

        self.len_x, self.len_y = len_x, len_y
        self.socket = None
        self.widgets = {'main': glWindow.gameGLWidget(self, width, height)}
        self.widgets['main'].zone = glkernel.glZone(-glkernel.cube_size*len_x/2, -glkernel.cube_size*len_y/2, -0.6, len_x, len_y)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.moveDown)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.widgets['main'])
        self.setLayout(layout)
        for i in xrange(count_op):
            self.begin_widgets.append(glWindow.gameGLWidget(self, width, height))            
            layout.addWidget(self.begin_widgets[-1])

        self.timer.start(500)
        self.grabKeyboard()

    def newConnect(self, name):
        try:
            self.widgets[name] = self.begin_widgets.pop(0)
            self.widgets[name].zone = glkernel.glZone(-glkernel.cube_size*self.len_x/2, -glkernel.cube_size*self.len_y/2, -0.6, self.len_x, self.len_y)
            self.send('%s,dump:%s|' % (name, self.widgets['main'].zone.dump()))
            self.setFixedSize(self.widgets['main'].width()*len(self.widgets), self.height())
#            self.layout().itemAt(0).addWidget(self.widgets[name])
        except IndexError:
            pass

    def delConnect(self, name):
        self.begin_widgets.append(self.widgets.pop(name))
        del self.begin_widgets[-1].zone
        self.begin_widgets[-1].updateGL()

    def connectToHost(self, host, port = 8128):
        self.socket = QtNetwork.QTcpSocket()
        self.socket.connectToHost(host, port)
        if self.socket.waitForConnected(1000):
            self.socket.readyRead.connect(self.receiveMessage)
            self.socket.write('*,dump:%s|' % self.widgets['main'].zone.dump())
        else:
            raise netExceptConnectToHost

    def disconnectFromHost(self):
        self.socket.disconnectFromHost()
        del self.socket

    def receiveMessage(self):
        self.actionOp(str(self.socket.readAll()))

    def send(self, message):
        if self.socket:
            self.socket.write(message)

    def actionOp(self, message):
        for msg in message.split('|'):
            try:
                zone_id, msg = msg.split(',', 1)
                zone = self.widgets[zone_id].zone
            except (ValueError, KeyError):
                pass
            try:
                if msg == 'newConnect':
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
                    self.send('*,dump:%s|' % self.widgets['main'].zone.dump())
                elif msg.startswith('dump:'):
                    zone.load(msg.split(':', 1)[1])
            except kernel.gameExceptMove:
                self.send('%s,sync|' % zone_id)
            except:
                pass
        try:
            self.widgets[zone_id].updateGL()
        except (ValueError, KeyError):
            pass
 
    def moveDown(self):
        try:
            self.widgets['main'].zone.moveDown()
            self.send('*,move_down|')
        except kernel.gameExceptLose:
            self.timer.stop()
        except kernel.gameExceptNewFigure:
            self.send('*,attach|')
            self.send('*,next_figure:%s|' % self.widgets['main'].zone.next_figure.dump())
            self.timer.stop()
            self.timer.start(500)
        self.widgets['main'].updateGL()

    def keyPressEvent(self, event):
        try:
            if event.key() == QtCore.Qt.Key_Left:
                self.widgets['main'].zone.figure.move(x = -1)
                self.send('*,move_left|')
            elif event.key() == QtCore.Qt.Key_Right:
                self.widgets['main'].zone.figure.move(x = 1)
                self.send('*,move_right|')
            elif event.key() == QtCore.Qt.Key_Down:
                self.widgets['main'].zone.figure.move(y = 1)
                self.send('*,move_down|')
            elif event.key() == QtCore.Qt.Key_Up:
                self.widgets['main'].zone.figure.rotate(-1)
                self.send('*,rotate|')
            elif event.key() == QtCore.Qt.Key_Space:
                self.timer.stop()
                self.timer.start(10)
            elif event.key() == QtCore.Qt.Key_M:
                x = random.randint(300, 1000)
                self.setFixedSize(x, x)
#                self.setMaximumWidth(300)
            self.widgets['main'].updateGL()
        except:
            pass

class mainWindow(QtGui.QMainWindow):
    game_widget = None

    def __init__(self, width, height):
        QtGui.QMainWindow.__init__(self)
        self.setMinimumSize(width, height)
        menu = QtGui.QMenuBar()
        menu_game = menu.addMenu('Game')
        menu_game.addAction('New game').triggered.connect(self.newGame)
        menu_game.addAction('Stop Game').triggered.connect(self.stopGame)
        menu_game.addSeparator()
        menu_game.addAction('Exit').triggered.connect(lambda:app.quit())

        menu_net = menu.addMenu('Network')
        self.act_server = menu_net.addAction('Start server')
        self.act_server.setCheckable(True)
        self.act_server.toggled.connect(self.runServer)
        self.act_client = menu_net.addAction('Connect to server')
        self.act_client.setCheckable(True)
        self.act_client.toggled.connect(self.connectToHost)
        menu.addAction('Options').triggered.connect(lambda:None)
        self.setMenuBar(menu)

    def newGame(self, count_players = 0):
        w, h = 500, 500
        self.game_widget = gameWidget(w, h, 10, 20, count_players)
        self.setFixedSize(w*(count_players + 1), h + 30)
        self.setCentralWidget(self.game_widget)

    def stopGame(self):
        if self.game_widget:
            self.game_widget.close()
            del self.game_widget
            self.game_widget = None
            self.setFixedSize(300, 200)

    def runServer(self, run):
        if run:
            self.act_server.setText('Stop server')
            self.act_client.setEnabled(False)
            self.newGame(1)
            self.server = server.gameServer()
            self.server.runServer()
            self.game_widget.connectToHost('localhost')
        else:
            self.act_server.setText('Start server')
            self.act_client.setEnabled(True)
            self.game_widget.disconnectFromHost()
            self.server.stopServer()
            self.stopGame()

    def connectToHost(self, run):
        if run:
            self.act_client.setText('Disconnect')
            self.act_server.setEnabled(False)
            self.newGame(1)
            self.game_widget.connectToHost('localhost')
        else:
            self.act_client.setText('Connect to server')
            self.act_server.setEnabled(True)
            self.game_widget.disconnectFromHost()
            self.stopGame()

def test():
    app = QtGui.QApplication(['kvartis'])
    window = mainWindow(300, 200)
    window.show()
    app.exec_()

if __name__ == '__main__':
    app = QtGui.QApplication(['kvartis'])
    window = mainWindow(300, 200)
    window.show()
    app.exec_()
