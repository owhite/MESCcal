import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QRectF, QSize

class colorSegmentRing(QWidget):
    def __init__(self):
        super().__init__()
        self.value_min = 400
        self.value_max = 2200
        self.value_total = 3900
        self.value = 8
        self.ring_text = ''
        self.ring_text_size = 10

    def setMinMax(self, min, max):
        self.value_min = min
        self.value_max = max

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

        # extent = ((self.value_total - self.value) / self.value_total) * arc_length
        extent = ((self.value) / self.value_total) * arc_length

        start_angle =  -90 - ((360 - arc_length) / 2) + 5
        painter.setBrush(color)
        painter.drawPie(center_rect, int(start_angle * 16), int(extent * -16))
        
        label_font = QFont("Arial", self.ring_text_size)  # Set the desired font and size
        painter.setFont(label_font)
        label_rect = QRectF(center_rect.left(), center_rect.bottom() - 6, center_rect.width(), 20) 
        painter.drawText(label_rect, Qt.AlignCenter, self.ring_text)

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return QSize(60, 60)  
        
