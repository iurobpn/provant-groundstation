from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainterPath


class JoystickStick(QtGui.QGraphicsView):
    def __init__(self, parent = None ):
        super(JoystickStick, self).__init__(parent)

        scene = QtGui.QGraphicsScene()
        self.setScene(scene)
        self.x = 0
        self.y = 0
        self.w = 20
        self.h = 20

        self.setStyleSheet("background: transparent");
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.black))
        brush = QtGui.QBrush(pen.color().darker(150))
        self.item = scene.addEllipse(self.x, self.y, self.w, self.h, pen, brush)
        self.item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

    def mouseMoveEvent(self, event):
        # check of mouse moved within the restricted area for the item
        x = event.pos().x()
        y = event.pos().y()
        size = self.size()
        if 0 < x < size.width() and 0 < y < size.height():
            super(JoystickStick, self).mouseMoveEvent(event)

    def resizeEvent(self,event):
        super(JoystickStick,self).resizeEvent(event)
        x, y = self.size().width()-4, self.size().height()-4
        self.setSceneRect(0, 0, x, y)
        self.x = x/2 - self.w/2
        self.y = y/2 - self.h/2
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.black))
        self.vline = self.scene().addLine(x/2, 0, x/2, y, pen)
        self.hline = self.scene().addLine(0, y/2, x, y/2, pen)

        self.generateArrows()
        self.show()

    def generateArrows(self):
        x, y = self.size().width()-4, self.size().height()-4
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.black))
        brush = QtGui.QBrush(pen.color().darker(150))
        points_list = [[QtCore.QPoint(x/2, 0), QtCore.QPoint(x/2 + 5, 5), QtCore.QPoint(x/2 - 5, 5)],
                       [QtCore.QPoint(x/2, y), QtCore.QPoint(x/2 + 5, y-5), QtCore.QPoint(x/2 - 5, y-5)],
                       [QtCore.QPoint(0, y/2), QtCore.QPoint(5,   y/2+5), QtCore.QPoint(5, y/2-5)],
                       [QtCore.QPoint(x, y/2), QtCore.QPoint(x-5, y/2+5), QtCore.QPoint(x-5, y/2-5)]]
        for points in points_list:
            poly = QtGui.QPolygonF(points)
            path = QPainterPath()
            path.addPolygon(poly)
            self.rArrow = self.scene().addPolygon(poly, pen)
            self.scene().addPath(path, pen, brush)

    def move(self, x1, y1):
        x, y = self.size().width()-4, self.size().height()-4
        self.x = x/2 - self.w/2 + x/2 * x1/100.0
        self.y = y/2 - self.h/2 + y/2 * y1/100.0
        self.item.setPos(self.x, self.y)
