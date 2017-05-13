# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InDialogPersonnelNumberScanner.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_myDialogPersonnelNumberScanner(object):
    def setupUi(self, myDialogPersonnelNumberScanner):
        myDialogPersonnelNumberScanner.setObjectName("myDialogPersonnelNumberScanner")
        myDialogPersonnelNumberScanner.setWindowModality(QtCore.Qt.ApplicationModal)
        myDialogPersonnelNumberScanner.resize(401, 110)
        font = QtGui.QFont()
        font.setPointSize(12)
        myDialogPersonnelNumberScanner.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Images/Micrometer-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        myDialogPersonnelNumberScanner.setWindowIcon(icon)
        self.myGridLayoutDialogPersonnelNumber = QtWidgets.QGridLayout(myDialogPersonnelNumberScanner)
        self.myGridLayoutDialogPersonnelNumber.setObjectName("myGridLayoutDialogPersonnelNumber")
        self.myLineEditScanPersonnelNumber = QtWidgets.QLineEdit(myDialogPersonnelNumberScanner)
        self.myLineEditScanPersonnelNumber.setMinimumSize(QtCore.QSize(200, 0))
        self.myLineEditScanPersonnelNumber.setObjectName("myLineEditScanPersonnelNumber")
        self.myGridLayoutDialogPersonnelNumber.addWidget(self.myLineEditScanPersonnelNumber, 0, 1, 1, 1)
        self.myButtonBoxDialogPersonnelNumberScanner = QtWidgets.QDialogButtonBox(myDialogPersonnelNumberScanner)
        self.myButtonBoxDialogPersonnelNumberScanner.setOrientation(QtCore.Qt.Horizontal)
        self.myButtonBoxDialogPersonnelNumberScanner.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.myButtonBoxDialogPersonnelNumberScanner.setObjectName("myButtonBoxDialogPersonnelNumberScanner")
        self.myGridLayoutDialogPersonnelNumber.addWidget(self.myButtonBoxDialogPersonnelNumberScanner, 1, 1, 1, 1)
        self.myLabelPersonnelNumber = QtWidgets.QLabel(myDialogPersonnelNumberScanner)
        self.myLabelPersonnelNumber.setObjectName("myLabelPersonnelNumber")
        self.myGridLayoutDialogPersonnelNumber.addWidget(self.myLabelPersonnelNumber, 0, 0, 1, 1)

        self.retranslateUi(myDialogPersonnelNumberScanner)
        self.myButtonBoxDialogPersonnelNumberScanner.accepted.connect(myDialogPersonnelNumberScanner.accept)
        self.myButtonBoxDialogPersonnelNumberScanner.rejected.connect(myDialogPersonnelNumberScanner.reject)
        QtCore.QMetaObject.connectSlotsByName(myDialogPersonnelNumberScanner)

    def retranslateUi(self, myDialogPersonnelNumberScanner):
        _translate = QtCore.QCoreApplication.translate
        myDialogPersonnelNumberScanner.setWindowTitle(_translate("myDialogPersonnelNumberScanner", "Name / Personal Nr. eingeben - Scanner"))
        myDialogPersonnelNumberScanner.setAccessibleName(_translate("myDialogPersonnelNumberScanner", "myDialogPersonnelNumberScanner"))
        self.myLineEditScanPersonnelNumber.setAccessibleName(_translate("myDialogPersonnelNumberScanner", "myLineEditScanPersonnelNumber"))
        self.myButtonBoxDialogPersonnelNumberScanner.setAccessibleName(_translate("myDialogPersonnelNumberScanner", "myButtonBoxDialogPersonnelNumberScanner"))
        self.myLabelPersonnelNumber.setAccessibleName(_translate("myDialogPersonnelNumberScanner", "myLabelPersonnelNumber"))
        self.myLabelPersonnelNumber.setText(_translate("myDialogPersonnelNumberScanner", "Name / Personal Nr. scannen:"))

import InResources_rc
