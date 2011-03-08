from PySide import QtCore, QtGui, QtNetwork
#from PyQt4 import QtCore, QtGui, QtNetwork
import kernel

class netException(kernel.gameException): pass
class netExceptRunServer(netException): pass
class netExceptConnectToHost(netException): pass

class netSocket(QtCore.QTcpSocket):
    def connectToHost(self, host, port):
        QtCore.QTcpSocket.connectToHost(self, host, port)
        return self.waitToConnected(30)

class gameServer(QtCore.QTcpServer):
    sockets = []
    receive = QtCore.Signal(str)
    newConnected = QtCore.Signal()
    newConnected = QtCore.Signal()

    def runServer(self, port):
        self.newConnection.connect(self.newConnect)
        return self.listen(port = port)

    def newConnect(self):
        socket = self.nextPendingConnection()
        socket.disconnected.connect(self.delConnect(len(self.sockets)))
        self.socket.readyRead.connect(self.receiveMessage(len(self.sockets)))
        self.newConnected.emit()

    def delConnect(self):
        del self

class gameSocket(QtCore.QObject):
    connected = False
    receive = QtCore.Signal(str)
    newConnected = QtCore.Signal()

    def runServer(self, port):
        self.server = QtNetwork.QTcpServer()
        self.server.newConnection.connect(self.newConnect)
        if self.server.listen(port = port):
            return True
        raise netExceptRunServer

    def newConnect(self):
        self.socket = self.server.nextPendingConnection()
        self.socket.disconnected.connect(self.delConnect)
        self.socket.readyRead.connect(self.receiveMessage)
        self.connected = True
        self.newConnected.emit()

    def delConnect(self):
        del self.socket
        self.connected = False

    def connectToHost(self, host, port):
        self.socket = QtNetwork.QTcpSocket()
        self.socket.connectToHost(host, port)
        if self.socket.waitForConnected(100):
            self.socket.disconnected.connect(self.disconnectFromHost)
            self.socket.readyRead.connect(self.receiveMessage)
            self.connected = True
        else:
            raise netExceptConnectToHost

    def disconnectFromHost(self):
        self.socket.disconnectFromHost()
        self.connected = False

    def sendMessage(self, message):
        if self.connected:
            self.socket.write(message)

    def receiveMessage(self):
        self.receive.emit(str(self.socket.readAll()))

if __name__ == '__main__':
    app = QtGui.QApplication(['serv'])
    serv = gameSocket()
    serv.runServer(6789)
    serv.connectToHost('localhost', 6789)
    app.exec_()
