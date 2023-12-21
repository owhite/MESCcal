
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider

class MescalineSafe:
    # ha ha
    pass

class showData(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Streaming Data')

        self.layout = QVBoxLayout()

        self.labelKeys = ['new']
        self.labelNames = ['streaming window']
        self.createLabels()
        app_name = "Show data"
        app_desc = "Simple display of mesc values"

        self.setLayout(self.layout)
        self.setGeometry(200, 200, 400, 200)

    def updateLabels(self, d):
        for i, n in enumerate(self.new_list):
            t = "{0}: {1}".format(n, round(d[n],1))
            self.labelPtrs[i].setText(t)

    def removeLabels(self):
        for index, p in enumerate(self.labelPtrs):
            if p is not None:
                self.layout.removeWidget(p)
                p.deleteLater()
                self.labelPtrs[index] = None  # Set the corresponding element to None

    def createLabels(self):
        self.labelPtrs = []
        for i, p in enumerate(self.labelKeys):
            t = "{0}: {1}".format(self.labelKeys[i], self.labelNames[i])
            label = None
            label = QLabel(t, self)
            self.labelPtrs.append(label)
            self.layout.addWidget(self.labelPtrs[i])


    def receive_data(self, d):
        self.new_list = sorted(list(d.keys()))
        if self.labelKeys != self.new_list:
            self.removeLabels()

            self.labelKeys = []
            self.labelNames = []
            for n in self.new_list:
                self.labelKeys.append(n)
                self.labelNames.append(d[n])
            self.createLabels()
        else:
            self.updateLabels(d)

if __name__ == '__main__':
    # For testing purposes
    app = QApplication([])
    window = showData()
    window.show()
    sys.exit(app.exec_())
