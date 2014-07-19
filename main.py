import sys
from PyQt4 import QtGui, uic, QtCore
#from ui.treeview import *

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('vant3.ui', self)
        self.show()
        self.setup_data_tree()



    def setup_data_tree(self):

        self.model = QtGui.QStandardItemModel()
        for k in range(0, 4):
            parentItem = self.model.invisibleRootItem()
            for i in range(0, 4):
                item = QtGui.QStandardItem(QtCore.QString("item %0 %1").arg(k).arg(i))
                parentItem.appendRow(item)
                parentItem = item
        self.dataTreeView.setModel(self.model)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Ui_MainWindow()
    sys.exit(app.exec_())
