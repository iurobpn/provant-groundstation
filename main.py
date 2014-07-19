import sys
from PyQt4 import QtGui, uic, QtCore
from ui.items import CustomTreeItem
class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('vant3.ui', self)
        self.show()
        self.add_single('uva')
        self.add_simple_tree('penis')
        self.treeWidget.header().setResizeMode(3)
# for(int i = 0; i < 3; i++)
#         tree->resizeColumnToContents(i);
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
