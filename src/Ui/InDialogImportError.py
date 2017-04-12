# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InDialogImportError.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_myDialogImportError(object):
    def setupUi(self, myDialogImportError):
        myDialogImportError.setObjectName("myDialogImportError")
        myDialogImportError.setWindowModality(QtCore.Qt.ApplicationModal)
        myDialogImportError.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Images/Micrometer-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        myDialogImportError.setWindowIcon(icon)
        myDialogImportError.setAccessibleName("myDialogImportError")
        self.gridLayout = QtWidgets.QGridLayout(myDialogImportError)
        self.gridLayout.setObjectName("gridLayout")
        self.myTextBrowserImportError = QtWidgets.QTextBrowser(myDialogImportError)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.myTextBrowserImportError.setFont(font)
        self.myTextBrowserImportError.setObjectName("myTextBrowserImportError")
        self.gridLayout.addWidget(self.myTextBrowserImportError, 1, 0, 1, 1)
        self.myLabelImportError = QtWidgets.QLabel(myDialogImportError)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.myLabelImportError.setFont(font)
        self.myLabelImportError.setAccessibleName("myLabelImportError")
        self.myLabelImportError.setObjectName("myLabelImportError")
        self.gridLayout.addWidget(self.myLabelImportError, 0, 0, 1, 1)
        self.myButtonBoxImportError = QtWidgets.QDialogButtonBox(myDialogImportError)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.myButtonBoxImportError.setFont(font)
        self.myButtonBoxImportError.setOrientation(QtCore.Qt.Horizontal)
        self.myButtonBoxImportError.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Ignore)
        self.myButtonBoxImportError.setObjectName("myButtonBoxImportError")
        self.gridLayout.addWidget(self.myButtonBoxImportError, 2, 0, 1, 1)

        self.retranslateUi(myDialogImportError)
        self.myButtonBoxImportError.rejected.connect(myDialogImportError.reject)
        self.myButtonBoxImportError.accepted.connect(myDialogImportError.accept)
        QtCore.QMetaObject.connectSlotsByName(myDialogImportError)

    def retranslateUi(self, myDialogImportError):
        _translate = QtCore.QCoreApplication.translate
        myDialogImportError.setWindowTitle(_translate("myDialogImportError", "Fehler beim Datenimport"))
        self.myLabelImportError.setText(_translate("myDialogImportError", "Bitte folgende Probleme beheben:"))

import InResources_rc
