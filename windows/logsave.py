__author__ = 'Patrick'

import sys
import os
import time
import webbrowser
from PyQt4 import *
import PyQt4.Qwt5 as Qwt
from PyQt4.QtCore import QTimer

class LogSaveSetup(QtGui.QTabWidget):
    def __init__(self,window=None):
        super(LogSaveSetup, self).__init__()
        uic.loadUi('windows/log.ui', self)
        self.setWindowIcon(QtGui.QIcon('windows/icon/favicon.ico'))
        self.window = window
        self.timer=QTimer()

        self.connect(self.timer,QtCore.SIGNAL('timeout()'),self.timerEvent)
        self.connect(self.startButton, Qt.SIGNAL("clicked()"), self.startEvent)
        self.startButton.setShortcut('Ctrl+O')
        self.connect(self.stopButton, Qt.SIGNAL("clicked()"), self.stopEvent)
        self.stopButton.setShortcut('Ctrl+P')
        self.connect(self.saveAsButton, Qt.SIGNAL("clicked()"), self.saveAsEvent)
        self.radioButton.toggled.connect(self.radioEvent)

        
        self.start=False
        self.stop=False
        self.radioEnabled=False



    def showWindow(self):
        self.show()

    def saveAsEvent(self):
        self.window.saveFileAs()

    def startEvent(self):
        self.start=True
        if(self.window):
            self.window.dataSets={}
            self.window.qwtPlot.clear()
            self.window.treeWidget.clear()

    def stopEvent(self):
        if(self.start==True):
            self.checkStart()
            self.stop=True
            self.window.saveFile()
            self.window.qwtPlot.clear()
            self.window.treeWidget.clear()
            self.window.dataSets={}

    def showDisplay(self,value=0):
        if(self.start==True):
            self.lcdNumber.display(value)

    def radioEvent(self,enabled):
        if enabled:
            self.radioEnabled=True
            self.lcdNumber.display(0)
            self.startEvent()
        else:
            self.radioEnabled=False
        
        if(self.timer.isActive()==False):
            self.timer.start()

    def checkStart(self):
        temp = self.start
        self.start = False
        return temp

    def checkStop(self):
        temp = self.stop
        self.stop = False
        return temp


    def autoSave(self):
        if(self.radioEnabled==True):
            if(self.spinBox.value()==0):
                self.radioEnabled=False
            else:
                self.startEvent()
                self.radioEnabled=True
                while(self.lcdNumber.value()<self.spinBox.value()):
                    pass
                self.stopEvent()

    def timerEvent(self):
        time.sleep(0.01)
        if(self.radioEnabled==True):
            if(self.spinBox.value()==0):
                self.radioEnabled=False
            else:
                self.radioEnabled=True
                if(self.lcdNumber.value()>self.spinBox.value()):
                    self.stopEvent()
                else:
                    self.progressBar.setValue(self.lcdNumber.value()*100/self.spinBox.value())
