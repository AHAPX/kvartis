from PySide import PyCore, PyGui

class myInputDialog(QtGui.QDialog):
    def __init__(self, title, objects):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle(title)
        layout_main = QtGui.QVBoxLayout()
        self.objects = []
        for obj in objects:
            label = QtGui.QLabel(obj[0])
            self.objects.append(obj[1]())
            self.objects[-1].setText(str(obj[2]))
            if len(obj) > 3:
                self.objects[-1].setValidator(obj[3])
            layout = QtGui.QHBoxLayout()
            layout.addWidget(label)
            layout.addWidget(self.objects[-1])
            layout_main.addLayout(layout)
        button_ok = QtGui.QPushButton('OK')
        button_ok.clicked.connect(self.ok)
        button_cancel = QtGui.QPushButton('Cancel')
        button_cancel.clicked.connect(self.close)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(button_ok)
        layout.addWidget(button_cancel)

        layout_main.addStretch()
        layout_main.addLayout(layout)
        self.setLayout(layout_main)
        self.setModal(True)
        self.setWindowState(QtCore.Qt.WindowNoState)
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def ok(self):
        self.accept()

    def run(self):
        if self.exec_():
            for obj in self.objects:
                yield obj.text() 


