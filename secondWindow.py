from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class secondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Second Window')

        self.layout = QVBoxLayout()

        self.labelKeys = ['new']
        self.labelNames = ['streaming window']
        self.createLabels()

        self.setLayout(self.layout)
        self.setGeometry(200, 200, 400, 200)

    def updateLabels(self):
        count = 0
        for k in self.labelKeys:
            count += 1

    def removeLabels(self):
        print("REMOVE")
        for index, p in enumerate(self.labelPtrs):
            if p is not None:
                print(" remove {0} :: {1}".format(index, p))
                self.layout.removeWidget(p)
                p.deleteLater()
                self.labelPtrs[index] = None  # Set the corresponding element to None

    def createLabels(self):
        print("CREATE")
        self.labelPtrs = []
        count = 0
        for p in self.labelKeys:
            t = "{0}: {1}".format(self.labelKeys[count], self.labelNames[count])
            print(t)
            label = None
            label = QLabel(t, self)
            self.labelPtrs.append(label)
            self.layout.addWidget(self.labelPtrs[0])
            count += 1

    def receive_data(self, d):
        self.new_list = sorted(list(d.keys()))

        print(self.new_list)
        print(self.labelNames)

        if self.labelNames != self.new_list:
            self.removeLabels()

            for n in self.new_list:

            self.createLabels()
            

if __name__ == '__main__':
    # For testing purposes
    app = QApplication([])
    window = secondWindow()
    window.show()
    sys.exit(app.exec_())
