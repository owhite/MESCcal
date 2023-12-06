from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class secondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Second Window')

        self.layout = QVBoxLayout()
        self.old_list = ['new']
        self.new_list = []

        self.labels = []

        self.label_list = {}
        self.label_list['new'] = QLabel('streaming window', self)
        self.layout.addWidget(self.label_list['new'])

        self.setLayout(self.layout)
        self.setGeometry(200, 200, 400, 200)

    def receive_data(self, d):
        print("widget count {0}".format(self.layout.count()))

        i = 0
        while i < self.layout.count():
            item = self.layout.takeAt(i)
            widget = item.widget()
            if widget and isinstance(widget, QLabel):
                pass
            i += 1

        self.new_list = sorted(list(d.keys()))
        print(self.old_list)
        print(self.new_list)

        if self.old_list != self.new_list:
            self.old_list = self.new_list
            print("removing")
            print(self.old_list)
            print(self.new_list)

            self.layout = QVBoxLayout()
            for name in self.new_list:
                self.label_list[name] = QLabel(name, self)
                self.layout.addWidget(self.label_list[name])

        for name in self.new_list:
            print("  {0} :: {1}".format(name, d[name]))
            self.label_list[name].setText(str(d[name]))

        self.setLayout(self.layout)

        
