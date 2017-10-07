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

# csv for the csv file handling
import csv

# PyQt Classes for the UI
from PyQt5.QtWidgets import QDialog, QMessageBox, QWidget

# Own UIs
from Ui.InDialogOpenTestInstruction import Ui_myDialogOpenTestInstruction
from Ui.InDialogImportError import Ui_myDialogImportError
from Ui.InDialogToleranceExceeded import Ui_myDialogToleranceExceeded
from Ui.InDialogOpenTestInstructionScanner import Ui_myDialogOpenTestInstructionScanner
from Ui.InDialogContractNumberScanner import Ui_myDialogContractNumberScanner
from Ui.InDialogPersonnelNumberScanner import Ui_myDialogPersonnelNumberScanner


# The dialog for the staff number and contract number
class MyDialogOpenTestInstruction(QDialog, Ui_myDialogOpenTestInstruction):
    def __init__(self, myParent):
        super(MyDialogOpenTestInstruction, self).__init__()
        self.myParent = myParent

    def startUi(self):
        # Set up the ui from designer, minimum size
        self.setupUi(self)
        self.resize(0, 0)
        self.show()
        # Check which button the user presses
        self.myButtonBoxOpenTestInstruction.accepted.connect(self.ok)

    def ok(self):
        if (str(self.myLineEditContractNumber.text()) == '') or (str(self.myLineEditContractNumber.text()).isspace() == True) or (str(self.myLineEditStaffNumber.text()) == '') or (str(self.myLineEditStaffNumber.text()).isspace() == True):
            self.myInsertSthMessage = QMessageBox.warning(self, 'Daten eingeben', 'Bitte geben Sie eine Auftragsnummer und \neinen Namen bzw. Personal-Nr. ein.', QMessageBox.Ok)
            self.show()
        else:
            # Start the next method in InStart
            self.myParent.startTesting2(str(self.myLineEditContractNumber.text()).strip(), str(self.myLineEditStaffNumber.text()).strip())


# The dialog for the import errors
class MyDialogImportError(QDialog, Ui_myDialogImportError):
    def __init__(self, parent):
        super(MyDialogImportError, self).__init__()
        self.myParent = parent


    def startUi(self):
        # Set up the ui from designer
        self.setupUi(self)
        # Import error messages
        self.myErrorText = ''
        for myError in self.myParent.myImportReport:
            self.myErrorText = self.myErrorText + myError + '\n\n'
        self.myTextBrowserImportError.setPlainText(self.myErrorText)
        self.show()
        # The ignore button has the accepted role. Go on, if it is pressed.
        self.myButtonBoxImportError.accepted.connect(self.ignore)

    def ignore(self):
        # If the user ignores the waring go on and create the table model
        self.myParent.createTableModel()


# the dialog for the reason if a tolerance is exceeded
class MyDialogToleranceExceeded(QDialog, Ui_myDialogToleranceExceeded):
    def __init__(self, parent):
        super(MyDialogToleranceExceeded, self).__init__()
        self.myParent = parent

    # The UI for quantitative attributes
    def startUi(self):
        # Set up the ui from designer
        self.setupUi(self)
        self.show()
        # Check which button the user presses
        self.myButtonBoxToleranceExceeded.accepted.connect(self.ok)

    # The function for quantitative attributes
    def ok(self):
        # Delete all new line characters and return the comment, if there is one. Else return an empty string
        try:
            self.myExplanationText = self.myTextBrowserToleranceExceeded.toPlainText()
            self.myExplanationText = ' '.join(self.myExplanationText.split())
        except:
            self.myExplanationText = ''
        self.myParent.checkQuantitative4(str(self.myExplanationText))

    # The UI for qualitative attributes
    def startUi2(self):
        # Set up the ui from designer
        self.setupUi(self)
        self.show()
        # Check which button the user presses
        self.myButtonBoxToleranceExceeded.accepted.connect(self.ok2)

    # The function for qualitative attributes
    def ok2(self):
        # Delete all new line characters and return the comment, if there is one. Else return an empty string
        try:
            self.myExplanationText = self.myTextBrowserToleranceExceeded.toPlainText()
            self.myExplanationText = ' '.join(self.myExplanationText.split())
        except:
            self.myExplanationText = ''
        self.myParent.checkQualitative3(str(self.myExplanationText))


