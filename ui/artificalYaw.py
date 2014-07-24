__author__ = 'will'
#from https://github.com/pvbrowser/pvb/blob/master/qwt/examples/dials/attitude_indicator.cpp
# then found here, after porting the code
# http://xy-27.pythonxy.googlecode.com/hg-history/01b1d2a2550e0e46d86097aad85d8641cbe4d6ed/src/python/PyQwt/DOC/qt4examples/DialDemo.py

import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5 import *
from PyQt4.QtGui import *
from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
import math
from math import pi as M_PI

M_PI_2 = M_PI/2.0


def enumList(enum, sentinel):
    '''
    '''
    return [enum(i) for i in range(sentinel)]

colorGroupList = enumList(
    QPalette.ColorGroup, QPalette.NColorGroups)
colorRoleList = enumList(
    QPalette.ColorRole, QPalette.NColorRoles)
handList  = enumList(
    Qwt.QwtAnalogClock.Hand, Qwt.QwtAnalogClock.NHands)

class YawIndicator(QWidget):

    angleChanged = pyqtSignal(float)
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setFixedSize(135,135)
        self._angle = 0.0
        self._margins = 10
        self._pointText = {0: "N", 45: "NE", 90: "E", 135: "SE", 180: "S",
        225: "SW", 270: "W", 315: "NW"}

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))
        self.drawMarkings(painter)
        self.drawNeedle(painter)
        
        painter.end()
    
    def drawMarkings(self, painter):
    
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        scale = min((self.width() - self._margins)/120.0,
                    (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)
        
        font = QFont(self.font())
        font.setPixelSize(10)
        metrics = QFontMetricsF(font)
        
        painter.setFont(font)
        painter.setPen(self.palette().color(QPalette.Text))
        
        i = 0
        while i < 360:
        
            if i % 45 == 0:
                painter.drawLine(0, -40, 0, -50)
                painter.drawText(-metrics.width(self._pointText[i])/2.0, -52,
                                 self._pointText[i])
            else:
                painter.drawLine(0, -45, 0, -50)
            
            painter.rotate(15)
            i += 15
        
        painter.restore()
    
    def drawNeedle(self, painter):
    
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self._angle)
        scale = min((self.width() - self._margins)/120.0,
                    (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)
        
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(self.palette().brush(QPalette.Shadow))
        
        painter.drawPolygon(
            QPolygon([QPoint(-10, 0), QPoint(0, -45), QPoint(10, 0),
                      QPoint(0, 45), QPoint(-10, 0)])
            )
        
        painter.setBrush(QtGui.QColor(220, 0, 0))
        
        painter.drawPolygon(
            QPolygon([QPoint(-5, -25), QPoint(0, -45), QPoint(5, -25),
                      QPoint(0, -30), QPoint(-5, -25)])
            )
        
        painter.restore()
    '''
    def sizeHint(self):
        return QSize(40, 40)
    '''
    
    def angle(self):
        return self._angle
    
    @pyqtSlot(float)
    def setAngle(self, angle):
    
        #if angle != self._angle:
        self._angle = angle
        self.angleChanged.emit(angle)
        self.update()
    
    #angle = pyqtProperty(float, angle, setAngle)