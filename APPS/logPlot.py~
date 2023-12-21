import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets  # Import QtWidgets for correct attribute access

class MescalineSafe:
    # ha ha
    pass

class logPlot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.canvas = MatplotlibCanvas(self, width=5, height=4)
        self.layout.addWidget(self.canvas)

        self.button = QPushButton("Update Plot", self)
        # self.button.clicked.connect(self.canvas.update_plot)
        self.button.clicked.connect(self.send_log_request)
        self.layout.addWidget(self.button)

    #  so usually this gets data of the form: {'adc1': 0, 'ehz': 0.051 ....
    #    display that if you get it
    def receive_data(self, d):
        if d.get('vbus'): # bad test if we're getting status data
            p_y1 = float(d['vbus'])
            p_y2 = float(d['TMOS']) - 273.15
        if d.get('time'):
            self.canvas.update_plot(d)

    def send_log_request(self):
        text = 'log -fl \r\n'
        self.port.write( text.encode() )

    def set_port(self, p):
        self.port = p

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(width, height), dpi=dpi)

        self.axes = [ax1, ax2, ax3, ax4]

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_plot(self, streamDict):
        for ax in self.axes:
            ax.clear()

        # 'time',
        x = np.array(streamDict['time'])

        # 'Vbus.V.y1',
        y1_1 = np.array(streamDict['Vbus.V.y1'])

        # 'Iu.I_phase.y1', 'Iv.I_phase.y1', 'Iw.I_phase.y1',
        y2_1 = np.array(streamDict['Iu.I_phase.y1'])
        y2_2 = np.array(streamDict['Iv.I_phase.y1'])
        y2_3 = np.array(streamDict['Iw.I_phase.y1'])

        # 'Vd.V_dq.y1', 'Vq.V_dq.y1'
        y3_1 = np.array(streamDict['Vd.V_dq.y1'])
        y3_2 = np.array(streamDict['Vq.V_dq.y1'])

        # 'angle.misc.y1'
        y4_1 = np.array(streamDict['angle.misc.y1'])

        self.axes[0].plot(x, y1_1, label='Vbus')
        self.axes[0].set_title('Vbus')
        self.axes[0].set_ylim(0, np.max(y1_1) + int(np.max(y1_1) * .2))

        y = np.concatenate((y2_1, y2_2, y2_3), axis=None)
        min = np.min(y) 
        max = np.max(y)
        min = min - (abs(min) * .2)
        max = max + (max * .2)
        self.axes[1].plot(x, y2_1, label='Iu')
        self.axes[1].plot(x, y2_2, label='Iv')
        self.axes[1].plot(x, y2_3, label='Iw')
        self.axes[1].set_ylim(min, max)
        self.axes[1].set_title('I')
        self.axes[1].legend(loc='upper right')

        y = np.concatenate((y3_1, y3_2), axis=None)
        min = np.min(y) 
        max = np.max(y)
        min = min - (abs(min) * .2)
        max = max + (max * .2)
        self.axes[2].plot(x, y3_1, label='Vd')
        self.axes[2].plot(x, y3_2, label='Vq')
        self.axes[2].set_ylim(0, max)
        self.axes[2].set_title('Vd/Vq')
        self.axes[2].legend(loc='upper right')

        self.axes[3].plot(x, y4_1, label='angle')
        self.axes[3].set_title('Angle')
        self.axes[3].legend(loc='upper right')

        for ax in self.axes:
            ax.grid()

        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = logPlot()
    main_window.show()

    sys.exit(app.exec_())
