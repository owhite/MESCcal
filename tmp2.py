#!/usr/bin/env python3

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPolygonItem, QGraphicsView, QGraphicsDropShadowEffect
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF, QColor

class MyScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        # Create a polygon
        polygon = QPolygonF([QPointF(0, -50), QPointF(50, 50), QPointF(-50, 50)])

        # Create a QGraphicsPolygonItem
        item = QGraphicsPolygonItem(polygon)

        # Set color and opacity of the shadow
        shadow_color = QColor(0, 0, 0)
        shadow_color.setAlpha(254)  # Set alpha for transparency
        item.setGraphicsEffect(self.createDropShadow(shadow_color))

        # Set a pen for visualization
        item.setPen(QColor(0, 0, 144))

        # Add the item to the scene
        self.addItem(item)

        # Set the background color of the scene to make the shadow visible
        self.setBackgroundBrush(QColor(255, 255, 255))  # White background

    def createDropShadow(self, color):
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(color)
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 0)
        return shadow

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])

    scene = MyScene()
    view = QGraphicsView(scene)
    view.show()

    app.exec_()
