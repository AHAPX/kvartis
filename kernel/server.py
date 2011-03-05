from PyQt4 import QtCore, QtGui, QtNetwork
import kernel

class netException(kernel.gameException): pass
class netExceptRunServer(netException): pass

class gameSocket():
    def runServer(self, port):
        self.server = QtNetwork.QTcpServer()
        QtCore.QObject.connect(self.server, QtCore.SIGNAL('newConnection()'), self.addConnect)
        if self.server.listen(port = port):
            return True
        raise netExceptRunServer

    def addConnect(self):
        self.socket = self.server.nextPendingConnection()
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL('disconnected()'), self.delConnect)
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL('readyRead()'), self.receiveMessage)

    def delConnect(self):
        del self.socket

    def connectToHost(self, host, port):
        self.socket = QtNetwork.QTcpSocket()
        self.socket.connectToHost(host, port)
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL('disconnected()'), self.disconnectFromHost)
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL('readyRead()'), self.receiveMessage)

    def disconnectFromHost(self):
        self.socket.disconnectFromHost()

    def sendMessage(self, message):
        self.socket.write(message)

    def receiveMessage(self):
        print str(self.socket.readAll())


class myServer(QtGui.QWidget):
    def __init__(self, width, height):
        QtGui.QWidget.__init__(self)
        self.setFixedSize(width, height)
        layout = QtGui.QVBoxLayout()
        self.label1 = QtGui.QLabel()
        self.label2 = QtGui.QLabel()
        self.button1 = QtGui.QPushButton('New server')
        self.button2 = QtGui.QPushButton('Connect to server')

        self.edit1 = QtGui.QLineEdit()
        self.button3 = QtGui.QPushButton('Send')
        self.label_mesg = QtGui.QLabel()
        self.button3.setDefault(True)

        group = QtGui.QGroupBox()
        layout_chat = QtGui.QVBoxLayout()
        layout_chat.addWidget(self.edit1)
        layout_chat.addWidget(self.button3)
        layout_chat.addWidget(self.label_mesg)
        layout_chat.addStretch()
        group.setLayout(layout_chat)

        self.edit1.setEnabled(False)
        self.button3.setEnabled(False)
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(group)
        self.setLayout(layout)
        QtCore.QObject.connect(self.button1, QtCore.SIGNAL('clicked()'), self.newServer)
        QtCore.QObject.connect(self.button2, QtCore.SIGNAL('clicked()'), self.connectToServer)
        QtCore.QObject.connect(self.button3, QtCore.SIGNAL('clicked()'), self.sendMessage)

    def newServer(self):
        self.server = QtNetwork.QTcpServer()
        QtCore.QObject.connect(self.server, QtCore.SIGNAL('newConnection()'), self.newConnect)
        if self.server.listen(port = 8765):
            self.label1.setText('Server active')
        else:
            self.label1.setText('Error')

    def connectToServer(self):
        self.socket = QtNetwork.QTcpSocket()
        self.socket.connectToHost('localhost', 8765)
        self.label1.setText('Connect to server')
        self.button2.setText('Disconnect')
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL('disconnected()'), self.disconnect)
        QtCore.QObject.connect(self.button2, QtCore.SIGNAL('clicked()'), self.disconnect)
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL('readyRead()'), self.readMessage)
        self.edit1.setEnabled(True)
        self.button3.setEnabled(True)

    def disconnect(self):
        self.socket.disconnectFromHost()
        self.label1.setText('')
        self.button2.setText('Connect to server')
        QtCore.QObject.connect(self.button2, QtCore.SIGNAL('clicked()'), self.connectToServer)
        self.edit1.setEnabled(False)
        self.button3.setEnabled(False)

    def newConnect(self):
        self.socket = self.server.nextPendingConnection()
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL('disconnected()'), self.delConnect)
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL('readyRead()'), self.readMessage)
        self.label2.setText('Connect')
        self.edit1.setEnabled(True)
        self.button3.setEnabled(True)

    def delConnect(self):
        self.label2.setText('')
        self.edit1.setEnabled(False)
        self.button3.setEnabled(False)

    def sendMessage(self):
        self.socket.write(str(self.edit1.text()))
        self.edit1.setText('')

    def readMessage(self):
        self.label_mesg.setText(str(self.socket.readAll()))
        
if __name__ == '__main__':
    app = QtGui.QApplication(['serv'])
    window = myServer(200, 250)
    window.show()
    app.exec_()
