# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InDialogToleranceExceeded.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_myDialogToleranceExceeded(object):
    def setupUi(self, myDialogToleranceExceeded):
        myDialogToleranceExceeded.setObjectName("myDialogToleranceExceeded")
        myDialogToleranceExceeded.setWindowModality(QtCore.Qt.ApplicationModal)
        myDialogToleranceExceeded.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Images/Micrometer-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        myDialogToleranceExceeded.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(myDialogToleranceExceeded)
        self.gridLayout.setObjectName("gridLayout")
        self.myButtonBoxToleranceExceeded = QtWidgets.QDialogButtonBox(myDialogToleranceExceeded)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.myButtonBoxToleranceExceeded.setFont(font)
        self.myButtonBoxToleranceExceeded.setOrientation(QtCore.Qt.Horizontal)
        self.myButtonBoxToleranceExceeded.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.myButtonBoxToleranceExceeded.setObjectName("myButtonBoxToleranceExceeded")
        self.gridLayout.addWidget(self.myButtonBoxToleranceExceeded, 2, 0, 1, 1)
        self.myLabelToleranceExceeded = QtWidgets.QLabel(myDialogToleranceExceeded)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.myLabelToleranceExceeded.setFont(font)
        self.myLabelToleranceExceeded.setWordWrap(True)
        self.myLabelToleranceExceeded.setObjectName("myLabelToleranceExceeded")
        self.gridLayout.addWidget(self.myLabelToleranceExceeded, 0, 0, 1, 1)
        self.myTextBrowserToleranceExceeded = QtWidgets.QTextBrowser(myDialogToleranceExceeded)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.myTextBrowserToleranceExceeded.setFont(font)
        self.myTextBrowserToleranceExceeded.setReadOnly(False)
        self.myTextBrowserToleranceExceeded.setObjectName("myTextBrowserToleranceExceeded")
        self.gridLayout.addWidget(self.myTextBrowserToleranceExceeded, 1, 0, 1, 1)

        self.retranslateUi(myDialogToleranceExceeded)
        self.myButtonBoxToleranceExceeded.accepted.connect(myDialogToleranceExceeded.accept)
        self.myButtonBoxToleranceExceeded.rejected.connect(myDialogToleranceExceeded.reject)
        QtCore.QMetaObject.connectSlotsByName(myDialogToleranceExceeded)

    def retranslateUi(self, myDialogToleranceExceeded):
        _translate = QtCore.QCoreApplication.translate
        myDialogToleranceExceeded.setWindowTitle(_translate("myDialogToleranceExceeded", "Toleranzüberschreitung"))
        myDialogToleranceExceeded.setAccessibleName(_translate("myDialogToleranceExceeded", "myDialogToleranceExceeded"))
        self.myButtonBoxToleranceExceeded.setAccessibleName(_translate("myDialogToleranceExceeded", "myButtonBoxToleranceExceeded"))
        self.myLabelToleranceExceeded.setAccessibleName(_translate("myDialogToleranceExceeded", "myLabelToleranceExceeded"))
        self.myLabelToleranceExceeded.setText(_translate("myDialogToleranceExceeded", "Bitte geben Sie den Grund für die Toleranzüberschreitung ein, sofern Sie ihn kennen:"))
        self.myTextBrowserToleranceExceeded.setAccessibleName(_translate("myDialogToleranceExceeded", "myTextBrowserToleranceExceeded"))

import InResources_rc
