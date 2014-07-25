__author__ = 'will'
from PyQt4 import QtGui, QtCore
from PyKDE4.kdeui import KVBox, KHBox, KColorButton
from random import randint

class CustomTreeItem(QtGui.QTreeWidgetItem):

    def __init__(self, window, parent, name, view=None, color=True):
        if view:
            self.view = view
        if not view:
            view = parent.view
        self.window = window
        self._name = name
        ## Init super class ( QtGui.QTreeWidgetItem )
        super(CustomTreeItem, self).__init__(parent)

        ## Column 0 - Text:
        self.setText(0, name)

        ## Column 1 - Color:
        if color:
            self.colorChooser = KColorButton(view)
            self.colorChooser.setColor(QtGui.QColor(randint(0, 255), randint(0, 255), randint(0, 255)))
            self.colorChooser.setGeometry(QtCore.QRect(0, 0, 10, 10))
            view.setItemWidget(self, 1, self.colorChooser)
            view.connect(self.colorChooser, QtCore.SIGNAL("changed (const QColor&)"), self.colorChanged)

        ## Column 2 - CheckBox:
        self.button = QtGui.QCheckBox(view)
        self.button.setChecked(True)
        view.setItemWidget(self, 2, self.button)

        ## Column 3 - Current value:
        if color:
            self.setText(3, 'N/A')
        else:
            self.setText(3, '')

        ## Signals
        view.connect(self.button, QtCore.SIGNAL("clicked()"), self.buttonPressed)


    def setDataValue(self, value):
        self.setText(3, str(value))

    def buttonPressed(self):
        if self.childCount():
            for i in range(self.childCount()):
                self.child(i).button.setChecked(self.button.isChecked())
                self.child(i).buttonPressed()

        elif self.button.isChecked():
            self.window.enablePlot(self._name)
            self.window.setPlotColor(self._name, self.colorChooser.color())
        else:
            self.window.disablePlot(self._name)

    def colorChanged(self):
        self.window.setPlotColor(self._name, self.colorChooser.color())