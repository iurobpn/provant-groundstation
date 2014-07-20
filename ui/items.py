__author__ = 'will'
from PyQt4 import QtGui, QtCore
from PyKDE4.kdeui import KVBox, KHBox, KColorButton

class CustomTreeItem( QtGui.QTreeWidgetItem ):
    '''
    Custom QTreeWidgetItem with Widgets
    '''

    def __init__( self,window, parent, name, view=None, color=True ):
        '''
        parent (QTreeWidget) : Item's QTreeWidget parent.
        name   (str)         : Item's name. just an example.
        '''
        if view:
            self.view = view
        if not view:
            view = parent.view
        self.window = window
        self._name = name
        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeItem, self ).__init__( parent )

        ## Column 0 - Text:
        self.setText( 0, name )

        ## Column 1 - SpinBox:
        if color:
            self.colorChooser = KColorButton(view)
            self.colorChooser.setGeometry(QtCore.QRect(0, 0, 10, 10))
    #        self.spinBox.setValue( 0 )
            view.setItemWidget( self, 1, self.colorChooser )
            view.connect( self.colorChooser, QtCore.SIGNAL("changed (const QColor&)"), self.colorChanged )



        ## Column 2 - Button:
        self.button = QtGui.QCheckBox( view)
        #self.button.setText( "button %s" %name )
        view.setItemWidget( self, 2, self.button )

        ## Signals
        view.connect( self.button, QtCore.SIGNAL("clicked()"), self.buttonPressed )

    @property
    def name(self):
        '''
        Return name ( 1st column text )
        '''
        return self.text(0)

    @property
    def value(self):
        '''
        Return value ( 2nd column int)
        '''
        return self.colorChooser.value()

    def buttonPressed(self):
        if self.button.isChecked():
            self.window.enable_plot(self._name)
        else:
            self.window.disable_plot(self._name)

    def colorChanged(self):
        print 'color changed'
        self.window.set_plot_color(self._name,self.colorChooser.color())