# The dialog to scan the test instruction path or assignment number
class MyDialogOpenTestInstructionScanner(QDialog, Ui_myDialogOpenTestInstructionScanner):
    def __init__(self, myParent):
        super(MyDialogOpenTestInstructionScanner, self).__init__()
        self.myParent = myParent

    def startUi(self):
        # Set up the ui from designer, minimum size
        self.setupUi(self)
        self.resize(0, 0)
        self.show()
        # Check which button the user presses
        self.myButtonBoxOpenTestInstructionScanner.accepted.connect(self.ok)

    def ok(self):
        # Error message, if there is no input or only space
        if (str(self.myLineEditScanPath.text()) == '') or (str(self.myLineEditScanPath.text()).isspace() == True):
            self.myScanPathMessage = QMessageBox.warning(self, 'Pfad scannen', 'Bitte scannen Sie einen Pfad\noder eine Zuordnungsnummer.', QMessageBox.Ok)
            self.show()
        # Validate if the file is a .csv file and start testing
        elif (str(self.myLineEditScanPath.text())[str(self.myLineEditScanPath.text()).rfind('.'):].lower() == '.csv'):
            self.myParent.startTestingScanner2(str(self.myLineEditScanPath.text()))
        # Check if there is a path in the assignment file, according to the non-valid-path-input.
        else:
            # Print a warning, if there is no assignment file
            if not os.path.exists(os.path.split(os.path.normpath(sys.argv[0]))[0] + os.sep + 'Assignment.csv'):
                self.myAssignmentPathMessage = QMessageBox.warning(self, 'Pfad scannen', 'Die Eingabe ist kein gültiger Pfad und\nes existiert keine Zuordnungstabelle.', QMessageBox.Ok)
                self.show()
            else:
                # Check if the assignment file contains a link to another file
                self.myPathToCsv = None
                with open(os.path.split(os.path.normpath(sys.argv[0]))[0] + os.sep + 'Assignment.csv', 'r', encoding='utf-8-sig') as myFile:
                    csvReader = csv.reader(myFile, delimiter=';')
                    for row in csvReader:
                        if os.path.exists(str(row[0]).strip()):
                            self.myPathToCsv = str(row[0]).strip()

                # Append all data in the assignment file to the dictionary self.myAssignmentDict
                self.myAssignmentDict = {}
                # Decide if the assignment file links to another one or contains the paths.
                if self.myPathToCsv != None:
                    try:
                        with open(self.myPathToCsv, 'r', encoding='utf-8-sig') as myFile:
                            csvReader = csv.reader(myFile, delimiter=';')
                            # Check if the assignment file contains the assignment to the user input
                            for row in csvReader:
                                self.myAssignmentDict[str(row[0]).strip()] = os.path.abspath(str(row[1]).strip())
                    except:
                        QMessageBox.critical(self, 'Zuordnungstabelle fehlerheft', 'Die Zuordnungstabelle ist fehlerhaft. \nWenden Sie sich an den Administrator.', QMessageBox.Ok)
                        pass
                else:
                    try:
                        with open(os.path.split(os.path.normpath(sys.argv[0]))[0] + os.sep + 'Assignment.csv', 'r', encoding='utf-8-sig') as myFile:
                            csvReader = csv.reader(myFile, delimiter=';')
                            # Check if the assignment file contains the assignment to the user input
                            for row in csvReader:
                                self.myAssignmentDict[str(row[0]).strip()] = os.path.abspath(str(row[1]).strip())
                    except:
                        QMessageBox.critical(self, 'Zuordnungstabelle fehlerheft', 'Die Zuordnungstabelle ist fehlerhaft. \nWenden Sie sich an den Administrator.', QMessageBox.Ok)
                        pass
                # Check if the assignment file contains the assignment to the user input
                if not (str(self.myLineEditScanPath.text()).strip() in self.myAssignmentDict):
                    self.myAssignmentDictMessage = QMessageBox.warning(self, 'Pfad scannen', 'Die Eingabe ist kein gültiger Pfad und\nwurde in der Zuordnungstabelle nicht gefunden.', QMessageBox.Ok)
                    self.show()
                # Validate if the file is a .csv file and start testing
                else:
                    if not self.myAssignmentDict[str(self.myLineEditScanPath.text()).strip()][self.myAssignmentDict[str(self.myLineEditScanPath.text()).strip()].rfind('.'):].lower() == '.csv':
                        self.myAssignmentDictMessage2 = QMessageBox.warning(self, 'Pfad scannen', 'Der Pfad in der Zuordnungstabelle\nist ungültig.', QMessageBox.Ok)
                        self.show()
                    else:
                        self.myParent.startTestingScanner2(os.path.abspath(self.myAssignmentDict[str(self.myLineEditScanPath.text()).strip()]))

