import sys
from PyQt4 import QtGui, uic, QtCore
import PyQt4.Qwt5 as Qwt
from ui.items import CustomTreeItem
from random_snippets.qwtplot1 import DataPlot
from PyQt4 import Qt
from math import *
import random
from PyQt4.Qwt5.anynumpy import *

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('vant3.ui', self)
        self.setupTreeWidget()
        self.show()
        self.setupPlot()
        self.phase = 0
        self.x = arange(0.0, 100.1, 0.5)
        self.y = zeros(len(self.x), Float)
        self.z = zeros(len(self.x), Float)
        self.curveR = Qwt.QwtPlotCurve("Data Moving Right")
        self.curveR.attach(self.qwtPlot)
        self.curveL = Qwt.QwtPlotCurve("Data Moving Left")
        self.curveL.attach(self.qwtPlot)

    def setupPlot(self):
        self.qwtPlot.setCanvasBackground(Qt.Qt.white)
        #self.qwtPlot.alignScales()
        #self.qwtPlot.setTitle("A Moving QwtPlot Demonstration")
        #self.qwtPlot.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend)
        self.startTimer(50)


    def timerEvent(self, e):
        from PyQt4.Qwt5.anynumpy import *
        if self.phase > pi - 0.0001:
            self.phase = 0.0

        # y moves from left to right:
        # shift y array right and assign new value y[0]
        self.y = concatenate((self.y[:1], self.y[:-1]), 1)
        self.y[0] = sin(self.phase) * (-1.0 + 2.0*random.random())

        # z moves from right to left:
        # Shift z array left and assign new value to z[n-1].
        self.z = concatenate((self.z[1:], self.z[:1]), 1)
        self.z[-1] = 0.8 - (2.0 * self.phase/pi) + 0.4*random.random()

        self.curveR.setData(self.x, self.y)
        self.curveL.setData(self.x, self.z)

        self.qwtPlot.replot()
        self.phase += pi*0.02

    def setupTreeWidget(self):
        self.treeWidget.header().setResizeMode(3)
        self.add_single('uva')
        self.add_simple_tree('penis')
        print self.treeWidget

    def add_simple_tree(self,data):
        parent = CustomTreeItem(self.treeWidget,data,self.treeWidget,color = False)
        CustomTreeItem(parent,data+'1')
        CustomTreeItem(parent,data+'2')
        CustomTreeItem(parent,data+'3')

    def add_single(self,name):
        CustomTreeItem(self.treeWidget,name,self.treeWidget)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Ui_MainWindow()
    sys.exit(app.exec_())
