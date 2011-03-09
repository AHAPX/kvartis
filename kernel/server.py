from PySide import QtCore, QtNetwork
import kernel

class netException(kernel.gameException): pass
class netExceptRunServer(netException): pass
class netExceptConnectToHost(netException): pass

class gameServer(QtNetwork.QTcpServer):
    counter = 0
    sockets = {}
    newConnected = QtCore.Signal()
    delConnected = QtCore.Signal(int)
    receive = QtCore.Signal(int, str)

    def runServer(self, port = 8128):
        self.newConnection.connect(self.newConnect)
        if not self.listen(port = port):
            raise netExceptRunServer

    def stopServer(self):
        self.stop()

    def newConnect(self):
        self.sockets[self.counter] = self.nextPendingConnection()
        self.sockets[self.counter].disconnected.connect(self.delConnect(self.counter))
        self.sockets[self.counter].readyRead.connect(self.receiveMessage(self.counter))
        self.newConnected.emit()
        for sock in self.sockets.keys()[:-1]:
            self.sockets[self.counter].write('%s,newConnect|' % sock)
        self.writeToAll('%s,newConnect|' % self.counter, self.counter)
        self.counter += 1

    def delConnect(self, socket_id):
        def temp():
            del self.sockets[socket_id]
            self.writeToAll('%s,delConnect|' % socket_id)
            self.delConnected.emit(socket_id)
        return temp

    def receiveMessage(self, socket_id):
        def temp():
            message = str(self.sockets[socket_id].readAll())
            for m in message.split('|'):
                if m:
#                print msg
                    sock_id, msg = m.split(',', 1)
                    msg = '%s,%s|' % (socket_id, msg)
                    if sock_id == '*':
#                        print 'hell', sock_id
                        self.writeToAll(msg, socket_id)
                    else:
                        self.sockets[int(sock_id)].write(msg)
            self.receive.emit(socket_id, message)
        return temp
        
    def writeToAll(self, message, exclude_socket = None):
        for i in self.sockets.keys():
            if i != exclude_socket:
                self.sockets[i].write(message)

