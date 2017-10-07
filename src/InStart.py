# Copyright 2017 Patrick Kuttruff
#
# -------------------- English --------------------
# This file is part of Quality SPC.
#
# Quality SPC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# Quality SPC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Quality SPC.  If not, see <http://www.gnu.org/licenses/>.
#
# -------------------- Deutsch --------------------
# Diese Datei ist Teil von Quality SPC.
#
# Quality SPC ist Freie Software: Sie können es unter den Bedingungen
# der GNU General Public License, wie von der Free Software Foundation,
# Version 3 der Lizenz oder jeder späteren veröffentlichten Version,
# weiterverbreiten und/oder modifizieren.
#
# Quality SPC wird in der Hoffnung, dass es nützlich sein wird, aber
# OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
# Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
# Siehe die GNU General Public License für weitere Details.
#
# Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
# Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.


# System specific parameters and functions
import sys, os

# PyQt Classes for the UI
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QGridLayout, QShortcut
from PyQt5.QtGui import QPixmap, QPaintDevice, QKeySequence
from PyQt5.QtCore import QUrl, QModelIndex, QLocale, QTranslator, QLibraryInfo, pyqtSlot

# Own UIs
from Ui.InMainWindow import Ui_myMainWindow

# Own Dialogs
from InDialog import MyDialogOpenTestInstruction, MyDialogToleranceExceeded, MyDialogOpenTestInstructionScanner, MyDialogOpenTestInstructionScanner2, MyDialogOpenTestInstructionScanner3

# Own Widgets
from InWidget import MyEditWidget

# Own model handlers
from InModel import MyCharacteristics, MyCharacteristicsTableModel, MyCharacteristicsAdjustView, MyDelegateComoBox1, MyDelegateComoBox2, MyDelegateSpinBox1, MyDelegateLineEdit1
from InControl import MyControl
from InResult import MyResult

# decimal for correctly rounded float point arithmetic
from decimal import Decimal

# csv for the new csv file
import csv

# for time and date handling
from datetime import datetime, date

# for plotting
from InPlot import MySpcCanvas, MyDeviationCanvas
from InSpcFull import MySpcFull, MyDeviationFull, MyResultList


