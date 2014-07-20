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
    """
    Class responsible for keeping data points, and creating a curve from them.
    """
    def __init__(self,name):
        self.data = list(zeros(XRANGE, Float))
        self.curve = Qwt.QwtPlotCurve("Data"+name)

    def addPoint(self, y):
        self.data.append(y)

    def update(self):
        self.curve.setData(self.x, self.data[-XRANGE:])

    def setColor(self, value):
        self.curve.setPen(value)


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('vant3.ui', self)
        self.setupTreeWidget()
        self.show()
        self.setupPlot()
        self.dataSets = {}

    def addPoint(self, datasetName, y):
        if datasetName not in self.dataSets:
            self.dataSets[datasetName] = DataSet(datasetName)
            self.dataSets[datasetName].curve.attach(self.qwtPlot)
        self.dataSets[datasetName].addPoint(y)

    def setupPlot(self):
        self.startTimer(50)

    def timerEvent(self, e):
        self.addPoint('gyr', random.randint(10))

        self.qwtPlot.replot()
        for namea, dataset in self.dataSets.items():
            dataset.update()

    def setupTreeWidget(self):
        self.treeWidget.header().setResizeMode(3)

    def addDataTree(self, data, children_number):
        parent = CustomTreeItem(self, self.treeWidget, data, self.treeWidget, color=False)
        for i in range(children_number):
            CustomTreeItem(self, parent, data+str(children_number))

    def addSingleData(self, name):
        CustomTreeItem(self, self.treeWidget, name, self.treeWidget)

    def disable_plot(self, name):
        self.dataSets[name].curve.detach()

    def enable_plot(self, name):
        self.dataSets[name].curve.attach(self.qwtPlot)

    def set_plot_color(self, name, color):
        self.dataSets[name].setColor(color)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.addSingleData('gyr')
    window.addDataTree('acc')
    sys.exit(app.exec_())
