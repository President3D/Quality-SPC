# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InFormEditTestInstruction.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_myFormEdit(object):
    def setupUi(self, myFormEdit):
        myFormEdit.setObjectName("myFormEdit")
        myFormEdit.resize(779, 610)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Images/Micrometer-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        myFormEdit.setWindowIcon(icon)
        self.myGridLayoutFormEdit = QtWidgets.QGridLayout(myFormEdit)
        self.myGridLayoutFormEdit.setContentsMargins(1, 1, 1, 1)
        self.myGridLayoutFormEdit.setSpacing(4)
        self.myGridLayoutFormEdit.setObjectName("myGridLayoutFormEdit")
        self.myTableViewEdit = QtWidgets.QTableView(myFormEdit)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.myTableViewEdit.setFont(font)
        self.myTableViewEdit.setStyleSheet("QHeaderView::section {\n"
"    background-color: lightgray;\n"
"    color: black;\n"
"    padding: 4px;\n"
"    border: 1px solid black;\n"
"}\n"
"\n"
"QHeaderView::section:checked\n"
"{\n"
"    background-color: lightgray;\n"
"}")
        self.myTableViewEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.myTableViewEdit.setEditTriggers(QtWidgets.QAbstractItemView.CurrentChanged|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.myTableViewEdit.setAlternatingRowColors(True)
        self.myTableViewEdit.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.myTableViewEdit.setObjectName("myTableViewEdit")
        self.myGridLayoutFormEdit.addWidget(self.myTableViewEdit, 2, 0, 1, 1)
        self.myLabelTestInstructionNamePageEdit = QtWidgets.QLabel(myFormEdit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myLabelTestInstructionNamePageEdit.sizePolicy().hasHeightForWidth())
        self.myLabelTestInstructionNamePageEdit.setSizePolicy(sizePolicy)
        self.myLabelTestInstructionNamePageEdit.setMinimumSize(QtCore.QSize(1, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.myLabelTestInstructionNamePageEdit.setFont(font)
        self.myLabelTestInstructionNamePageEdit.setObjectName("myLabelTestInstructionNamePageEdit")
        self.myGridLayoutFormEdit.addWidget(self.myLabelTestInstructionNamePageEdit, 1, 0, 1, 1)
        self.myFrameNavigationEdit = QtWidgets.QFrame(myFormEdit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myFrameNavigationEdit.sizePolicy().hasHeightForWidth())
        self.myFrameNavigationEdit.setSizePolicy(sizePolicy)
        self.myFrameNavigationEdit.setMinimumSize(QtCore.QSize(0, 80))
        self.myFrameNavigationEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.myFrameNavigationEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.myFrameNavigationEdit.setObjectName("myFrameNavigationEdit")
        self.myGridLayoutFrameNavigationEdit = QtWidgets.QGridLayout(self.myFrameNavigationEdit)
        self.myGridLayoutFrameNavigationEdit.setContentsMargins(1, 6, 1, 6)
        self.myGridLayoutFrameNavigationEdit.setSpacing(6)
        self.myGridLayoutFrameNavigationEdit.setObjectName("myGridLayoutFrameNavigationEdit")
        self.myToolButtonDownEdit = QtWidgets.QToolButton(self.myFrameNavigationEdit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myToolButtonDownEdit.sizePolicy().hasHeightForWidth())
        self.myToolButtonDownEdit.setSizePolicy(sizePolicy)
        self.myToolButtonDownEdit.setStyleSheet("#myToolButtonDownEdit {color: black;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(187, 187, 187, 255));\n"
"border-width: 1px;\n"
"border-color: gray;\n"
"border-style: outset;\n"
"border-radius: 2px;\n"
"padding: 3px}\n"
"#myToolButtonDownEdit:hover {color: black;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(187, 187, 187, 255));\n"
"border-width: 2px;\n"
"border-color: gray;\n"
"border-style: outset;\n"
"border-radius: 2px;\n"
"padding: 3px}\n"
"#myToolButtonDownEdit:pressed {color: black;\n"
"background-color: qlineargradient(spread:reflect, x1:0, y1:0.517, x2:0, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(218, 218, 218, 255));\n"
"border-width: 1px;\n"
"border-color: gray;\n"
"border-style: inset;\n"
"border-radius: 2px;\n"
"padding: 3px}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/Images/Down.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.myToolButtonDownEdit.setIcon(icon1)
        self.myToolButtonDownEdit.setIconSize(QtCore.QSize(30, 30))
        self.myToolButtonDownEdit.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.myToolButtonDownEdit.setObjectName("myToolButtonDownEdit")
        self.myGridLayoutFrameNavigationEdit.addWidget(self.myToolButtonDownEdit, 0, 3, 1, 1)
        self.myToolButtonDeleteEdit = QtWidgets.QToolButton(self.myFrameNavigationEdit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myToolButtonDeleteEdit.sizePolicy().hasHeightForWidth())
        self.myToolButtonDeleteEdit.setSizePolicy(sizePolicy)
        self.myToolButtonDeleteEdit.setStyleSheet("#myToolButtonDeleteEdit {color: black;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(187, 187, 187, 255));\n"
"border-width: 1px;\n"
"border-color: gray;\n"
"border-style: outset;\n"
"border-radius: 2px;\n"
"padding: 3px}\n"
"#myToolButtonDeleteEdit:hover {color: black;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(187, 187, 187, 255));\n"
"border-width: 2px;\n"
"border-color: gray;\n"
"border-style: outset;\n"
"border-radius: 2px;\n"
"padding: 3px}\n"
"#myToolButtonDeleteEdit:pressed {color: black;\n"
"background-color: qlineargradient(spread:reflect, x1:0, y1:0.517, x2:0, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(218, 218, 218, 255));\n"
"border-width: 1px;\n"
"border-color: gray;\n"
"border-style: inset;\n"
"border-radius: 2px;\n"
"padding: 3px}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/Images/Trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.myToolButtonDeleteEdit.setIcon(icon2)
        self.myToolButtonDeleteEdit.setIconSize(QtCore.QSize(30, 30))
        self.myToolButtonDeleteEdit.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.myToolButtonDeleteEdit.setObjectName("myToolButtonDeleteEdit")
        self.myGridLayoutFrameNavigationEdit.addWidget(self.myToolButtonDeleteEdit, 0, 2, 1, 1)
        self.myToolButtonSaveEdit = QtWidgets.QToolButton(self.myFrameNavigationEdit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myToolButtonSaveEdit.sizePolicy().hasHeightForWidth())
        self.myToolButtonSaveEdit.setSizePolicy(sizePolicy)
        self.myToolButtonSaveEdit.setStyleSheet("#myToolButtonSaveEdit {color: black;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(187, 187, 187, 255));\n"
"border-width: 1px;\n"
"border-color: gray;\n"
"border-style: outset;\n"
"border-radius: 2px;\n"
"padding: 3px}\n"
"#myToolButtonSaveEdit:hover {color: black;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(187, 187, 187, 255));\n"
"border-width: 2px;\n"
"border-color: gray;\n"
"border-style: outset;\n"
"border-radius: 2px;\n"
"padding: 3px}\n"
"#myToolButtonSaveEdit:pressed {color: black;\n"
"background-color: qlineargradient(spread:reflect, x1:0, y1:0.517, x2:0, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(218, 218, 218, 255));\n"
"border-width: 1px;\n"
"border-color: gray;\n"
"border-style: inset;\n"
"border-radius: 2px;\n"
"padding: 3px}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Icons/Images/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.myToolButtonSaveEdit.setIcon(icon3)
        self.myToolButtonSaveEdit.setIconSize(QtCore.QSize(30, 30))
        self.myToolButtonSaveEdit.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.myToolButtonSaveEdit.setObjectName("myToolButtonSaveEdit")
        self.myGridLayoutFrameNavigationEdit.addWidget(self.myToolButtonSaveEdit, 0, 0, 1, 1)
        self.myToolButtonAddEdit = QtWidgets.QToolButton(self.myFrameNavigationEdit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myToolButtonAddEdit.sizePolicy().hasHeightForWidth())
        self.myToolButtonAddEdit.setSizePolicy(sizePolicy)
        self.myToolButtonAddEdit.setStyleSheet("#myToolButtonAddEdit {color: black;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(187, 187, 187, 255));\n"
"border-width: 1px;\n"
"border-color: gray;\n"
"border-style: outset;\n"
"border-radius: 2px;\n"
"padding: 3px}\n"
"#myToolButtonAddEdit:hover {color: black;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(187, 187, 187, 255));\n"
"border-width: 2px;\n"
"border-color: gray;\n"
"border-style: outset;\n"
"border-radius: 2px;\n"
"padding: 3px}\n"
"#myToolButtonAddEdit:pressed {color: black;\n"
"background-color: qlineargradient(spread:reflect, x1:0, y1:0.517, x2:0, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(218, 218, 218, 255));\n"
"border-width: 1px;\n"
"border-color: gray;\n"
"border-style: inset;\n"
"border-radius: 2px;\n"
"padding: 3px}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Icons/Images/Plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.myToolButtonAddEdit.setIcon(icon4)
        self.myToolButtonAddEdit.setIconSize(QtCore.QSize(30, 30))
        self.myToolButtonAddEdit.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.myToolButtonAddEdit.setObjectName("myToolButtonAddEdit")
        self.myGridLayoutFrameNavigationEdit.addWidget(self.myToolButtonAddEdit, 0, 1, 1, 1)
        self.myToolButtonUpEdit = QtWidgets.QToolButton(self.myFrameNavigationEdit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myToolButtonUpEdit.sizePolicy().hasHeightForWidth())
        self.myToolButtonUpEdit.setSizePolicy(sizePolicy)
        self.myToolButtonUpEdit.setStyleSheet("#myToolButtonUpEdit {color: black;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(187, 187, 187, 255));\n"
"border-width: 1px;\n"
"border-color: gray;\n"
"border-style: outset;\n"
"border-radius: 2px;\n"
"padding: 3px}\n"
"#myToolButtonUpEdit:hover {color: black;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(187, 187, 187, 255));\n"
"border-width: 2px;\n"
"border-color: gray;\n"
"border-style: outset;\n"
"border-radius: 2px;\n"
"padding: 3px}\n"
"#myToolButtonUpEdit:pressed {color: black;\n"
"background-color: qlineargradient(spread:reflect, x1:0, y1:0.517, x2:0, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(218, 218, 218, 255));\n"
"border-width: 1px;\n"
"border-color: gray;\n"
"border-style: inset;\n"
"border-radius: 2px;\n"
"padding: 3px}")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Icons/Images/Up.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.myToolButtonUpEdit.setIcon(icon5)
        self.myToolButtonUpEdit.setIconSize(QtCore.QSize(30, 30))
        self.myToolButtonUpEdit.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.myToolButtonUpEdit.setObjectName("myToolButtonUpEdit")
        self.myGridLayoutFrameNavigationEdit.addWidget(self.myToolButtonUpEdit, 0, 4, 1, 1)
        self.myGridLayoutFormEdit.addWidget(self.myFrameNavigationEdit, 0, 0, 1, 1)
        self.myGridLayoutFormEdit.setRowStretch(0, 3)
        self.myGridLayoutFormEdit.setRowStretch(1, 1)
        self.myGridLayoutFormEdit.setRowStretch(2, 20)

        self.retranslateUi(myFormEdit)
        QtCore.QMetaObject.connectSlotsByName(myFormEdit)

    def retranslateUi(self, myFormEdit):
        _translate = QtCore.QCoreApplication.translate
        myFormEdit.setWindowTitle(_translate("myFormEdit", "Quality SPC - Editieren"))
        myFormEdit.setAccessibleName(_translate("myFormEdit", "myFormEdit"))
        self.myTableViewEdit.setAccessibleName(_translate("myFormEdit", "myTableViewEdit"))
        self.myLabelTestInstructionNamePageEdit.setAccessibleName(_translate("myFormEdit", "myLabelTestInstructionNamePageEdit"))
        self.myLabelTestInstructionNamePageEdit.setText(_translate("myFormEdit", "..."))
        self.myFrameNavigationEdit.setAccessibleName(_translate("myFormEdit", "myFrameNavigationEdit"))
        self.myToolButtonDownEdit.setAccessibleName(_translate("myFormEdit", "myToolButtonDownEdit"))
        self.myToolButtonDownEdit.setText(_translate("myFormEdit", "Nach Unten"))
        self.myToolButtonDeleteEdit.setAccessibleName(_translate("myFormEdit", "myToolButtonDeleteEdit"))
        self.myToolButtonDeleteEdit.setText(_translate("myFormEdit", "Zeile Löschen"))
        self.myToolButtonSaveEdit.setAccessibleName(_translate("myFormEdit", "myToolButtonSaveEdit"))
        self.myToolButtonSaveEdit.setText(_translate("myFormEdit", "Speichern"))
        self.myToolButtonAddEdit.setAccessibleName(_translate("myFormEdit", "myToolButtonAddEdit"))
        self.myToolButtonAddEdit.setText(_translate("myFormEdit", "Zeile Hinzufügen"))
        self.myToolButtonUpEdit.setAccessibleName(_translate("myFormEdit", "myToolButtonUpEdit"))
        self.myToolButtonUpEdit.setText(_translate("myFormEdit", "Nach Oben"))

import InResources_rc
