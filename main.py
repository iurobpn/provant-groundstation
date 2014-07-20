import sys
from PyQt4 import QtGui, uic
import PyQt4.Qwt5 as Qwt
from ui.items import CustomTreeItem
import random
from PyQt4.Qwt5.anynumpy import *
XRANGE = 500

#just tricking my auto-complete
arange = arange

class DataSet():
    """
    Class responsible for keeping data points, and creating a curve from them.
    """
    def __init__(self, name):
        self.data = list(zeros(XRANGE, Float)) ##starts Y with zeros
        self.x = arange(0.0, 1000, 0.5)
        self.curve = Qwt.QwtPlotCurve("Data"+name)

    def addPoint(self, y):
        self.data.append(y)

    def update(self):
        self.curve.setData(self.x, self.data[-XRANGE:])

    def setColor(self, value):
        ## pen style: http://pyqt.sourceforge.net/Docs/PyQt4/qpen.html
        self.curve.setPen(QtGui.QPen(value,2))


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
            self.addSingleData(datasetName)
            self.dataSets[datasetName].setColor(self.getColor(datasetName))
        self.dataSets[datasetName].addPoint(y)

    def addArray(self, datasetName, points):
        datasetName_ = datasetName + str(0)
        if datasetName_ not in self.dataSets:
            self.addDataTree(datasetName, len(points))
            for i in range(len(points)):
                datasetName_ = datasetName+str(i)
                self.dataSets[datasetName_] = DataSet(datasetName)
                self.dataSets[datasetName_].curve.attach(self.qwtPlot)
                self.dataSets[datasetName_].setColor(self.getColor(datasetName_))
        for i in range(len(points)):
                self.dataSets[datasetName+str(i)].addPoint(points[i])

    def setupPlot(self):
        self.startTimer(50)

    def timerEvent(self, e):
        asd = 3.3
        self.addPoint('gyr', asd + random.randint(40)/100.0)
        self.addArray('acc',[1,2,3])
        self.qwtPlot.replot()
        for namea, dataset in self.dataSets.items():
            dataset.update()

    def setupTreeWidget(self):
        self.treeWidget.header().setResizeMode(3)

    def addDataTree(self, data, children_number):
        parent = CustomTreeItem(self, self.treeWidget, data, self.treeWidget, color=False)
        for i in range(children_number):
            CustomTreeItem(self, parent, data+str(i))

    def addSingleData(self, name):
        CustomTreeItem(self, self.treeWidget, name, self.treeWidget)

    def disablePlot(self, name):
        self.dataSets[name].curve.detach()

    def enablePlot(self, name):
        self.dataSets[name].curve.attach(self.qwtPlot)

    def setPlotColor(self, name, color):
        #print color
        self.dataSets[name].setColor(color)

    def getColor(self, name):
        return self.findNode(name).colorChooser.color()

    def findNode(self, name, node=None):
        if not node:
            root = self.treeWidget.invisibleRootItem()
            node = root
        else:
            #print node.text(0)
            if node.text(0) == name:
                return node
        for i in range(node.childCount()):
            if self.findNode(name, node.child(i)):
                return self.findNode(name, node.child(i))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    #window.addDataTree('acc',3)
    sys.exit(app.exec_())
