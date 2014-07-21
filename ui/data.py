__author__ = 'will'

from PyQt4 import QtGui, uic
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *
XRANGE = 500

class DataSet():
    """
    Class responsible for keeping data points, and creating a curve from them.
    """
    def __init__(self,window, name):
        self.window = window
        self.data = list(zeros(XRANGE, Float)) ##starts Y with zeros
        self.x = arange(0.0, 1000, 0.5)
        self.curve = Qwt.QwtPlotCurve("Data"+name)
        self.treeItem = None
        self.name = name

    def addPoint(self, y):
        self.data.append(y)
        if not self.treeItem:
            self.treeItem = self.window.findNode(self.name)
            #print self.treeItem._name
        else:
            self.treeItem.setDataValue(y)

    def update(self):
        self.curve.setData(self.x, self.data[-XRANGE:])

    def setColor(self, value):
        ## pen style: http://pyqt.sourceforge.net/Docs/PyQt4/qpen.html
        self.curve.setPen(QtGui.QPen(value, 2))

