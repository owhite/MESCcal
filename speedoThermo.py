import math

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRectF, QSize, QPoint
from PyQt5.QtGui import QPen, QPainter, QPainterPath, QTransform, QFont

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPolygon

class SpeedoThermo(QWidget):
    def __init__(self, x, y, radius, width, min_temp, max_temp, show, name):
        super().__init__()
        self.origin_x = x
        self.origin_y = y
        self.radius = radius
        self.app_width = width
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.show_temps = show
        self.name = name

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.angle_range = 56

        self.initUI()

    def initUI(self):
        self.angle = 0
        self.setThermoTemp(self.min_temp)
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        green = QColor(46, 125, 50)

        # magic nums to draw the lil segments
        self.drawArc(painter, self.origin_x, self.origin_y, green, self.radius, -self.angle_range, 6, self.app_width)
        self.drawArc(painter, self.origin_x, self.origin_y, green, self.radius, -self.angle_range + 14, 38, self.app_width)
        self.drawArc(painter, self.origin_x, self.origin_y, green, self.radius, 4, 38, self.app_width)
        self.drawArc(painter, self.origin_x, self.origin_y, Qt.red, self.radius, self.angle_range-6, 6, self.app_width)

        if self.show_temps:
            label_font = QFont("Futura", 32) 
            label_font.setBold(True)
            painter.setFont(label_font)
            font_color = QColor(255, 255, 255) 
            painter.setPen(font_color)

            (x, y) = self.get_radial_point(self.origin_x, self.origin_y, self.radius + (self.app_width * 2.4), -56)
            label_rect = QRectF(x-40, y, 100, 40)
            painter.drawText(label_rect, Qt.AlignCenter, str(self.min_temp))

            (x, y) = self.get_radial_point(self.origin_x, self.origin_y, self.radius + (self.app_width * 2.4), 56)
            label_rect = QRectF(x-60, y, 100, 40)
            painter.drawText(label_rect, Qt.AlignCenter, str(self.max_temp))

        # lil circle
        d = int(self.radius * .7)
        x = int(self.origin_x - (d / 2))
        y = int(self.origin_y - (d / 2))
        painter.setBrush(QColor(Qt.yellow))
        painter.setPen(QPen(QColor(Qt.black), 1, Qt.SolidLine))
        painter.drawEllipse(x, y, d, d)

        # bottom label with name
        label_font = QFont("Futura", 22) 
        label_font.setBold(True)
        painter.setFont(label_font)
        painter.setPen(QPen(QColor(Qt.white), 1, Qt.SolidLine))
        label_rect = QRectF(x, y + d, 100, 50)
        painter.drawText(label_rect, Qt.AlignCenter, str(self.name))

        # Create a transformation matrix for rotation
        transform = QTransform()
        transform.translate(self.origin_x, self.origin_y)
        transform.rotate(self.angle)
        transform.translate(-self.origin_x, -self.origin_y)
        painter.setTransform(transform)

        # draw the triangle
        triangle = QPolygon([
            QPoint(self.origin_x, int(self.origin_y - self.radius - (self.app_width/2))),
            QPoint(self.origin_x - 8, self.origin_y),
            QPoint(self.origin_x + 8, self.origin_y)
        ])
        painter.setBrush(QColor(255, 143, 0))
        painter.drawPolygon(triangle)

    def drawArc(self, painter, origin_x, origin_y, color, radius, start_angle, span_angle, width):
        painter.setPen(QPen(color, 1, Qt.SolidLine))

        # Calculate points for the arc
        arc_points1 = self.calculate_arc_points(origin_x, origin_y, radius, start_angle, span_angle)
        arc_points2 = self.calculate_arc_points(origin_x, origin_y, radius + width, start_angle, span_angle)
        arc_points2.reverse()

        path = QPainterPath()
        path.moveTo(arc_points1[0])
        for point in arc_points1:
            path.lineTo(point)

        path.lineTo(arc_points2[0])
        for point in arc_points2:
            path.lineTo(point)

        path.lineTo(arc_points1[0])

        painter.setBrush(color)
        painter.drawPath(path)

    def setThermoTemp(self, angle):
        # self.angle = 0 is straight up
        r = self.max_temp - self.min_temp
        
        self.angle = self.map_range(angle, self.min_temp, self.max_temp, (-1 * self.angle_range), self.angle_range)
        self.update()

    def map_range(self, x, in_min, in_max, out_min, out_max):
        return ((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)


    def get_radial_point(self, x, y, radius, angle):
        angle += 270
        x = int(x + radius * math.cos(angle * math.pi / 180))
        y = int(y + radius * math.sin(angle * math.pi / 180))
        return(x, y)

    def calculate_arc_points(self, origin_x, origin_y, radius, start_angle, span_angle):
        start_angle += 270

        # Calculate the points on the arc
        arc_points = []
        angle_step = 1  # Increment angle by 1 degree

        if span_angle < 0:
            for angle in range(start_angle, -(start_angle + span_angle + 1), -angle_step):
                x = int(origin_x + radius * math.cos(angle * math.pi / 180))
                y = int(origin_y + radius * math.sin(angle * math.pi / 180))
                arc_points.append(QPoint(x, y))  # Create QPoint object and append
        else:
            for angle in range(start_angle, start_angle + span_angle + 1, angle_step):
                x = int(origin_x + radius * math.cos(angle * math.pi / 180))
                y = int(origin_y + radius * math.sin(angle * math.pi / 180))
                arc_points.append(QPoint(x, y))  # Create QPoint object and append

        return arc_points
