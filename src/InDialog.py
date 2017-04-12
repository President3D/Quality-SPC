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

# PyQt Classes for the UI
from PyQt5.QtWidgets import QDialog, QMessageBox, QWidget

# Own UIs
from Ui.InDialogOpenTestInstruction import Ui_myDialogOpenTestInstruction
from Ui.InDialogImportError import Ui_myDialogImportError
from Ui.InDialogToleranceExceeded import Ui_myDialogToleranceExceeded


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
            self.myParent.startTesting2(str(self.myLineEditContractNumber.text()), str(self.myLineEditStaffNumber.text()))


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