# The main Window of the application
class MyMainWindow(QMainWindow, Ui_myMainWindow):
    def __init__(self):
        try:
            super(MyMainWindow, self).__init__()
            # Set up the MyMainWindow-UI from the designer
            self.setupUi(self)
            # Set the window title with the version number
            self.myWindowTitle = 'Quality SPC - v.1.08'
            self.setWindowTitle(self.myWindowTitle)
            # Set up the variables for the image and video handling
            self.myVisibleImage = None
            self.myCurrentImage = None
            self.myImageScaled = None
            self.myVideoFiles = None
            # Set up the variables for the control flow
            self.currentSampleValue = 0
            # Hide the buttons at the beginning
            self.myPushButtonForward.hide()
            self.myPushButtonBackward.hide()
            self.myPushButtonZoom.hide()
            self.myPushButtonVideo.hide()
            # Hide the actual value at the beginning
            self.hideActualValue()
            # Hide the SPC and Deviation Chart at the beginning
            self.myFrameSpc.hide()
            self.myFrameDeviation.hide()
            # Start the myImageResize-Method every time the image label is resized
            self.myLabelImage.resizeEvent = self.myImageResize
            # Convert the value every time it is changed
            self.myLineEditActualValue.textChanged.connect(self.convertValue)
            # Set up the signals and slots of the menubar
            self.myActionStartTesting.triggered.connect(self.startTesting)
            self.myActionStartTestingScanner.triggered.connect(self.startTestingScanner)
            self.myActionQuit.triggered.connect(self.closeEvent)
            self.myActionFullscreenTi.triggered.connect(self.showTestInstructionWidget)
            self.myActionFullscreenSpc.triggered.connect(self.showSpcWidget)
            self.myActionFullscreenDeviation.triggered.connect(self.showDeviationWidget)
            self.myActionResultlist.triggered.connect(self.showResultWidget)
            self.myActionLicense.triggered.connect(self.showLicenseWidget)
            self.myActionContact.triggered.connect(self.showContactWidget)
            self.myActionEditTestInstruction.triggered.connect(self.showEditWidget)
            self.myActionNewTestInstruction.triggered.connect(self.newTestInstruction)
            # Set up the signals and slots of the main window
            self.myPushButtonForward.clicked.connect(self.nextImage)
            self.myPushButtonBackward.clicked.connect(self.previousImage)
            self.myPushButtonZoom.clicked.connect(self.zoomImage)
            self.myPushButtonVideo.clicked.connect(self.startVideo)
            self.myToolButtonOk.clicked.connect(self.checkActualValueOk)
            self.myToolButtonNok.clicked.connect(self.checkActualValueNok)
            # Set up shortcuts with corresponding slots
            self.shortcutButtonOk = QShortcut(QKeySequence("Enter"), self)
            self.shortcutButtonOk.activated.connect(self.buttonOkShortcut)
            # Set up the SPC chart
            self.spcPlot = MySpcCanvas(self, self.myFrameSpc, width=self.myFrameSpc.width(), height=self.myFrameSpc.height(),dpi=QPaintDevice.logicalDpiX(self))
            self.myGridLayoutSpc.addWidget(self.spcPlot)
            # Set up the deviation chart
            self.deviationPlot = MyDeviationCanvas(self, self.myFrameDeviation, width=self.myFrameDeviation.width(), height=self.myFrameDeviation.height(), dpi=QPaintDevice.logicalDpiX(self))
            self.myGridLayoutDeviation.addWidget(self.deviationPlot)
            # Set up the SPC fullscreen chart
            self.spcFullPlot = MySpcCanvas(self, self.myFrameSpcFull, width=self.myFrameSpcFull.width(), height=self.myFrameSpcFull.height(),dpi=QPaintDevice.logicalDpiX(self))
            self.myVerticalLayoutFrameSpcFull.addWidget(self.spcFullPlot)
            # Set up the deviation fullscreen chart
            self.deviationFullPlot = MyDeviationCanvas(self, self.myFrameDeviationFull, width=self.myFrameDeviation.width(), height=self.myFrameDeviation.height(), dpi=QPaintDevice.logicalDpiX(self))
            self.myVerticalLayoutGroupBoxDeviationFull.addWidget(self.deviationFullPlot)
            # Make sure, the page which is shown is the test instruction page
            self.myStackedWidget.setCurrentWidget(self.myPageTestInstruction)
            # Show the license text on the license page
            self.myLicenseText = open(os.path.split(os.path.normpath(sys.argv[0]))[0] + os.sep + 'COPYING.txt', encoding='utf-8-sig').read()
            self.myTextBrowserLicense.setPlainText(self.myLicenseText)
            # Show the copyright information on the contact page
            self.myTextBrowserContact.setPlainText('Copyright © 2017 Patrick Kuttruff \n\nhttps://github.com/President3D/Quality-SPC')
        except Exception as e:
            self.myErrorMessage(str(e))

    # The slots to handle the shortcuts
    @pyqtSlot()
    def buttonOkShortcut(self):
        # Only apply the action, if the button is visible
        if self.myToolButtonOk.isVisible():
            self.checkActualValueOk()

    # To hide the content of the actual value groupbox, spc chart and deviation chart
    def hideActualValue(self):
        try:
            self.myLineEditActualValue.hide()
            self.myLineEditSerialNo.hide()
            self.myToolButtonOk.hide()
            self.myToolButtonNok.hide()
            self.myLabelActualValue.hide()
            self.myLabelSerialNo.hide()
            self.myLabelActualValuePreview.hide()
            self.myFrameSpc.hide()
            self.myFrameDeviation.hide()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Close the application with the X in the upper right corner or the Quit-Button
    def closeEvent(self, event):
        try:
            self.myCloseMessage = QMessageBox.question(self, 'Programm beenden', 'Programm beenden?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if self.myCloseMessage == QMessageBox.Yes:
                sys.exit()
            elif (self.myCloseMessage == QMessageBox.No) and (event is False):
                pass
            else:
                event.ignore()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Show the test instruction on the main screen
    def showTestInstructionWidget(self):
        try:
            self.myStackedWidget.setCurrentWidget(self.myPageTestInstruction)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Show the spc chart in fullscreen
    def showSpcWidget(self):
        try:
            self.myStackedWidget.setCurrentWidget(self.myPageSpc)
            # Check if there is an open test instruction. If not display a message. Else show the SPC chart
            try:
                self.startSpcFull = MySpcFull(self, self.myResult.returnResult())
            except:
                self.mySpcFullMessage = QMessageBox.information(self, 'Aktion nicht möglich', 'Sie müssen zuerst einen Prüfplan öffnen', QMessageBox.Ok)
                # Send the user back to the main page.
                self.myStackedWidget.setCurrentWidget(self.myPageTestInstruction)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Show the deviation chart in fullscreen
    def showDeviationWidget(self):
        try:
            self.myStackedWidget.setCurrentWidget(self.myPageDeviation)
            # Check if there is an open test instruction. If not display a message. Else show the deviation chart
            try:
                self.startDeviationFull = MyDeviationFull(self, self.myResult.returnResult())
            except:
                self.myDeviationFullMessage = QMessageBox.information(self, 'Aktion nicht möglich', 'Sie müssen zuerst einen Prüfplan öffnen', QMessageBox.Ok)
                # Send the user back to the main page.
                self.myStackedWidget.setCurrentWidget(self.myPageTestInstruction)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Show the result list
    def showResultWidget(self):
        try:
            self.myStackedWidget.setCurrentWidget(self.myPageResult)
            # Check if there is an open test instruction. If not display a message. Else show the result list
            try:
                self.startResultList = MyResultList(self, self.myResult.returnResult())
            except:
                self.myResultListMessage = QMessageBox.information(self, 'Aktion nicht möglich', 'Sie müssen zuerst einen Prüfplan öffnen', QMessageBox.Ok)
                # Send the user back to the main page.
                self.myStackedWidget.setCurrentWidget(self.myPageTestInstruction)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Show the licence
    def showLicenseWidget(self):
        try:
            self.myStackedWidget.setCurrentWidget(self.myPageLicense)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Show the contact information
    def showContactWidget(self):
        try:
            self.myStackedWidget.setCurrentWidget(self.myPageContact)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Show the edit widget 1
    def showEditWidget(self):
        try:
            # Check if there is an open test instruction. If not display a message. Else show the edit window
            try:
                # Check if the variable is valid. If it is not, the except occurs, because there is no open test instruction
                self.myData
                # Call the edit method and open the edit widget
                self.showEditWidget2()

            except:
                self.myEditFullMessage = QMessageBox.information(self, 'Aktion nicht möglich', 'Sie müssen zuerst einen Prüfplan öffnen', QMessageBox.Ok)
                # Send the user back to the main page.
                self.myStackedWidget.setCurrentWidget(self.myPageTestInstruction)
        except Exception as e:
            self.myErrorMessage(str(e))

    def showEditWidget2(self):
        try:
            # Clear the Tableview of the main window, so the user has to load it anew after he made changes. Important to use the automated checks.
            self.myTableViewCharacteristics.setModel(None)
            # Clear all elements of the main window
            self.clearMainWindow()
            # Set up the edit widget 1/2
            self.myEditForm = MyEditWidget(self)
            # Set up the edit widget 2/2
            self.myEditForm.startUi()
            # set up the table model
            self.myEditForm.myTableViewEdit.setModel(self.myTableModel)

            # Set up the signals and slots of the edit widget
            self.myEditForm.myToolButtonSaveEdit.clicked.connect(self.saveChanges)
            self.myEditForm.myToolButtonAddEdit.clicked.connect(self.insertRow)
            self.myEditForm.myToolButtonDeleteEdit.clicked.connect(self.removeRow)
            self.myEditForm.myToolButtonUpEdit.clicked.connect(self.moveUpRow)
            self.myEditForm.myToolButtonDownEdit.clicked.connect(self.moveDownRow)

            # set up the combo box delegate for the type
            self.myDelegateCombo1 = MyDelegateComoBox1()
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(2, self.myDelegateCombo1)

            # set up the spin box delegate for the ID, Frequency and Sample
            self.myDelegateSpin1 = MyDelegateSpinBox1()
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(0, self.myDelegateSpin1)
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(3, self.myDelegateSpin1)
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(4, self.myDelegateSpin1)

            # set up the combo box delegate for Absolut
            self.myDelegateCombo2 = MyDelegateComoBox2()
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(9, self.myDelegateCombo2)

            # set up the line edit delegate for floating point numbers
            self.myDelegateLineEdit1 = MyDelegateLineEdit1(self)
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(6, self.myDelegateLineEdit1)
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(8, self.myDelegateLineEdit1)
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(10, self.myDelegateLineEdit1)
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(11, self.myDelegateLineEdit1)
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(12, self.myDelegateLineEdit1)
            self.myEditForm.myTableViewEdit.setItemDelegateForColumn(13, self.myDelegateLineEdit1)

            # set the matching wide to the columns
            self.myEditForm.myTableViewEdit.resizeColumnsToContents()
            # Set the test instruction name to the table
            self.myEditForm.myLabelTestInstructionNamePageEdit.setText(os.path.normpath(self.myTestInstructionFile[0]))
            # show the edit form
            self.myEditForm.show()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Clear all elements of the main window
    def clearMainWindow(self):
        try:
            # Set the window title back to normal
            self.setWindowTitle(self.myWindowTitle)
            # Clear all labels
            self.myLabelTestInstruction.clear()
            self.myTextBrowserDescription.clear()
            self.myLabelType.clear()
            self.myLabelReference.clear()
            self.myLabelEquipment.clear()
            self.myLabelValue.clear()
            self.myLabelTolerance.clear()
            self.myLabelInterference.clear()
            # Hide the buttons, labels and line edits
            self.myToolButtonOk.hide()
            self.myToolButtonNok.hide()
            self.myPushButtonForward.hide()
            self.myPushButtonBackward.hide()
            self.myPushButtonZoom.hide()
            self.myPushButtonVideo.hide()
            self.myLabelActualValuePreview.hide()
            self.myLineEditActualValue.hide()
            self.myLineEditSerialNo.hide()
            self.myLabelActualValue.hide()
            self.myLabelSerialNo.hide()
            # Hide the SPC and Deviation Chart at the beginning
            self.myFrameSpc.hide()
            self.myFrameDeviation.hide()
            # Clear the image and imageAmount text
            self.myLabelImage.clear()
            self.myLabelImageAmount.setText('')
        except Exception as e:
            self.myErrorMessage(str(e))

    # Save the changed table model to the csv
    def saveChanges(self):
        # First save a copy of the old file. If the new one troubles you, you can easily restore the old one.
        try:
            # Check if a old data folder exists. If not, create it.
            self.myAltFilePath = os.path.split(os.path.normpath(self.myTestInstructionFile[0]))
            if not os.path.exists(os.path.join(self.myAltFilePath[0] + os.sep + self.myAltFilePath[1][:self.myAltFilePath[1].rfind('.')] + os.sep + 'Old')):
                os.makedirs(os.path.join(self.myAltFilePath[0] + os.sep + self.myAltFilePath[1][:self.myAltFilePath[1].rfind('.')] + os.sep + 'Old'))
            # Save the old data
            self.myData.to_csv(path_or_buf=os.path.abspath(os.path.join(self.myAltFilePath[0] + os.sep + self.myAltFilePath[1][:self.myAltFilePath[1].rfind('.')] + os.sep + 'Old' + os.sep + '{:%Y%m%d%H%M%S}'.format(datetime.now()) + '_' + str(self.myStaffNumber) + '.csv')), sep=';', encoding='utf-8-sig', mode='w', index=False, header=False)
            self.saveChanges2()
        except:
            pass

    # Save the changed table model to the csv 2
    def saveChanges2(self):
        # Overwrite the existing file with the edited file
        try:
            # Jump with the curser to the first cell and back to the last selected cell. Important to ensure contents do not get lost, if the user forgot to press enter after his last insertion.
            self.myDefaultEditIndex = self.myEditForm.myTableViewEdit.model().index(0, 0)
            # This try-except ensures that the app does not crash, if the user has not changed the initial selection of cell index(0,0)
            try:
                self.mySelectedEditIndex = self.myEditForm.myTableViewEdit.selectedIndexes()
                # If the current selected column is index 2 or 9, jump one column ahead to avoid a selection change
                if (self.mySelectedEditIndex[0].column() == 2) or (self.mySelectedEditIndex[0].column() == 9):
                    self.mySelectedEditIndex2 = self.myEditForm.myTableViewEdit.model().index(self.mySelectedEditIndex[0].row(), self.mySelectedEditIndex[0].column() + 1)
                else:
                    self.mySelectedEditIndex2 = self.myEditForm.myTableViewEdit.model().index(self.mySelectedEditIndex[0].row(), self.mySelectedEditIndex[0].column())
            except:
                self.myDefaultEditIndex = self.myEditForm.myTableViewEdit.model().index(0, 1)
                self.mySelectedEditIndex2 = self.myEditForm.myTableViewEdit.model().index(0, 0)
            # The actual cursor jump to the first cell and back to the last selected cell.
            self.myEditForm.myTableViewEdit.setCurrentIndex(self.myDefaultEditIndex)
            self.myEditForm.myTableViewEdit.setCurrentIndex(self.mySelectedEditIndex2)
            # Save the new test instruction
            self.myTableModel.myData.to_csv(path_or_buf=os.path.abspath(self.myTestInstructionFile[0]), sep=';', encoding='utf-8-sig', mode='w', index=False, header=False)
            # Change myData from InStart to the the newData of InModel
            self.myData = self.myTableModel.myData
        except:
            QMessageBox.warning(self, 'Vorgang nicht möglich', 'Beim Speichern ist ein Fehler aufgetreten.', QMessageBox.Ok)

    # Add a new row below the current selected row
    def insertRow(self):
        try:
            # The row number which is selected
            self.mySelectedIndex = self.myEditForm.myTableViewEdit.selectedIndexes()
            self.mySelectedIndexRow = self.mySelectedIndex[0].row()
        # If the user has nothing selected, use row 0
        except:
            self.mySelectedIndexRow = 0
        try:
            # The insertRow()-Method calls the insertRows()-Method of the tablemodel.
            self.myTableModel.insertRow(self.mySelectedIndexRow)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Delete the current selected row
    def removeRow(self):
        try:
            # The row number which is selected
            self.mySelectedIndex = self.myEditForm.myTableViewEdit.selectedIndexes()
            self.mySelectedIndexRow = self.mySelectedIndex[0].row()
            self.removeRow2()
        # If the user has nothing selected, do nothing
        except:
            pass

    # Delete the current selected row 2
    def removeRow2(self):
        try:
            # The removeRow()-Method calls the removeRows()-Method of the tablemodel.
            self.removeRowResult = self.myTableModel.removeRow(self.mySelectedIndexRow)
            if self.removeRowResult == False:
                QMessageBox.information(self.myEditForm, 'Aktion nicht möglich', 'Ein Prüfplan muss aus mindestens einem Merkmal (einer Zeile) bestehen.', QMessageBox.Ok)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Move the current seleted row up
    def moveUpRow(self):
        try:
            # The row number which is selected
            self.mySelectedIndex = self.myEditForm.myTableViewEdit.selectedIndexes()
            self.mySelectedIndexRow = self.mySelectedIndex[0].row()
            self.moveUpRow2()
        # If the user has nothing selected, do nothing
        except:
            pass

    # Move the current selected row up
    def moveUpRow2(self):
        try:
            if self.mySelectedIndexRow != 0:
                self.myTableModel.moveRows(self.mySelectedIndexRow, self.mySelectedIndexRow-1)
            else:
                QMessageBox.information(self.myEditForm, 'Aktion nicht möglich', 'Das Merkmal kann nicht nach oben verschoben werden.', QMessageBox.Ok)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Move the current selected row down
    def moveDownRow(self):
        try:
            # The row number which is selected
            self.mySelectedIndex = self.myEditForm.myTableViewEdit.selectedIndexes()
            self.mySelectedIndexRow = self.mySelectedIndex[0].row()
            self.moveDownRow2()
        # If the user has nothing selected, do nothing
        except:
            pass

    # Move the currend selected row down 2
    def moveDownRow2(self):
        # Only move the row down, if it is not the last row
        if (self.mySelectedIndexRow + 1) != len(self.myTableModel.myData):
            try:
                self.myTableModel.moveRows(self.mySelectedIndexRow, self.mySelectedIndexRow + 1)
            except Exception as e:
                self.myErrorMessage(str(e))
        else:
            try:
                QMessageBox.information(self.myEditForm, 'Aktion nicht möglich', 'Das Merkmal kann nicht nach unten verschoben werden.', QMessageBox.Ok)
            except Exception as e:
                self.myErrorMessage(str(e))

    # Start a new test instruction from scratch
    def newTestInstruction(self):
        try:
            self.myTestInstructionFile = QFileDialog.getSaveFileName(self, 'Neuer Prüfplan erstellen', filter='Prüfplan (*.csv)')
            # QFileDialog.getOpenFileName returns a tuple. On position [0] is the file path. If nothing is on position [0], the user clicked cancel.
            if self.myTestInstructionFile[0]:
                # Create an empty test instruction
                try:
                    with open(self.myTestInstructionFile[0], 'w', newline='', encoding='utf-8-sig') as myFile:
                        myCsvWriter = csv.writer(myFile, delimiter=';')
                        myCsvWriter.writerow(['1','','0','1','1','Neu','','','','0','','','','','','',''])
                except Exception as e:
                    self.myErrorMessage(str(e))
                # Create the dataframe. Corresponds to startTesting
                self.myDialogOpenTestInstruction = MyDialogOpenTestInstruction(self)
                self.myDialogOpenTestInstruction.startUi()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Load a test instruction and start the ui for the contract and staff number
    def startTesting(self):
        try:
            self.myTestInstructionFile = QFileDialog.getOpenFileName(self, 'Prüfplan öffnen [UTF-8]', filter='Prüfplan (*.csv)')
            # QFileDialog.getOpenFileName returns a tuple. On position [0] is the file path. If nothing is on position [0], the user clicked cancel.
            if self.myTestInstructionFile[0]:
                # Set up the dialog for the staff number and contract number. Use the self-parameter, because the Dialog has to send a sinal back.
                self.myDialogOpenTestInstruction = MyDialogOpenTestInstruction(self)
                self.myDialogOpenTestInstruction.startUi()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Assign the contract and staff number to self and check the characteristics for errors
    def startTesting2(self, myContractNumber, myStaffNumber):
        try:
            self.myContractNumber = myContractNumber
            self.myStaffNumber = myStaffNumber
            # Add the contract number and name to the window title
            self.setWindowTitle(self.myWindowTitle + ' - Name: ' + self.myStaffNumber + ' - Auftrag: ' + self.myContractNumber)
            # Start the MyCharacteristics class
            self.myCharacteristics = MyCharacteristics(self, self.myTestInstructionFile[0])
        except Exception as e:
            self.myErrorMessage(str(e))

    # Assign the data from the csv to self and create the model for the table view. Load the control data.
    def startTesting3(self, data):
        try:
            self.myData = data
            # Create the table model
            self.myTableModel = MyCharacteristicsTableModel(self.myData)
            # Create the table view
            self.myTableViewCharacteristics.setModel(self.myTableModel)
            self.myTableViewCharacteristics.resizeColumnsToContents()
            # Show the file name
            self.myLabelTestInstruction.setText(os.path.split(os.path.normpath(self.myTestInstructionFile[0]))[1])
            # Load the control data, which stores the frequency, how many times each characteristics has run
            self.myControlData = MyControl(self)
            # Load the result data, which stores the results
            self.myResult = MyResult(self)
            # Every Time a new line is selected, this code detects it and runs the newLineSelected-method.
            self.selectionModel = self.myTableViewCharacteristics.selectionModel()
            self.selectionModel.selectionChanged.connect(self.newLineSelection)
            # Proceed with the next step
            self.startTesting4()
        except Exception as e:
            self.myErrorMessage(str(e))

    def startTesting4(self):
        try:
            # Read the Material-No from the file name
            self.myMatNo = os.path.abspath(self.myTestInstructionFile[0])[os.path.abspath(self.myTestInstructionFile[0]).rfind(os.sep) + 1:]
            if '_' in self.myMatNo:
                self.myMatNo = self.myMatNo[:self.myMatNo.find('_')]
            else:
                self.myMatNo = self.myMatNo[:self.myMatNo.find('.')]
            # Set up the dict for the json output in the log file
            self.myResultLog = {}
            # Append the head data to the myResultLog dict
            self.myResultLog['0'] = {'Material_No.' : str(self.myMatNo), 'Contract_No.' : str(self.myContractNumber), 'Staff' : str(self.myStaffNumber)}
            # Set up the default values of the variables
            self.currentRow = 0
            self.currentSerialNo = {}
            self.showCurrentLine = False
            self.rowAmount = len(self.myData.index)
            # Detect the first appropriate row
            self.showCurrentLine = self.checkRow(self.currentRow)
            while self.showCurrentLine != True:
                if (self.currentRow + 1) > (self.rowAmount - 1):
                    self.currentRow = 0
                else:
                    self.currentRow = self.currentRow + 1
                self.showCurrentLine = self.checkRow(self.currentRow)
            # Save the control csv with the edited frequency
            self.myControlData.safeCsv()
            # Show the detected row
            self.myTableViewCharacteristics.setFocus()
            self.myTableViewCharacteristics.selectRow(self.currentRow)
            # Make sure, the page which is shown is the test instruction page
            self.myStackedWidget.setCurrentWidget(self.myPageTestInstruction)
            # If the test instruction only has one attribute, the charts only work, if you call newLineSelection manually
            self.newLineSelection()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Load the test instruction with barcode-scanner support
    def startTestingScanner(self):
        try:
            # Set up the dialog to scan the test instruction path or assignment number
            self.myDialogOpenTestInstructionScanner = MyDialogOpenTestInstructionScanner(self)
            self.myDialogOpenTestInstructionScanner.startUi()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Load the contract number with barcode-scanner support
    def startTestingScanner2(self, myTestInstructionPath):
        try:
            # Assign the scanned test instruction path the the tuple which holds it during manual opening
            self.myTestInstructionFile = (os.path.abspath(myTestInstructionPath), 'Prüfplan (*.csv)')
            # Set up the dialog to scan the contract number
            self.myDialogOpenTestInstructionScanner2 = MyDialogOpenTestInstructionScanner2(self)
            self.myDialogOpenTestInstructionScanner2.startUi()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Load the personnel number with barcode-scanner support
    def startTestingScanner3(self, myContractNumber):
        try:
            self.myContractNumber = myContractNumber
            self.myDialogOpenTestInstructionScanner3 = MyDialogOpenTestInstructionScanner3(self)
            self.myDialogOpenTestInstructionScanner3.startUi()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Root the Programm to the same result as startTesting2
    def startTestingScanner4(self, myStaffNumber):
        self.myStaffNumber = myStaffNumber
        # Add the contract number and name to the window title
        self.setWindowTitle(self.myWindowTitle + ' - Name: ' + self.myStaffNumber + ' - Auftrag: ' + self.myContractNumber)
        # Start the MyCharacteristics class
        self.myCharacteristics = MyCharacteristics(self, self.myTestInstructionFile[0])

    # Runs every time, a new line of the tables is selected
    def newLineSelection(self):
        try:
            # The current selected row number
            self.selectedRow = self.myTableViewCharacteristics.selectionModel().selectedRows()
            self.selectedRowNumber = self.selectedRow[0].row()
            # To ignore user clicks only select the row, if the selectedRowNumber == currentRow (1/2)
            if self.selectedRowNumber == self.currentRow:
                # Show the labels for the selected row
                self.adjustView = MyCharacteristicsAdjustView(self, self.selectedRowNumber)
                # Check if there is a video for the selected row
                self.myVideoFiles = self.adjustView.setVideoAmount()
                if len(self.myVideoFiles) == 0:
                    self.myPushButtonVideo.hide()
                else:
                    self.myPushButtonVideo.show()
                # Show the first image for the selected row
                self.myImageFiles = self.adjustView.setImageAmount()
                # Only set up the image, if there is a image
                if len(self.myImageFiles) > 0:
                    self.myPushButtonForward.show()
                    self.myPushButtonBackward.show()
                    self.myPushButtonZoom.show()
                    self.setUpImage(True)
                else:
                    self.myVisibleImage = None
                    self.myCurrentImage = None
                    self.myPushButtonForward.hide()
                    self.myPushButtonBackward.hide()
                    self.myPushButtonZoom.hide()
                    self.setUpImage(False)
                # Show the appropriate setpoint, SPC and deviation contents, according the the attribute type
                self.hideActualValue()
                # If it is quantitative
                if self.myData.iloc[self.selectedRowNumber, 2].strip() == '2':
                    self.showQuantitativeInput()
                # If it is qualitative
                elif self.myData.iloc[self.selectedRowNumber, 2].strip() == '1':
                    self.showQualitativeInput()
                # If it is informative
                else:
                    self.showInformativeInput()
            # To ignore user clicks only select the row, if the selectedRowNumber == currentRow (2/2)
            else:
                self.myTableViewCharacteristics.setFocus()
                self.myTableViewCharacteristics.selectRow(self.currentRow)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Check the current row if you should jump to the next or show it. Return True if you should show it. Else False.
    def checkRow(self, currentRow):
        try:
            self.thisRow = currentRow
            # Detect the controlFrequency and save it with +1
            self.controlFrequency = self.myControlData.returnFrequency(self.thisRow)
            self.myControlData.saveFrequency(self.controlFrequency + 1)
            # If not (control-frequency -1) % (frequency of the current row) == 0, than show the next row.
            if not self.controlFrequency % int(self.myData.iloc[self.thisRow][3].strip()) == 0:
                return False
            else:
                return True
        except Exception as e:
            self.myErrorMessage(str(e))

    # Set up the images
    def setUpImage(self, imageAvailable):
        try:
            # If there is at least one image
            if imageAvailable:
                self.myLabelImageAmount.setText('{0!s} / {1!s}'.format('1', len(self.myImageFiles)))
                self.myCurrentImage = self.myImageFiles[0]
                self.showImage()
            # If there is no image, clear the label
            else:
                # Clear the Label ans set myVisibleImage to None, so next and previous image functions will have not effect
                self.myLabelImage.clear()
                self.myLabelImageAmount.setText('{0!s} / {1!s}'.format('0', '0'))
        except Exception as e:
            self.myErrorMessage(str(e))

    # If next image is pressed
    def nextImage(self):
        # Show the next image if there is at least one image
        if self.myVisibleImage:
            try:
                if self.myImageFiles.index(self.myCurrentImage) + 1 == len(self.myImageFiles):
                    self.myCurrentImage = self.myImageFiles[0]
                    self.showImage()
                    self.myLabelImageAmount.setText('{0!s} / {1!s}'.format('1', len(self.myImageFiles)))
                else:
                    self.myCurrentImage = self.myImageFiles[self.myImageFiles.index(self.myCurrentImage) + 1]
                    self.showImage()
                    self.myLabelImageAmount.setText('{0!s} / {1!s}'.format(self.myImageFiles.index(self.myCurrentImage) + 1, len(self.myImageFiles)))
            except Exception as e:
                self.myErrorMessage(str(e))

    # If next image is pressed
    def previousImage(self):
        # Show the next image if there is at least one image
        if self.myVisibleImage:
            try:
                if self.myImageFiles.index(self.myCurrentImage) + 1 == 1:
                    self.myCurrentImage = self.myImageFiles[len(self.myImageFiles) - 1]
                    self.showImage()
                    self.myLabelImageAmount.setText('{0!s} / {1!s}'.format(len(self.myImageFiles), len(self.myImageFiles)))
                else:
                    self.myCurrentImage = self.myImageFiles[self.myImageFiles.index(self.myCurrentImage) - 1]
                    self.showImage()
                    self.myLabelImageAmount.setText('{0!s} / {1!s}'.format(self.myImageFiles.index(self.myCurrentImage) + 1, len(self.myImageFiles)))
            except Exception as e:
                self.myErrorMessage(str(e))

    # Standard function for the next and previous image functionality
    def showImage(self):
        try:
            self.myVisibleImage = QPixmap(os.path.abspath(self.myCurrentImage))
            self.myVisibleImageAspectRatio = self.myVisibleImage.width() / self.myVisibleImage.height()
            self.myLabelImage.resizeEvent(self)
        except Exception as e:
            self.myErrorMessage(str(e))

    # If the zoom button is pressed, show the image with the default program
    def zoomImage(self):
        if self.myVisibleImage:
            try:
                os.startfile(os.path.abspath(self.myCurrentImage), 'open')
            except Exception as e:
                self.myErrorMessage(str(e))

    # If the Video button is pressed, show the video with the default program
    def startVideo(self):
        if self.myVideoFiles:
            try:
                os.startfile(os.path.abspath(self.myVideoFiles[0]), 'open')
            except Exception as e:
                self.myErrorMessage(str(e))

    # Resize the image so it fits the current label size.
    def myImageResize(self, event):
        try:
            if self.myVisibleImage:
                self.myLabelAspectRatio = self.myLabelImage.width() / self.myLabelImage.height()
                if self.myVisibleImageAspectRatio >= self.myLabelAspectRatio:
                    self.myImageScaled = self.myVisibleImage.scaledToWidth(self.myLabelImage.width() - self.myLabelImage.lineWidth() - 2)
                else:
                    self.myImageScaled = self.myVisibleImage.scaledToHeight(self.myLabelImage.height() - self.myLabelImage.lineWidth() - 2)
                self.myLabelImage.setPixmap(self.myImageScaled)
        except Exception as e:
            self.myErrorMessage(str(e))

    # Every time the inserted value changed, run this code
    def convertValue(self):
        try:
            # Convert the user input to decimal
            self.myCurrentValue = Decimal((self.myLineEditActualValue.text().strip()).replace(',', '.'))
            # Get the current offset value. If not available, set it to 0.
            if (self.myData.iloc[self.currentRow, 8]).strip() == '':
                self.myCurrentOffset = Decimal(0)
            else:
                self.myCurrentOffset = Decimal(((self.myData.iloc[self.currentRow, 8]).strip()).replace(',', '.'))
            # myValue is the real measured value. Proceed with the tolerance and intervention checks.
            self.myAdjustedValue = self.myCurrentValue + self.myCurrentOffset
            # If the value is a absolute value, change the sign, if it is negative
            if (self.myData.iloc[self.currentRow, 9]).strip() == '1':
                self.myAdjustedValue = abs(self.myAdjustedValue)
            self.myLabelActualValuePreview.setText(str(self.myAdjustedValue))
            # Red background color if value is outside tolerance level
            if (self.myAdjustedValue < Decimal(((self.myData.iloc[self.currentRow, 11]).strip()).replace(',', '.'))) or (self.myAdjustedValue > Decimal(((self.myData.iloc[self.currentRow, 10]).strip()).replace(',', '.'))):
                self.myLabelActualValuePreview.setStyleSheet('border: 1px solid gray; border-radius: 2px; padding: 3 3px; background: rgb(255, 0, 0);')
            # Yellow background color if value is outside interference level
            elif (self.myAdjustedValue < Decimal(((self.myData.iloc[self.currentRow, 13]).strip()).replace(',', '.'))) or (self.myAdjustedValue > Decimal(((self.myData.iloc[self.currentRow, 12]).strip()).replace(',', '.'))):
                self.myLabelActualValuePreview.setStyleSheet('border: 1px solid gray; border-radius: 2px; padding: 3 3px; background: rgb(255, 255, 0);')
            # Green background color if value is inside interference level
            else:
               self.myLabelActualValuePreview.setStyleSheet('border: 1px solid gray; border-radius: 2px; padding: 3 3px; background: rgb(0, 170, 0);')
        except:
            self.myLabelActualValuePreview.setText('Ungültig')
            # Blue background color if value is not valid
            self.myLabelActualValuePreview.setStyleSheet('border: 1px solid gray; border-radius: 2px; padding: 3 3px; background: rgb(0, 85, 255);')


    # Set the actual value contets if the attribute is quantitative
    def showQuantitativeInput(self):
        try:
            self.myToolButtonOk.setText('{0!s}'.format('OK'))
            self.myLineEditActualValue.show()
            self.myLineEditSerialNo.show()
            self.myToolButtonOk.show()
            self.myLabelActualValue.show()
            self.myLabelSerialNo.show()
            self.myLabelActualValuePreview.show()
            # Suggest serial no if available
            self.showSerialNo()
            # Set the focus to the input line for a better usability
            self.myLineEditActualValue.setFocus()
            # Update the date of the spc and deviation charts and show them
            # Update and show the Spc plot
            self.showSpc = self.spcPlot.update_figure(self.myResult.returnResult(), float(((self.myData.iloc[self.currentRow, 12]).strip()).replace(',', '.')), float(((self.myData.iloc[self.currentRow, 13]).strip()).replace(',', '.')))
            # Only show the SPC plot, if there is data. Else do not show it.
            if self.showSpc:
                self.myFrameSpc.show()
            # Update and show the deviation chart
            self.showDeviation = self.deviationPlot.update_figure(self.myResult.returnResult())
            # Only show the deviation chart, if there is enough data. Else do not show it.
            if self.showDeviation:
                self.myFrameDeviation.show()
        except Exception as e:
            self.myErrorMessage(str(e))


    # Set the actual value contets if the attribute is qualitative
    def showQualitativeInput(self):
        try:
            self.myToolButtonOk.setText('{0!s}'.format('i.O.'))
            self.myLabelSerialNo.show()
            self.myLineEditSerialNo.show()
            self.myToolButtonOk.show()
            self.myToolButtonNok.show()
            # Suggest serial no if available
            self.showSerialNo()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Set the actual value contets if the attribute is informative
    def showInformativeInput(self):
        try:
            self.myToolButtonOk.setText('{0!s}'.format('Weiter'))
            self.myToolButtonOk.show()
        except Exception as e:
            self.myErrorMessage(str(e))

    # If available suggest a serial no
    def showSerialNo(self):
        try:
            if self.currentSampleValue in self.currentSerialNo:
                self.myLineEditSerialNo.setText(self.currentSerialNo[self.currentSampleValue])
            else:
                self.myLineEditSerialNo.clear()
        except Exception as e:
            self.myErrorMessage(str(e))

    # If the user clicks OK in the actual value groupbox
    def checkActualValueOk(self):
        try:
            # If there is a serial no, safe it with the key currentSampleValue in the dict currentSerialNo.
            # Else clear that key in the dict
            if (self.myData.iloc[self.currentRow, 2].strip() == '1') or (self.myData.iloc[self.currentRow, 2].strip() == '2'):
                if self.myLineEditSerialNo.text().strip() != '':
                    self.currentSerialNo[self.currentSampleValue] = self.myLineEditSerialNo.text().strip()
                else:
                    if self.currentSampleValue in self.currentSerialNo:
                        del self.currentSerialNo[self.currentSampleValue]
            # If the characteristic is informative
            if self.myData.iloc[self.currentRow, 2].strip() == '0':
                self.staticRow = 0
            # If the characteristic is qualitative
            elif self.myData.iloc[self.currentRow, 2].strip() == '1':
                self.staticRow = 1
            # If the characteristic is quantitative
            elif self.myData.iloc[self.currentRow, 2].strip() == '2':
                self.staticRow = 2
            # Use the staticRow-Variable, becouse the currentRow can change during the next if, what causes problems
            if self.staticRow == 0:
                # Proceed with Informative
                self.checkInformative1()
            elif self.staticRow == 1:
                # Proceed with Qualitative
                self.checkQualitative1()
            elif self.staticRow == 2:
                # Proceed with Quantitative
                # Check if the entered value is valid
                try:
                    self.currentValue = Decimal(((self.myLineEditActualValue.text()).strip()).replace(',', '.'))
                    self.proceed = True
                except:
                    self.proceed = False
                    self.myDecimalWarningMessage = QMessageBox.warning(self, 'Der Messwert ist ungültig', 'Geben Sie einen gültigen Messwert ein.\n(Eine Dezimalzahl)', QMessageBox.Ok)
                    if self.myDecimalWarningMessage == QMessageBox.Ok:
                        pass
                if self.proceed == True:
                    # If the value is valid, proceed to the tolerance check
                    self.checkQuantitative1()
        except Exception as e:
            self.myErrorMessage(str(e))

    # If the user clicks not OK in the actual value groupbox
    def checkActualValueNok(self):
        try:
            # If there is a serial no, safe it with the key currentSampleValue in the dict currentSerialNo.
            # Else clear that key in the dict
            if self.myLineEditSerialNo.text().strip() != '':
                self.currentSerialNo[self.currentSampleValue] = self.myLineEditSerialNo.text().strip()
            else:
                if self.currentSampleValue in self.currentSerialNo:
                    del self.currentSerialNo[self.currentSampleValue]
            # Ask the user if it is true, that the outcome was bad
            self.myNokWarningMessage = QMessageBox.warning(self, 'Das Prüfergebnis ist n.i.O.', 'Sind Sie sicher, dass das Prüfergebnis n.i.O. ist?', QMessageBox.Discard | QMessageBox.Yes, QMessageBox.Discard)
            if self.myNokWarningMessage == QMessageBox.Discard:
                # The user can correct his choice
                pass
            else:
                # Proceed with the reason for the bad value
                self.checkQualitative2()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Tolerance check
    def checkQuantitative1(self):
        try:
            # Get the current offset value. If not available, set it to 0.
            if (self.myData.iloc[self.currentRow, 8]).strip() == '':
                self.currentOffset = Decimal(0)
            else:
                self.currentOffset = Decimal(((self.myData.iloc[self.currentRow, 8]).strip()).replace(',', '.'))
            # The adjustedValue is the real measured value. Proceed with the tolerance and intervention checks.
            self.adjustedValue = self.currentValue + self.currentOffset
            # If the value is a absolute value, change the sign, if it is negative
            if (self.myData.iloc[self.currentRow, 9]).strip() == '1':
                self.adjustedValue = abs(self.adjustedValue)
            # Is the value inside of the tolerance level?
            if (self.adjustedValue < Decimal(((self.myData.iloc[self.currentRow, 11]).strip()).replace(',', '.'))) or (self.adjustedValue > Decimal(((self.myData.iloc[self.currentRow, 10]).strip()).replace(',', '.'))):
                self.myToleranceWarningMessage = QMessageBox.warning(self, 'Der Messwert ist außerhalb der Toleranz', 'Sind Sie sicher, dass der Messwert richtig ist?', QMessageBox.Discard | QMessageBox.Yes, QMessageBox.Discard)
                if self.myToleranceWarningMessage == QMessageBox.Discard:
                    # The user can insert a new value
                    pass
                else:
                    # Proceed with the reason for the bad value
                    self.checkQuantitative2()
            else:
                # Proceed with the intervention check
                self.checkQuantitative3()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Enter a reason for the value outside of the tolerance level
    def checkQuantitative2(self):
        try:
            self.myDialogToleranceExceeded = MyDialogToleranceExceeded(self)
            self.myDialogToleranceExceeded.startUi()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Interference check
    def checkQuantitative3(self):
        try:
            # Is the value inside of the interference level?
            if (self.adjustedValue < Decimal(((self.myData.iloc[self.currentRow, 13]).strip()).replace(',', '.'))) or (self.adjustedValue > Decimal(((self.myData.iloc[self.currentRow, 12]).strip()).replace(',', '.'))):
                self.myInterferenceWarningMessage = QMessageBox.warning(self, 'Der Messwert ist außerhalb der Eingriffsgrenze', 'Korrigieren Sie die betreffenden Prozessparameter', QMessageBox.Ok)
                if self.myInterferenceWarningMessage == QMessageBox.Ok:
                    self.checkQuantitative4('')
            else:
                self.checkQuantitative4('')
        except Exception as e:
            self.myErrorMessage(str(e))

    # Check if enough samples
    def checkQuantitative4(self, comment):
        try:
            self.myComment = comment
            self.currentSampleValue = self.currentSampleValue + 1
            # Stay at this row, if there are more samples
            if self.currentSampleValue < int((self.myData.iloc[self.currentRow, 4]).strip()):
                self.myResult.saveResult(int((self.myData.iloc[self.currentRow, 0]).strip()), self.adjustedValue, self.myLineEditSerialNo.text().strip(), '{:%d.%m.%Y}'.format(datetime.now()), '{:%H:%M:%S}'.format(datetime.now()), self.myStaffNumber, self.myComment)
                # Clear the rows
                self.myLineEditActualValue.clear()
                self.myLineEditSerialNo.clear()
                # Suggest serial no if available
                self.showSerialNo()
                self.myTableViewCharacteristics.setFocus()
                # Refresh the charts, to show the results of the last sample
                # Update and show the Spc plot
                self.showSpc = self.spcPlot.update_figure(self.myResult.returnResult(), float(((self.myData.iloc[self.currentRow, 12]).strip()).replace(',', '.')), float(((self.myData.iloc[self.currentRow, 13]).strip()).replace(',', '.')))
                # Only show the SPC plot, if there is data. Else do not show it.
                if self.showSpc:
                    self.myFrameSpc.show()
                # Update and show the deviation chart
                self.showDeviation = self.deviationPlot.update_figure(self.myResult.returnResult())
                # Only show the deviation chart, if there is enough data. Else do not show it.
                if self.showDeviation:
                    self.myFrameDeviation.show()
            # Proceed to the next row, if all samples are met
            else:
                # Reset the currentSampleValue
                self.currentSampleValue = 0
                # Save the result data
                self.myResult.saveResult(int((self.myData.iloc[self.currentRow, 0]).strip()), self.adjustedValue, self.myLineEditSerialNo.text().strip(), '{:%d.%m.%Y}'.format(datetime.now()), '{:%H:%M:%S}'.format(datetime.now()), self.myStaffNumber, self.myComment)
                # Clear the rows
                self.myLineEditActualValue.clear()
                self.myLineEditSerialNo.clear()
                # Next row
                self.nextRow()
        except Exception as e:
            self.myErrorMessage(str(e))

    # OK pressed with a qualitative attribute
    def checkQualitative1(self):
        try:
            self.currentSampleValue = self.currentSampleValue + 1
            # Stay at this row, if there are more samples
            if self.currentSampleValue < int((self.myData.iloc[self.currentRow, 4]).strip()):
                self.myComment = ''
                self.myResult.saveResult(int((self.myData.iloc[self.currentRow, 0]).strip()), 'i.O.', self.myLineEditSerialNo.text().strip(), '{:%d.%m.%Y}'.format(datetime.now()), '{:%H:%M:%S}'.format(datetime.now()), self.myStaffNumber, self.myComment)
                # Clear the rows
                self.myLineEditSerialNo.clear()
                # Suggest serial no if available
                self.showSerialNo()
                self.myTableViewCharacteristics.setFocus()
            # Proceed to the next row, if all samples are met
            else:
                # Reset the currentSampleValue
                self.currentSampleValue = 0
                # Save the result data
                self.myComment = ''
                self.myResult.saveResult(int((self.myData.iloc[self.currentRow, 0]).strip()), 'i.O.', self.myLineEditSerialNo.text().strip(), '{:%d.%m.%Y}'.format(datetime.now()), '{:%H:%M:%S}'.format(datetime.now()), self.myStaffNumber, self.myComment)
                # Clear the rows
                self.myLineEditSerialNo.clear()
                # Next row
                self.nextRow()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Enter a reason for the value outside of the tolerance level
    def checkQualitative2(self):
        try:
            self.myDialogToleranceExceeded = MyDialogToleranceExceeded(self)
            self.myDialogToleranceExceeded.startUi2()
        except Exception as e:
            self.myErrorMessage(str(e))

        # Check if enough samples
    def checkQualitative3(self, comment):
        try:
            self.myComment = comment
            self.currentSampleValue = self.currentSampleValue + 1
            # Stay at this row, if there are more samples
            if self.currentSampleValue < int((self.myData.iloc[self.currentRow, 4]).strip()):
                self.myResult.saveResult(int((self.myData.iloc[self.currentRow, 0]).strip()), 'n.i.O.', self.myLineEditSerialNo.text().strip(), '{:%d.%m.%Y}'.format(datetime.now()), '{:%H:%M:%S}'.format(datetime.now()), self.myStaffNumber, self.myComment)
                # Clear the rows
                self.myLineEditSerialNo.clear()
                # Suggest serial no if available
                self.showSerialNo()
                self.myTableViewCharacteristics.setFocus()
            # Proceed to the next row, if all samples are met
            else:
                # Reset the currentSampleValue
                self.currentSampleValue = 0
                # Save the result data
                self.myResult.saveResult(int((self.myData.iloc[self.currentRow, 0]).strip()), 'n.i.O.', self.myLineEditSerialNo.text().strip(), '{:%d.%m.%Y}'.format(datetime.now()), '{:%H:%M:%S}'.format(datetime.now()), self.myStaffNumber, self.myComment)
                # Clear the rows
                self.myLineEditSerialNo.clear()
                # Next row
                self.nextRow()
        except Exception as e:
            self.myErrorMessage(str(e))

    def checkInformative1(self):
        try:
            self.currentSampleValue = self.currentSampleValue + 1
            # Stay at this row, if there are more samples
            if self.currentSampleValue < int((self.myData.iloc[self.currentRow, 4]).strip()):
                self.myTableViewCharacteristics.setFocus()
            # Proceed to the next row, if all samples are met
            else:
                # Reset the currentSampleValue
                self.currentSampleValue = 0
                # Next row
                self.nextRow()
        except Exception as e:
            self.myErrorMessage(str(e))

    # Proceed to the next row
    def nextRow(self):
        try:
            self.showCurrentLine = False
            # Detect the next appropriate row
            while self.showCurrentLine != True:
                if (self.currentRow + 1) > (self.rowAmount - 1):
                    break
                else:
                    self.currentRow = self.currentRow + 1
                self.showCurrentLine = self.checkRow(self.currentRow)
            # If the user reached the last line, save the json log file and show the end message
            if self.showCurrentLine != True:
                self.currentSerialNo = {}
                # Save the json log file
                self.myResult.saveResultLog2('{:%Y%m%d%H%M%S}'.format(datetime.now()))
                # Show the end message
                self.endMessage()
            else:
                # Save the control csv with the edited frequency
                self.myControlData.safeCsv()
                # Show the detected row
                self.myTableViewCharacteristics.setFocus()
                self.myTableViewCharacteristics.selectRow(self.currentRow)
        except Exception as e:
            self.myErrorMessage(str(e))

    # If there is no next Row, show this message
    def endMessage(self):
        try:
            self.myEndMessage = QMessageBox.information(self, 'Die Prüfschritte sind abgeschlossen', 'Der Prüfablauf beginnt erneut', QMessageBox.Ok)
            self.startTesting4()
        except Exception as e:
            self.myErrorMessage(str(e))

    def myErrorMessage(self, error):
        QMessageBox.critical(self, 'Aktion nicht möglich', error)
        pass


# Start the application
try:
    spcApp = None

    def run():
        # Start the GUI with QApplication. The sys.argv is a parameter list of arguments from the command line.
        # On Position [0] of sys.argv is the path of the application.
        global spcApp
        spcApp = QApplication(sys.argv)

        # Install a translator, so the built in strings (e.g. buttons) are labeled with the right language.
        try:
            translator = QTranslator(spcApp)
            locale = QLocale.system().name()
            path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
            translator.load('qt_%s' %locale, path)
            spcApp.installTranslator(translator)
        # If the translator could not be installed, the app will start with default english.
        except:
            pass

        # exec_ = the main loop of the application.
        # sys.exit = The mainloop ends if we call exit(). sys.exit() ensures a clean exit.
        spcAppWindow = MyMainWindow()
        spcAppWindow.show()
        sys.exit(spcApp.exec_())

    if __name__ == '__main__':
        run()

except Exception as e:
    print('Error: ' + str(e))