# The dialog to scan the contract number
class MyDialogOpenTestInstructionScanner2(QDialog, Ui_myDialogContractNumberScanner):
    def __init__(self, myParent):
        super(MyDialogOpenTestInstructionScanner2, self).__init__()
        self.myParent = myParent

    def startUi(self):
        # Set up the ui from designer, minimum size
        self.setupUi(self)
        self.resize(0, 0)
        self.show()
        # Check which button the user presses
        self.myButtonBoxDialogContractNumberScanner.accepted.connect(self.ok)

    def ok(self):
        if (str(self.myLineEditScanContractNumber.text()) == '') or (str(self.myLineEditScanContractNumber.text()).isspace() == True):
            self.myContractNumberScanMessage = QMessageBox.warning(self, 'Auftragsnummer scannen', 'Bitte scannen Sie die Auftragsnummer ein.', QMessageBox.Ok)
            self.show()
        else:
            # The contract number must differ from the material number.
            self.materialNumberFromPath = os.path.abspath(self.myParent.myTestInstructionFile[0])[os.path.abspath(self.myParent.myTestInstructionFile[0]).rfind(os.sep) + 1:]
            if '_' in self.materialNumberFromPath:
                self.materialNumberFromPath = self.materialNumberFromPath[:self.materialNumberFromPath.find('_')]
            else:
                self.materialNumberFromPath = self.materialNumberFromPath[:self.materialNumberFromPath.find('.')]
            if (str(self.materialNumberFromPath) == str(self.myLineEditScanContractNumber.text().strip())):
                self.myContractNumberScanMessage2 = QMessageBox.warning(self, 'Auftragsnummer scannen', 'Die Auftragsnummer muss sich von\nder Materialnummer unterscheiden.', QMessageBox.Ok)
                self.show()
            else:
                # Start the next method in InStart
                self.myParent.startTestingScanner3(str(self.myLineEditScanContractNumber.text()).strip())

# The dialog to scan the staff number
class MyDialogOpenTestInstructionScanner3(QDialog, Ui_myDialogPersonnelNumberScanner):
    def __init__(self, myParent):
        super(MyDialogOpenTestInstructionScanner3, self).__init__()
        self.myParent = myParent

    def startUi(self):
        # Set up the ui from designer, minimum size
        self.setupUi(self)
        self.resize(0, 0)
        self.show()
        # Check which button the user presses
        self.myButtonBoxDialogPersonnelNumberScanner.accepted.connect(self.ok)

    def ok(self):
        if (str(self.myLineEditScanPersonnelNumber.text()) == '') or (str(self.myLineEditScanPersonnelNumber.text()).isspace() == True):
            self.myPersonnelNumberScanMessage = QMessageBox.warning(self, 'Name oder Personalnummer scannen', 'Bitte scannen Sie ihren Namen/\nihre Personal-Nr. ein.', QMessageBox.Ok)
            self.show()
        else:
            # Start the next method in InStart
            self.myParent.startTestingScanner4(str(self.myLineEditScanPersonnelNumber.text().strip()))