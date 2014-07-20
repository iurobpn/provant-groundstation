import sys
from PyQt4 import QtGui, uic, QtCore
import PyQt4.Qwt5 as Qwt
from ui.items import CustomTreeItem
from random_snippets.qwtplot1 import DataPlot
from PyQt4 import Qt
from math import *
import random
from PyQt4.Qwt5.anynumpy import *
XRANGE = 1000

arange = arange ##just tricking my auto-complete

class DataSet():
    def __init__(self,name):
        self.data = list(zeros(XRANGE, Float))
        self.curve = Qwt.QwtPlotCurve("Data"+name)
        self.x = arange(0.0, XRANGE, 0.5)

    def addPoint(self,y):
        self.data.append(y)

    def update(self):
        self.curve.setData(self.x, self.data[-XRANGE:])

    def set_color(self,value):
        self.curve.setPen(value)

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('vant3.ui', self)
        self.setupTreeWidget()
        self.show()
        self.setupPlot()
        self.datasets = {}


    def add_point(self,datasetName,y):
        if datasetName not in self.datasets:
            self.datasets[datasetName] = DataSet(datasetName)
            self.datasets[datasetName].curve.attach(self.qwtPlot)
        self.datasets[datasetName].addPoint(y)


    def setupPlot(self):
        self.phase = 0
        self.startTimer(50)


    def timerEvent(self, e):
        self.add_point('gyr',random.randint(10))

        self.qwtPlot.replot()
        for name, dataset in self.datasets.items():
            dataset.update()

    def setupTreeWidget(self):
        self.treeWidget.header().setResizeMode(3)

    def add_simple_tree(self,data,children_number):
        parent = CustomTreeItem(self,self.treeWidget,data,self.treeWidget,color = False)
        for i in range(children_number):
            CustomTreeItem(self,parent,data+str(children_number))

    def add_single(self,name):
        CustomTreeItem(self,self.treeWidget,name,self.treeWidget)

    def disable_plot(self,name):
        self.datasets[name].curve.detach()

    def enable_plot(self,name):
        self.datasets[name].curve.attach(self.qwtPlot)

    def set_plot_color(self,name,color):
        self.datasets[name].set_color(color)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.add_single('gyr')
    window.add_simple_tree('acc')
    sys.exit(app.exec_())
