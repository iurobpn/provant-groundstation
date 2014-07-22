__author__ = 'will'
#from https://github.com/pvbrowser/pvb/blob/master/qwt/examples/dials/attitude_indicator.cpp
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5 import QwtDial,QwtDialNeedle,qwtPolar2Pos
from PyQt4.QtGui import QPalette
from PyQt4.Qt import QPoint, QPolygon, QPen, QColor, Qt, QRegion,QSizePolicy
from PyQt4.QtCore import qRound

from math import pi as M_PI



M_PI_2 = M_PI
class AttitudeIndicatorNeedle(QwtDialNeedle):
    direction = 10

    def __init__(self, c, *args, **kwargs):
        QwtDialNeedle.__init__(self, *args, **kwargs)
        palette = QPalette()
        for i in range(QPalette.NColorGroups):  # ( int i = 0; i < QPalette.NColorGroups; i++ )
            palette.setColor(i, palette.Text, c)
        self.setPalette(palette)

    def draw(self,painter, center, length, direction, cg):
        self.direction *= M_PI / 180.0;
        triangleSize = qRound(length * 0.1);

        painter.save();

        p0 = (QPoint(center.x() + 1, center.y() + 1));

        p1 = qwtPolar2Pos(p0,length - 2 * triangleSize - 2, direction);

        pa = QPolygon(3);
        pa.setPoint(0, qwtPolar2Pos(p1, 2 * triangleSize, direction));
        pa.setPoint(1, qwtPolar2Pos(p1, triangleSize, direction + M_PI_2));
        pa.setPoint(2, qwtPolar2Pos(p1, triangleSize, direction - M_PI_2));

        color = self.palette().color(cg, QPalette.Text);
    #endif
        painter.setBrush(color);
        painter.drawPolygon(pa);

        painter.setPen(QPen(color, 3));
        painter.drawLine(qwtPolar2Pos(p0, length - 2, direction + M_PI_2),
            qwtPolar2Pos(p0, length - 2, direction - M_PI_2));

        painter.restore();


class AttitudeIndicator(QwtDial):#AttitudeIndicator::AttitudeIndicator(

    def __init__(self, parent, *args, **kwargs):

        QwtDial.__init__(self, parent, *args, **kwargs)

        self.setMinimumSize(200, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.direction = 'Standstill'
        self.setWrapping(False)


        self.gradient = 0.0

        self.setMode(self.RotateScale);
        self.setWrapping(True);

        self.setOrigin(270.0);
        self.setScaleOptions(self.ScaleTicks);
        self.setScale(0, 0, 30.0);

        color = self.palette().color(QPalette.Text);
        self.setNeedle(AttitudeIndicatorNeedle(color));

    def setGradient(self, gradient):
        if gradient < -1.0:
            self.gradient = -1.0;
        elif gradient > 1.0:
            self.gradient = 1.0;
        if self.gradient != gradient:
            self.gradient = gradient;
            self.update();

    def drawScale(self,painter, center, radius, origin, minArc, maxArc):

        dir = (360.0 - origin) * M_PI / 180.0; #counter clockwise, radian

        offset = 4;

        p0 = qwtPolar2Pos(center, offset, dir + M_PI);

        w = self.contentsRect().width();

        pa = [0,0,0,0]
        pa[0] = qwtPolar2Pos(p0, w, dir - M_PI_2);
        pa[1] = qwtPolar2Pos(pa[0], 2 * w, dir + M_PI/2);
        pa[2] = qwtPolar2Pos(pa[1], w, dir);
        pa[3] = qwtPolar2Pos(pa[2], 2 * w, dir - M_PI/2);
        painter.save();
        painter.setClipRegion(QRegion(pa)); # swallow 180 - 360 degrees

        QwtDial.drawScale(self,painter, center, radius, origin, minArc, maxArc);

        painter.restore();


    def drawScaleContents(self, painter, Non2, None2):

        dir = 360 - qRound(self.origin() - self.value()); #// counter clockwise
        arc = 90 + qRound(self.gradient * 90);

        skyColor = QColor(38, 151, 221);

        painter.save();
        painter.setBrush(skyColor);
        painter.drawChord(self.scaleContentsRect(),
            (dir - arc) * 16, 2 * arc * 16 );
        painter.restore();


    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Plus:
            self.setGradient(self.gradient + 0.05);
        elif e.key() == Qt.Key_Minus:
            self.setGradient(self.gradient - 0.05);
        else:
            QwtDial.keyPressEvent(e);
