#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QLCDNumber
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPolygonF, QColor

class PolygonColoringApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create QTabWidget
        tab_widget = QTabWidget()

        # Create tabs
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        # Add tabs to the tab widget
        tab_widget.addTab(tab1, "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")
        tab_widget.addTab(tab3, "Tab 3")

        # Create polygons and QLCDNumbers for the first tab
        scene1 = QGraphicsScene(self)
        self.create_polygons_and_lcd(scene1)

        # Create a QGraphicsView for the first tab
        view1 = QGraphicsView(scene1)

        # Add the QGraphicsView to the layout of the first tab
        layout1 = QVBoxLayout(tab1)
        layout1.addWidget(view1)

        # Set the central widget of the main window to the tab widget
        self.setCentralWidget(tab_widget)

        self.setWindowTitle('Main Window with Tabs')
        self.setGeometry(100, 100, 600, 400)

    def create_polygons_and_lcd(self, scene):
        # Create polygons
        polygon1 = QPolygonF([QPointF(-50, -50), QPointF(0, -100), QPointF(50, -50)])
        polygon2 = QPolygonF([QPointF(-50, 50), QPointF(0, 100), QPointF(50, 50)])

        # Create QGraphicsPolygonItems with different colors
        item1 = QGraphicsPolygonItem(polygon1)
        item1.setBrush(QColor(Qt.red))

        item2 = QGraphicsPolygonItem(polygon2)
        item2.setBrush(QColor(Qt.blue))

        # Add items to the scene
        scene.addItem(item1)
        scene.addItem(item2)

        # Create QLCDNumber widgets
        lcd_number1 = QLCDNumber()
        lcd_number2 = QLCDNumber()

        # Set the geometry of the QLCDNumber widgets
        lcd_number1.setGeometry(50, 220, 100, 50)
        lcd_number2.setGeometry(250, 220, 100, 50)

        # Set digit count and segment style to make the color visible
        lcd_number1.setDigitCount(8)
        lcd_number2.setDigitCount(8)
        lcd_number1.setSegmentStyle(QLCDNumber.Flat)
        lcd_number2.setSegmentStyle(QLCDNumber.Flat)

        # Set color for the LCDNumbers
        lcd_number1.setStyleSheet("color: red")
        lcd_number2.setStyleSheet("color: blue")

        # Calculate and display the area of each polygon in the QLCDNumber widgets
        lcd_number1.display(self.calculate_polygon_area(item1.polygon()))
        lcd_number2.display(self.calculate_polygon_area(item2.polygon()))

    def calculate_polygon_area(self, polygon):
        # Calculate the area of the polygon's bounding rectangle
        bounding_rect = polygon.boundingRect()
        return bounding_rect.width() * bounding_rect.height()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PolygonColoringApp()
    window.show()
    sys.exit(app.exec_())
