import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF, QSize

class colorSegmentRing(QWidget):
    def __init__(self):
        super().__init__()
        self.value_min = 400
        self.value_max = 2200
        self.value_total = 3200
        self.value = 2000

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        m = min(self.width(),self.height())
        bump = int(m * .125)
        rect_size = min(self.width() - bump, 
                        self.height() - bump)
        outer_rect = QRectF((self.width() - rect_size) // 2,
                            (self.height() - rect_size) // 2,
                            rect_size,
                            rect_size)
        inner_rect = QRectF((self.width() - rect_size + bump) // 2,
                            (self.height() - rect_size + bump) // 2,
                            rect_size - bump,
                            rect_size - bump)

        pen = QPen()
        pen.setWidth(1)
        painter.setPen(pen)

        colors = [Qt.red]
        colors = [Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.cyan, Qt.magenta]

        arc_length = 270
        extent1 = (self.value_min / self.value_total) * arc_length
        extent2 = ((self.value_max - self.value_min) / self.value_total) * arc_length
        extent3 = ((self.value_total - self.value_max) / self.value_total) * arc_length

        start_angle =  -90 - ((360 - arc_length) / 2) 

        ## block
        color = Qt.blue
        pen = QPen(QColor(color))
        pen.setWidth(int(bump / 2) + 2)
        painter.setPen(pen)

        painter.setBrush(QColor(color))
        painter.drawArc(outer_rect, int(start_angle * 16), int(extent1 * -16))
        painter.drawArc(inner_rect, int(start_angle * 16), int(extent1 * -16))

        start_angle -= extent1

        color = Qt.red
        pen = QPen(QColor(color))
        pen.setWidth(int(bump / 2) + 2)
        painter.setPen(pen)

        painter.setBrush(QColor(color))
        painter.drawArc(outer_rect, int(start_angle * 16), int(extent2 * -16))
        painter.drawArc(inner_rect, int(start_angle * 16), int(extent2 * -16))

        start_angle -= extent2

        color = Qt.blue
        pen = QPen(QColor(color))
        pen.setWidth(int(bump / 2) + 2)
        painter.setPen(pen)

        painter.setBrush(QColor(color))
        painter.drawArc(outer_rect, int(start_angle * 16), int(extent3 * -16))
        painter.drawArc(inner_rect, int(start_angle * 16), int(extent3 * -16))

        # fill area to indicate throttle
        color = Qt.black
        pen = QPen(QColor(color))
        pen.setWidth(1)
        painter.setPen(pen)

        bump *= 2
        center_rect = QRectF((self.width() - rect_size + bump) // 2, (self.height() - rect_size + bump) // 2, rect_size - bump, rect_size - bump)

        # Add another pie slice shape in the center
        color = QColor(Qt.black)
        if self.value > self.value_max:
            color = QColor(Qt.red)

        pen = QPen(color)
        pen.setWidth(1)
        painter.setPen(pen)

        extent = ((self.value_total - 700) / self.value_total) * arc_length

        start_angle =  -90 - ((360 - arc_length) / 2) + 5
        painter.setBrush(color)
        painter.drawPie(center_rect, int(start_angle * 16), int(extent * -16))

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return QSize(60, 60)  
        
def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setGeometry(100, 100, 800, 800)

    central_text_edit = QTextEdit()
    central_text_edit.setPlainText("This is a block of text.\nYou can add more text here.")

    main_window.setCentralWidget(central_text_edit)

    status_bar = main_window.statusBar()
    status_bar.setSizeGripEnabled(False)

    status_bar_widget = ColorSegmentRing()
    status_bar.addPermanentWidget(status_bar_widget, 1)

    main_window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
