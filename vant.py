# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vant.ui'
#
# Created: Fri Jul 18 02:19:28 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.qwtPlot = QwtPlot(self.centralwidget)
        self.qwtPlot.setGeometry(QtCore.QRect(0, 0, 400, 200))
        self.qwtPlot.setMouseTracking(True)
        self.qwtPlot.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qwtPlot.setFrameShadow(QtGui.QFrame.Plain)
        self.qwtPlot.setLineWidth(1)
        self.qwtPlot.setMidLineWidth(1)
        self.qwtPlot.setProperty("propertiesDocument", _fromUtf8(""))
        self.qwtPlot.setObjectName(_fromUtf8("qwtPlot"))
        
        self.ImageDialog = KDialog(self.centralwidget)
        self.ImageDialog.setGeometry(QtCore.QRect(490, 460, 193, 44))
        self.ImageDialog.setObjectName(_fromUtf8("ImageDialog"))
        self.kcolorcombo = KColorCombo(self.centralwidget)
        self.kcolorcombo.setGeometry(QtCore.QRect(410, 0, 88, 25))
        self.kcolorcombo.setObjectName(_fromUtf8("kcolorcombo"))
        self.kcolorcombo_2 = KColorCombo(self.centralwidget)
        self.kcolorcombo_2.setGeometry(QtCore.QRect(410, 30, 88, 25))
        self.kcolorcombo_2.setObjectName(_fromUtf8("kcolorcombo_2"))
        self.kcolorcombo_3 = KColorCombo(self.centralwidget)
        self.kcolorcombo_3.setGeometry(QtCore.QRect(590, 0, 88, 25))
        self.kcolorcombo_3.setObjectName(_fromUtf8("kcolorcombo_3"))
        self.kcolorcombo_4 = KColorCombo(self.centralwidget)
        self.kcolorcombo_4.setGeometry(QtCore.QRect(500, 30, 88, 25))
        self.kcolorcombo_4.setObjectName(_fromUtf8("kcolorcombo_4"))
        self.kcolorcombo_5 = KColorCombo(self.centralwidget)
        self.kcolorcombo_5.setGeometry(QtCore.QRect(500, 0, 88, 25))
        self.kcolorcombo_5.setObjectName(_fromUtf8("kcolorcombo_5"))
        self.kcolorcombo_6 = KColorCombo(self.centralwidget)
        self.kcolorcombo_6.setGeometry(QtCore.QRect(590, 30, 88, 25))
        self.kcolorcombo_6.setObjectName(_fromUtf8("kcolorcombo_6"))
        self.kcolorcombo_7 = KColorCombo(self.centralwidget)
        self.kcolorcombo_7.setGeometry(QtCore.QRect(500, 60, 88, 25))
        self.kcolorcombo_7.setObjectName(_fromUtf8("kcolorcombo_7"))
        self.kcolorcombo_8 = KColorCombo(self.centralwidget)
        self.kcolorcombo_8.setGeometry(QtCore.QRect(590, 60, 88, 25))
        self.kcolorcombo_8.setObjectName(_fromUtf8("kcolorcombo_8"))
        self.kcolorcombo_9 = KColorCombo(self.centralwidget)
        self.kcolorcombo_9.setGeometry(QtCore.QRect(410, 60, 88, 25))
        self.kcolorcombo_9.setObjectName(_fromUtf8("kcolorcombo_9"))
        self.ksqueezedtextlabel_4 = KSqueezedTextLabel(self.centralwidget)
        self.ksqueezedtextlabel_4.setGeometry(QtCore.QRect(450, 90, 124, 15))
        self.ksqueezedtextlabel_4.setObjectName(_fromUtf8("ksqueezedtextlabel_4"))
        self.ksqueezedtextlabel_5 = KSqueezedTextLabel(self.centralwidget)
        self.ksqueezedtextlabel_5.setGeometry(QtCore.QRect(530, 90, 124, 15))
        self.ksqueezedtextlabel_5.setObjectName(_fromUtf8("ksqueezedtextlabel_5"))
        self.ksqueezedtextlabel_6 = KSqueezedTextLabel(self.centralwidget)
        self.ksqueezedtextlabel_6.setGeometry(QtCore.QRect(620, 90, 124, 15))
        self.ksqueezedtextlabel_6.setObjectName(_fromUtf8("ksqueezedtextlabel_6"))
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(680, 0, 91, 21))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(680, 30, 91, 21))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(680, 60, 91, 21))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 210, 31, 201))
        self.progressBar.setMaximum(20)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.progressBar_2 = QtGui.QProgressBar(self.centralwidget)
        self.progressBar_2.setGeometry(QtCore.QRect(40, 210, 31, 201))
        self.progressBar_2.setMaximum(20)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_2.setObjectName(_fromUtf8("progressBar_2"))
        self.progressBar_3 = QtGui.QProgressBar(self.centralwidget)
        self.progressBar_3.setGeometry(QtCore.QRect(80, 210, 118, 23))
        self.progressBar_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar_3.setAutoFillBackground(False)
        self.progressBar_3.setMinimum(-60)
        self.progressBar_3.setMaximum(60)
        self.progressBar_3.setProperty("value", 0)
        self.progressBar_3.setInvertedAppearance(False)
        self.progressBar_3.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar_3.setObjectName(_fromUtf8("progressBar_3"))
        self.progressBar_4 = QtGui.QProgressBar(self.centralwidget)
        self.progressBar_4.setGeometry(QtCore.QRect(80, 240, 118, 23))
        self.progressBar_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar_4.setAutoFillBackground(False)
        self.progressBar_4.setMinimum(-60)
        self.progressBar_4.setMaximum(60)
        self.progressBar_4.setProperty("value", 0)
        self.progressBar_4.setInvertedAppearance(False)
        self.progressBar_4.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar_4.setObjectName(_fromUtf8("progressBar_4"))
        self.ksqueezedtextlabel = KSqueezedTextLabel(self.centralwidget)
        self.ksqueezedtextlabel.setGeometry(QtCore.QRect(0, 410, 124, 15))
        self.ksqueezedtextlabel.setObjectName(_fromUtf8("ksqueezedtextlabel"))
        self.ksqueezedtextlabel_2 = KSqueezedTextLabel(self.centralwidget)
        self.ksqueezedtextlabel_2.setGeometry(QtCore.QRect(40, 410, 124, 15))
        self.ksqueezedtextlabel_2.setObjectName(_fromUtf8("ksqueezedtextlabel_2"))
        self.ksqueezedtextlabel_3 = KSqueezedTextLabel(self.centralwidget)
        self.ksqueezedtextlabel_3.setGeometry(QtCore.QRect(200, 210, 124, 15))
        self.ksqueezedtextlabel_3.setObjectName(_fromUtf8("ksqueezedtextlabel_3"))
        self.ksqueezedtextlabel_7 = KSqueezedTextLabel(self.centralwidget)
        self.ksqueezedtextlabel_7.setGeometry(QtCore.QRect(200, 240, 124, 15))
        self.ksqueezedtextlabel_7.setObjectName(_fromUtf8("ksqueezedtextlabel_7"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        
        self.ksqueezedtextlabel_4.setText(_translate("MainWindow", "X", None))
        self.ksqueezedtextlabel_5.setText(_translate("MainWindow", "Y", None))
        self.ksqueezedtextlabel_6.setText(_translate("MainWindow", "Z", None))
        self.checkBox.setText(_translate("MainWindow", "Acc", None))
        self.checkBox_2.setText(_translate("MainWindow", "Gyr", None))
        self.checkBox_3.setText(_translate("MainWindow", "Mag", None))
        self.progressBar_3.setFormat(_translate("MainWindow", "%v", None))
        self.progressBar_4.setFormat(_translate("MainWindow", "%v", None))
        self.ksqueezedtextlabel.setText(_translate("MainWindow", "LM", None))
        self.ksqueezedtextlabel_2.setText(_translate("MainWindow", "RM", None))
        self.ksqueezedtextlabel_3.setText(_translate("MainWindow", "LS", None))
        self.ksqueezedtextlabel_7.setText(_translate("MainWindow", "RS", None))
        

from PyKDE4.kdeui import KDialog, KColorCombo, KSqueezedTextLabel
from PyQt4.Qwt5 import QwtPlot
'''import PyQt4.Qwt5 as Qwt
plot = Qwt.QwtPlot()'''
'from qwt_plot import QwtPlot'
