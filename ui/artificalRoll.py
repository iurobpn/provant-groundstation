__author__ = 'will'
#from https://github.com/pvbrowser/pvb/blob/master/qwt/examples/dials/attitude_indicator.cpp
# then found here, after porting the code
# http://xy-27.pythonxy.googlecode.com/hg-history/01b1d2a2550e0e46d86097aad85d8641cbe4d6ed/src/python/PyQwt/DOC/qt4examples/DialDemo.py

import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5 import QwtDial,QwtDialNeedle,qwtPolar2Pos
from PyQt4.QtGui import QPalette
from PyQt4.Qt import QPoint, QPolygon, QPen, QColor, Qt, QRegion,QSizePolicy
from PyQt4.QtCore import qRound
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

class AttitudeIndicatorNeedle(QwtDialNeedle):
    direction = 0

    def __init__(self, c, *args, **kwargs):
        QwtDialNeedle.__init__(self, *args, **kwargs)
        palette = QPalette()
        for i in range(QPalette.NColorGroups):  # ( int i = 0; i < QPalette.NColorGroups; i++ )
            palette.setColor(i, palette.Text, c)

        palette.setColor(QPalette.Base, QColor(0,0,0))
        self.setPalette(palette)

    def draw(self, painter, center, length, direction, cg):
        color = self.palette().color(cg, QPalette.Text)
        painter.setBrush(color)
        painter.setPen(QPen(color, 3))


class RollIndicator(Qwt.QwtDial):

    def __init__(self, *args):
        self.gradient = 0
        Qwt.QwtDial.__init__(self, *args)
        self.__gradient = 0.0
        self.setMode(Qwt.QwtDial.RotateScale)
        self.setWrapping(True)
        self.setOrigin(270.0)
        self.setScaleOptions(Qwt.QwtDial.ScaleTicks)
        self.setScale(0, 0, 30.0)
        self.setPalette(
            self.__colorTheme(QColor(Qt.darkGray).dark(150)))
        self.setNeedle(AttitudeIndicatorNeedle(
            self.palette().color(QPalette.Text)))

    # __init__()

    def setRoll(self,roll):
        self.setValue(roll)

    def setPitch(self,pitch):
        self.gradient = pitch/90.0
        self.update()

    def __colorTheme(self, base):
        background = base.dark(150)
        foreground = base.dark(200)

        mid = base.dark(110)
        dark = base.dark(170)
        light = base.light(170)
        text = foreground.light(800)

        palette = QPalette()
        for colorGroup in colorGroupList:
            palette.setColor(colorGroup, QPalette.Base, base)
            palette.setColor(colorGroup, QPalette.Background, background)
            palette.setColor(colorGroup, QPalette.Mid, mid)
            palette.setColor(colorGroup, QPalette.Light, light)
            palette.setColor(colorGroup, QPalette.Dark, dark)
            palette.setColor(colorGroup, QPalette.Text, text)
            palette.setColor(colorGroup, QPalette.Foreground, foreground)

        return palette

    def angle(self):
        return self.value()

    # angle()

    def setAngle(self, angle):
        self.setValue(angle)

    # setAngle()

    def gradient(self):
        return self.__gradient

    # gradient()

    def setGradient(self, gradient):
        self.__gradient = gradient

    # setGradient()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.setGradient(self.gradient + 0.05)
        elif event.key() == Qt.Key_Minus:
            self.setGradient(self.gradient - 0.05)
        else:
            Qwt.QwtDial.keyPressEvent(self, event)

    # keyPressEvent()

    def drawScale(self, painter, center, radius, origin, minArc, maxArc):
        direction1 = M_PI_2
        triangleSize = qRound(radius * 0.15)
        p0 = (QPoint(center.x() + 0, center.y() + 0))
        p1 = qwtPolar2Pos(p0, radius - 2 * triangleSize +20 , direction1)
        pa = QPolygon(3)
        pa.setPoint(0, qwtPolar2Pos(p1, -1.6 * triangleSize,direction1))
        pa.setPoint(1, qwtPolar2Pos(p1, triangleSize, direction1 + M_PI_2))
        pa.setPoint(2, qwtPolar2Pos(p1, triangleSize, direction1 - M_PI_2))
        color = self.palette().color(QPalette.Text)
        painter.setBrush(color)
        painter.drawPolygon(pa)

    def drawScaleContents(self, painter, center, radius):
        dir = 90#360 - int(roud(self.origin() - self.value()))
        arc = 90 #+ int(round(self.gradient * 90))
        skyColor = QColor(38, 151, 221)
        painter.save()
        painter.setBrush(skyColor)
        painter.drawChord(
            self.scaleContentsRect(), (dir - arc)*16, 2*arc*16)
        direction1 = self.value() * M_PI / 180.0 
        direction2 = self.value() * M_PI / 180.0 +M_PI_2

        triangleSize = qRound(radius * 0.15)
        p0 = (QPoint(center.x() + 0, center.y() + 0))
        p1 = qwtPolar2Pos(p0, 2, direction2)
        pa = QPolygon(3)
        pa.setPoint(0, qwtPolar2Pos(p1, 2 * triangleSize, direction2))
        pa.setPoint(1, qwtPolar2Pos(p1, triangleSize, direction2 + M_PI_2))
        pa.setPoint(2, qwtPolar2Pos(p1, triangleSize, direction2 - M_PI_2))
        color = self.palette().color(QPalette.Text)
        painter.setBrush(color)
        painter.drawPolygon(pa)

        p0 = (QPoint(center.x() + 0, center.y() + 0))
        color = self.palette().color(QPalette.Text)
        painter.setBrush(color)
        painter.setPen(QPen(color, 3))
        painter.drawLine(qwtPolar2Pos(p0, radius - 3, direction1), qwtPolar2Pos(p0, radius - 3, direction1 - M_PI))

        painter.restore()
