__author__ = 'Patrick'

import sys
import os
import webbrowser
from PyQt4 import QtGui, uic, Qt
import PyQt4.Qwt5 as Qwt

class AboutSetup(QtGui.QDialog):
    def __init__(self):
        super(AboutSetup, self).__init__()
        uic.loadUi('windows/about.ui', self)
        self.show()
        myPixmap = QtGui.QPixmap("provant_transp_canvas.png")
        myScaledPixmap = myPixmap.scaled(self.label.size(), 0)
        self.label.setPixmap(myScaledPixmap)
        self.connect(self.pushButton, Qt.SIGNAL("clicked()"), self.pushEvent)

    def pushEvent(self):
        webbrowser.open('http://provantbr.github.io')
        webbrowser.open('https://github.com/Williangalvani')
        webbrowser.open('https://github.com/patrickelectric')
        self.close()