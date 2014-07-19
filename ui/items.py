__author__ = 'will'
from PyQt4 import QtGui, QtCore
from PyKDE4.kdeui import KVBox, KHBox, KColorButton

class CustomTreeItem( QtGui.QTreeWidgetItem ):
    '''
    Custom QTreeWidgetItem with Widgets
    '''

    def __init__( self, parent, name, view=None, color=True ):
        '''
        parent (QTreeWidget) : Item's QTreeWidget parent.
        name   (str)         : Item's name. just an example.
        '''

        if view:
            self.view = view
        if not view:
            view = parent.view
        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeItem, self ).__init__( parent )

        ## Column 0 - Text:
        self.setText( 0, name )

        ## Column 1 - SpinBox:
        if color:
            self.spinBox = KColorButton(view)
            self.spinBox.setGeometry(QtCore.QRect(0, 0, 10, 10))
    #        self.spinBox.setValue( 0 )
            view.setItemWidget( self, 1, self.spinBox )

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
        return self.spinBox.value()

    def buttonPressed(self):
        '''
        Triggered when Item's button pressed.
        an example of using the Item's own values.
        '''
        print "This Item name:%s value:%i" %( self.name,
                                              self.value )
