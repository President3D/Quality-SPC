# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InDialogContractNumberScanner.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_myDialogContractNumberScanner(object):
    def setupUi(self, myDialogContractNumberScanner):
        myDialogContractNumberScanner.setObjectName("myDialogContractNumberScanner")
        myDialogContractNumberScanner.setWindowModality(QtCore.Qt.ApplicationModal)
        myDialogContractNumberScanner.resize(340, 110)
        font = QtGui.QFont()
        font.setPointSize(12)
        myDialogContractNumberScanner.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Images/Micrometer-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        myDialogContractNumberScanner.setWindowIcon(icon)
        self.myGridLayoutDialogContractNumber = QtWidgets.QGridLayout(myDialogContractNumberScanner)
        self.myGridLayoutDialogContractNumber.setObjectName("myGridLayoutDialogContractNumber")
        self.myLabelContractNumber = QtWidgets.QLabel(myDialogContractNumberScanner)
        self.myLabelContractNumber.setObjectName("myLabelContractNumber")
        self.myGridLayoutDialogContractNumber.addWidget(self.myLabelContractNumber, 0, 0, 1, 1)
        self.myLineEditScanContractNumber = QtWidgets.QLineEdit(myDialogContractNumberScanner)
        self.myLineEditScanContractNumber.setMinimumSize(QtCore.QSize(200, 0))
        self.myLineEditScanContractNumber.setObjectName("myLineEditScanContractNumber")
        self.myGridLayoutDialogContractNumber.addWidget(self.myLineEditScanContractNumber, 0, 1, 1, 1)
        self.myButtonBoxDialogContractNumberScanner = QtWidgets.QDialogButtonBox(myDialogContractNumberScanner)
        self.myButtonBoxDialogContractNumberScanner.setOrientation(QtCore.Qt.Horizontal)
        self.myButtonBoxDialogContractNumberScanner.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.myButtonBoxDialogContractNumberScanner.setObjectName("myButtonBoxDialogContractNumberScanner")
        self.myGridLayoutDialogContractNumber.addWidget(self.myButtonBoxDialogContractNumberScanner, 1, 1, 1, 1)

        self.retranslateUi(myDialogContractNumberScanner)
        self.myButtonBoxDialogContractNumberScanner.accepted.connect(myDialogContractNumberScanner.accept)
        self.myButtonBoxDialogContractNumberScanner.rejected.connect(myDialogContractNumberScanner.reject)
        QtCore.QMetaObject.connectSlotsByName(myDialogContractNumberScanner)

    def retranslateUi(self, myDialogContractNumberScanner):
        _translate = QtCore.QCoreApplication.translate
        myDialogContractNumberScanner.setWindowTitle(_translate("myDialogContractNumberScanner", "Auftrag Nr. eingeben - Scanner"))
        myDialogContractNumberScanner.setAccessibleName(_translate("myDialogContractNumberScanner", "myDialogContractNumberScanner"))
        self.myLabelContractNumber.setAccessibleName(_translate("myDialogContractNumberScanner", "myLabelContractNumber"))
        self.myLabelContractNumber.setText(_translate("myDialogContractNumberScanner", "Auftrag Nr. scannen:"))
        self.myLineEditScanContractNumber.setAccessibleName(_translate("myDialogContractNumberScanner", "myLineEditScanContractNumber"))
        self.myButtonBoxDialogContractNumberScanner.setAccessibleName(_translate("myDialogContractNumberScanner", "myButtonBoxDialogContractNumberScanner"))

import InResources_rc
