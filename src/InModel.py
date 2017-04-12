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

# OS for folder management
import os

# PyQt classes for the models
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox, QSpinBox, QLineEdit, QMessageBox

# pandas for csv handling
import pandas as pd

# decimal for correctly rounded float point arithmetic
from decimal import Decimal

# Own dialogs
from InDialog import MyDialogImportError

class MyCharacteristics():
    def __init__(self, parent, filePath):
        super(MyCharacteristics, self).__init__()
        self.parent = parent
        self.filePath = filePath
        # Import the csv
        self.importCsv()

    def importCsv(self):
        self.myColumnNames = ['ID', 'Arbeitsschritt', 'Merkmalsart', 'Häufigkeit', 'Stichprobe', 'Kurztext', 'Nennwert',
                              'Einheit', 'Offset', 'Absolut', 'Obere Toleranzgrenze', 'Untere Toleranzgrenze',
                              'Obere Eingriffsgrenze', 'Untere Eingriffsgrenze', 'Verweis', 'Messmittel',
                              'Beschreibung']
        try:
            # Import the csv. Every value is interpreted as a string. 'utf-8-sig' instead 'utf-8' to ignore the byte-order-mark before the fist value
            self.myData = pd.read_csv(os.path.abspath(self.filePath), sep=';', encoding='utf-8-sig', header=None, names=self.myColumnNames, keep_default_na=False, engine='c', dtype=str)
        except Exception as e:
            self.parent.myErrorMessage('Der Pfad und Dateiname darf keine Umlaute (ä, ö, ü) enthalten.')

        self.myData.columns = self.myColumnNames
        # Generate a list with the row numbers
        self.myRowNames = range(1, len(self.myData) + 1)

        #Check, if the values are valid. Store the problems in the myImportReport-List
        self.myImportReport = []
        self.myRowText = 'Zeile'
        self.myColumnText = 'Spalte'

        for myRow in range(0, len(self.myRowNames)):
            for myColumn in range(0, len(self.myColumnNames)):
                # iloc[row,column] access the specified value

                # ID is present, integer and unique
                if myColumn == 0:
                    if not ((self.myData.iloc[myRow, myColumn]).strip()).isdigit():
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine ID muss eine positive Ganzzahl ohne Vorzeichen sein.'))
                    for myRow2 in range(0, len(self.myRowNames)):
                        if (myRow < myRow2) and (self.myData.iloc[myRow, myColumn].strip() == self.myData.iloc[myRow2, myColumn].strip()):
                            self.myImportReport.append('{0!s} \'{1!s}\' {2!s} {3!s} {4!s} {5!s}. {6!s}'.format('ID', self.myData.iloc[myRow, myColumn], 'in Zeile', myRow + 1, 'entspricht der ID in Zeile', myRow2 + 1, 'Jede Zeile muss eine eindeutige ID haben.'))

                # Property is present, integer and match '1', '2', or '3'
                if myColumn == 2:
                    if (self.myData.iloc[myRow, myColumn].strip() != '0') and (self.myData.iloc[myRow, myColumn].strip() != '1') and (self.myData.iloc[myRow, myColumn].strip() != '2'):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Die Merkmalsart muss den Wert 0 für Informativ, 1 für Qualitativ oder 2 für Quantitativ haben.'))

                # Frequency is present, integer, > 0
                if myColumn == 3:
                    if not (((self.myData.iloc[myRow, myColumn]).strip()).isdigit()) or ((self.myData.iloc[myRow, myColumn]).strip() == '0'):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine Häufigkeit muss eine positive Ganzzahl ohne Vorzeichen sein.'))

                # Sample is present, integer
                if myColumn == 4:
                    if not (((self.myData.iloc[myRow, myColumn]).strip()).isdigit()) or ((self.myData.iloc[myRow, myColumn]).strip() == '0'):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine Stichprobe muss eine positive Ganzzahl ohne Vorzeichen sein.'))

                # Type is present and not whitespace
                if myColumn == 5:
                    if self.myData.iloc[myRow, myColumn].strip() == '':
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Ein Kurztext muss vorhanden sein.'))

                # Value must be present if property is 2. Valus must not be present if property is 0
                if myColumn == 6:
                    if (self.myData.iloc[myRow, 2].strip() == '0') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Ein Nennwert darf bei einem informativen Merkmal nicht vorhanden sein.'))
                    if self.myData.iloc[myRow, 2].strip() == '2':
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Ein Nennwert muss bei einem quantitativen Merkmal vorhanden und eine Fließkommazahl sein.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Ein Nennwert muss eine Fließkommazahl sein.'))

                # Unit must be present if property is 2. Unit must not be present if property is 0. Unit must be present if property is 1 and a value is given. Unit must not be present if property is 1 and no value is given.
                if myColumn == 7:
                    if (self.myData.iloc[myRow, 2].strip() == '0') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine Einheit darf bei einem informativen Merkmal nicht vorhanden sein.'))
                    if (self.myData.iloc[myRow, 2].strip() == '2') and (self.myData.iloc[myRow, myColumn].strip() == ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine Einheit muss bei einem qualitativen Merkmal vorhanden sein.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1'):
                        if (self.myData.iloc[myRow, 6].strip() != '') and (self.myData.iloc[myRow, myColumn].strip() == ''):
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine Einheit muss vorhanden sein, wenn ein Nennwert vorhanden ist.'))
                        if (self.myData.iloc[myRow, 6].strip() == '') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine Einheit darf nicht vorhanden sein, wenn kein Nennwert vorhanden ist.'))

                # Offset must not be present if property is 0 or 1. It mus be a floating point number, if it is present with property 2
                if myColumn == 8:
                    if (self.myData.iloc[myRow, 2].strip() == '0') or (self.myData.iloc[myRow, 2].strip() == '1'):
                        if self.myData.iloc[myRow, myColumn].strip() != '':
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Ein Offset darf bei einem informativen oder qualitativen Merkmal nicht vorhanden sein.'))
                    if (self.myData.iloc[myRow, 2].strip() == '2') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Ein Offset muss eine Fließkommazahl sein.'))

                # Absolut must be present. If property is 0 or 1, absolut must be False.
                if myColumn == 9:
                    if (self.myData.iloc[myRow, myColumn].strip() != '0') and (self.myData.iloc[myRow, myColumn].strip() != '1'):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Absolut muss 0 (Falsch) oder 1 (Wahr) sein.'))
                    if (self.myData.iloc[myRow, 2].strip() == '0') and (self.myData.iloc[myRow, myColumn].strip() == '1'):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Absolut muss 0 (Falsch) sein, bei einem informativen Merkmal.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, myColumn].strip() == '1'):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Absolut muss 0 (Falsch) sein, bei einem qualitativen Merkmal.'))

                # Upper Tolerance Level must not be present, if property is 0. It must be present and a floating point number, if property is 2.
                # It must be present, if property is 1 and there is a value. It must not be present, if property 1 1 and ther ise no value.
                if myColumn == 10:
                    if (self.myData.iloc[myRow, 2].strip() == '0') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Es darf keine Toleranz vorhanden sein, bei einem informativen Merkmal.'))
                    if (self.myData.iloc[myRow, 2].strip() == '2') and (self.myData.iloc[myRow, myColumn].strip() == ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Es muss eine obere Toleranzgrenze vorhanden sein, bei einem quantitativen Merkmal.'))
                    if (self.myData.iloc[myRow, 2] == '2') and (self.myData.iloc[myRow, myColumn] != ''):
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine obere Toleranzgrenze muss eine Fließkommazahl sein.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() == '') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine obere Toleranzgrenze darf bei einem qualitativen Merkmal nicht vorhanden sein, wenn kein Nennwert vorhanden ist.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() != '') and (self.myData.iloc[myRow, myColumn].strip() == ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine obere Toleranzgrenze muss bei einem qualitativen Merkmal vorhanden sein, wenn ein Nennwert vorhanden ist.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() != '') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine obere Toleranzgrenze muss eine Fließkommazahl sein.'))

                # Lower Tolerance Level must not be present, if property is 0. It must be present and a floating point number, if property is 2.
                # It must be present, if property is 1 and there is a value. It must not be present, if property 1 1 and ther ise no value.
                if myColumn == 11:
                    if (self.myData.iloc[myRow, 2].strip() == '0') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Es darf keine Toleranz vorhanden sein, bei einem informativen Merkmal.'))
                    if (self.myData.iloc[myRow, 2].strip() == '2') and (self.myData.iloc[myRow, myColumn].strip() == ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Es muss eine untere Toleranzgrenze vorhanden sein, bei einem quantitativen Merkmal.'))
                    if (self.myData.iloc[myRow, 2] == '2') and (self.myData.iloc[myRow, myColumn] != ''):
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine untere Toleranzgrenze muss eine Fließkommazahl sein.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() == '') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine untere Toleranzgrenze darf bei einem qualitativen Merkmal nicht vorhanden sein, wenn kein Nennwert vorhanden ist.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() != '') and (self.myData.iloc[myRow, myColumn].strip() == ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine untere Toleranzgrenze muss bei einem qualitativen Merkmal vorhanden sein, wenn ein Nennwert vorhanden ist.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() != '') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine untere Toleranzgrenze muss eine Fließkommazahl sein.'))
                    # If a upper and a lower tolerance level is present, the upper one must be higher than the lower one.
                    try:
                        if Decimal(((self.myData.iloc[myRow, 10]).strip()).replace(',', '.')) - Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.')) <= 0:
                            self.myImportReport.append('{0!s} {1!s}: {2!s}'.format(self.myRowText, myRow + 1, 'Die obere Toleranzgrenze muss höher sein, als die untere Toleranzgrenze.'))
                    except:
                        pass

                # Upper Intervention Threshold must not be present, if property is 0. It must be present and a floating point number, if property is 2.
                # It must be present, if property is 1 and there is a value. It must not be present, if property 1 1 and ther ise no value.
                if myColumn == 12:
                    if (self.myData.iloc[myRow, 2].strip() == '0') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Es darf keine Eingriffsgrenze vorhanden sein, bei einem informativen Merkmal.'))
                    if (self.myData.iloc[myRow, 2].strip() == '2') and (self.myData.iloc[myRow, myColumn].strip() == ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Es muss eine obere Eingriffsgrenze vorhanden sein, bei einem quantitativen Merkmal.'))
                    if (self.myData.iloc[myRow, 2].strip() == '2') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine obere Eingriffsgrenze muss eine Fließkommazahl sein.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() == '') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine obere Eingriffsgrenze darf bei einem qualitativen Merkmal nicht vorhanden sein, wenn kein Nennwert vorhanden ist.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() != '') and (self.myData.iloc[myRow, myColumn].strip() == ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine obere Eingriffsgrenze muss bei einem qualitativen Merkmal vorhanden sein, wenn ein Nennwert vorhanden ist.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() != '') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine obere Eingriffsgrenze muss eine Fließkommazahl sein.'))

                # Lower Intervention Threshold must not be present, if property is 0. It must be present and a floating point number, if property is 2.
                # It must be present, if property is 1 and there is a value. It must not be present, if property 1 1 and ther ise no value.
                if myColumn == 13:
                    if (self.myData.iloc[myRow, 2].strip() == '0') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Es darf keine Eingriffsgrenze vorhanden sein, bei einem informativen Merkmal.'))
                    if (self.myData.iloc[myRow, 2].strip() == '2') and (self.myData.iloc[myRow, myColumn].strip() == ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Es muss eine untere Eingriffsgrenze vorhanden sein, bei einem quantitativen Merkmal.'))
                    if (self.myData.iloc[myRow, 2].strip() == '2') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine untere Eingriffsgrenze muss eine Fließkommazahl sein.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() == '') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine untere Eingriffsgrenze darf bei einem qualitativen Merkmal nicht vorhanden sein, wenn kein Nennwert vorhanden ist.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() != '') and (self.myData.iloc[myRow, myColumn].strip() == ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine untere Eingriffsgrenze muss bei einem qualitativen Merkmal vorhanden sein, wenn ein Nennwert vorhanden ist.'))
                    if (self.myData.iloc[myRow, 2].strip() == '1') and (self.myData.iloc[myRow, 6].strip() != '') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        try:
                            Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.'))
                        except:
                            self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Eine untere Eingriffsgrenze muss eine Fließkommazahl sein.'))
                    # If a upper and a lower interference threshold is present, the upper one must be higher than the lower one.
                    try:
                        if Decimal(((self.myData.iloc[myRow, 12]).strip()).replace(',', '.')) - Decimal(((self.myData.iloc[myRow, myColumn]).strip()).replace(',', '.')) <= 0:
                            self.myImportReport.append('{0!s} {1!s}: {2!s}'.format(self.myRowText, myRow + 1, 'Die obere Eingriffsgrenze muss höher sein, als die untere Eingriffsgrenze.'))
                    except:
                        pass

                # Reference must not be present, if property is 0
                if myColumn == 14:
                    if (self.myData.iloc[myRow, 2].strip() == '0') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1, self.myColumnText, myColumn + 1, 'Ein Verweis darf nicht vorhanden sein, bei einem informativen Merkmal.'))

                # Equipment must not be present, if property is 0
                if myColumn == 15:
                    if (self.myData.iloc[myRow, 2].strip() == '0') and (self.myData.iloc[myRow, myColumn].strip() != ''):
                        self.myImportReport.append('\'{0!s}\' = {1!s} {2!s}, {3!s} {4!s}: {5!s}'.format(self.myData.iloc[myRow, myColumn], self.myRowText, myRow + 1,  self.myColumnText, myColumn + 1, 'Ein Messmittel darf nicht vorhanden sein, bei einem informativen Merkmal.'))

        # Error message, if import data is not valid
        if len(self.myImportReport) > 0:
            self.myDialogImportError = MyDialogImportError(self)
            self.result = self.myDialogImportError.startUi()

        else:
            # Create the table model, if there is no problem
            self.createTableModel()

    def createTableModel(self):
        self.parent.startTesting3(self.myData)


# The delegate for the type
class MyDelegateComoBox1(QStyledItemDelegate):
    def __init__(self):
        super(MyDelegateComoBox1, self).__init__()
        # set up the types an their description
        self.myComboItems=['0 - Informativ', '1 - Qualitativ','2 - Quantitativ']

    # set up the delegate for the model
    def createEditor(self, parent, option, proxyModelIndex):
        myComboBox = QComboBox(parent)
        myComboBox.addItems(self.myComboItems)
        return myComboBox

    # the code which runs, if a value of the delegate is selected
    def setModelData(self, combo, model, index):
        comboIndex = combo.currentIndex()
        value = self.myComboItems[comboIndex]
        model.setData(index, value[0:1])


# The delegate for the type
class MyDelegateComoBox2(QStyledItemDelegate):
    def __init__(self):
        super(MyDelegateComoBox2, self).__init__()
        # set up the types an their description
        self.myComboItems=['0 - Nein', '1 - Ja']

    # set up the delegate for the model
    def createEditor(self, parent, option, proxyModelIndex):
        myComboBox = QComboBox(parent)
        myComboBox.addItems(self.myComboItems)
        return myComboBox

    # the code which runs, if a value of the delegate is selected
    def setModelData(self, combo, model, index):
        comboIndex = combo.currentIndex()
        value = self.myComboItems[comboIndex]
        model.setData(index, value[0:1])


# The delegate for the ID, Frequency, Sample
class MyDelegateSpinBox1(QStyledItemDelegate):
    def __init__(self):
        super(MyDelegateSpinBox1, self).__init__()

    # set up the delegate
    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        myEditor = QSpinBox(QWidget)
        myEditor.setMinimum(1)
        myEditor.setMaximum(999999)
        return myEditor

    # The selected spin box shows the existing value
    def setEditorData(self, QWidget, QModelIndex):
        # Type casting. The item is str. The spin box works with int.
        try:
            myValue = int(QModelIndex.data())
        except:
            myValue = 1
        QWidget.setValue(myValue)

    # This code runs if the user confirms a new value
    def setModelData(self, QWidget, QAbstractItemModel, QModelIndex):
        myValue = QWidget.value()
        QAbstractItemModel.setData(QModelIndex, myValue)


# The delegate for for floating point numbers
class MyDelegateLineEdit1(QStyledItemDelegate):
    def __init__(self, parent):
        super(MyDelegateLineEdit1, self).__init__()
        self.myParent = parent

    # set up the delegate
    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        myEditor = QLineEdit(QWidget)
        return myEditor

    # The selected line edit shows the existing value
    def setEditorData(self, QWidget, QModelIndex):
        QWidget.setText(QModelIndex.data())

    # This code runs if the user confirms a new value
    def setModelData(self, QWidget, QAbstractItemModel, QModelIndex):
        # The value has to be convertable to Decimal or empty
        if QWidget.text().strip() != '':
            try:
                myValue = Decimal(QWidget.text().strip().replace(',', '.'))
            except:
                QMessageBox.warning(self.myParent.myEditForm, 'Fehlerhafte Eingabe', 'Geben Sie eine Dezimalzahl ein')
                myValue = ''
        else:
            myValue = ''
        QAbstractItemModel.setData(QModelIndex, myValue)


# The Table Model of all characteristics (pandas dataframe based)
class MyCharacteristicsTableModel(QAbstractTableModel):
    def __init__(self, data):
        super(MyCharacteristicsTableModel, self).__init__()
        # myData is a pandas dataframe
        self.myData = data

    # The number of rows of the table
    def rowCount(self, parent):
        return len(self.myData)

    # The number of columns of the table
    def columnCount(self, parent):
        return len(self.myData.columns)

    def data(self, QModelIndex, role=Qt.DisplayRole):

        # Correct error handling = retun an empty QVariant
        if not (QModelIndex.isValid()) or not (0 <= QModelIndex.row() < len(range(1, len(self.myData) + 1))):
            return QVariant()

        # Return the data, to show in the table or if the user double clicks on a value to edit it
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # The current selected row number
            self.myTableRow = int(QModelIndex.row())
            # The current selected column number
            self.myTableColumn = int(QModelIndex.column())
            return QVariant(str(self.myData.iloc[self.myTableRow][self.myTableColumn]))

        # Set the text alignment of the values in the table
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))

        # Set the color of the values in the table
        elif (role == Qt.ForegroundRole) and (QModelIndex.column() == 5):
            return QVariant(QBrush(Qt.black))

        # Change the font of the values in the table
        elif role == Qt.FontRole:
            # Create a QFont instance
            myFont = QFont()
            # Set the font size to 12
            myFont.setPointSize(12)

            if QModelIndex.column() == 5:
                # Set the 5th column to bold
                myFont.setBold(True)
            return QVariant(myFont)


    # The header data of the table
    def headerData(self, p_int, Qt_Orientation, role=Qt.DisplayRole):

        # Return the horizontal header data
        if (Qt_Orientation == Qt.Horizontal) and (role == Qt.DisplayRole):
            return QVariant(self.myData.columns[p_int])

        # Return the vertical header data
        elif (Qt_Orientation == Qt.Vertical) and (role == Qt.DisplayRole):
            return QVariant(range(1, len(self.myData) + 1)[p_int])

        # Set the text alignment of the header
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))

        # Change the font of the header
        elif role == Qt.FontRole:
            myFont = QFont()
            myFont.setPointSize(12)
            myFont.setBold(True)
            return QVariant(myFont)
        else:
            return QVariant()

    # If the user edits a value and press enter
    def setData(self, QModelIndex, value, role=Qt.EditRole):
        self.myEditRow = int(QModelIndex.row())
        self.myEditColumn = int(QModelIndex.column())
        self.myEditColumnName = self.myData.columns.values[self.myEditColumn]
        self.myData.set_value(self.myEditRow, self.myEditColumnName, value)
        return True

    # Set the flags, so the model data is editable
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    # Insert a new row underneath the current selected row
    def insertRows(self, position, rows=1, parent=QModelIndex()):
        # beginInsertRows marks the beginning of the insert and where the row is added
        self.beginInsertRows(parent, position+1, position+rows)
        # Create an new DataFrame with one empty line
        newLine = pd.DataFrame({self.myData.columns[0]:'', self.myData.columns[1]:'', self.myData.columns[2]:'', self.myData.columns[3]:'', self.myData.columns[4]:'', self.myData.columns[5]:'', self.myData.columns[6]:'', self.myData.columns[7]:'', self.myData.columns[8]:'', self.myData.columns[9]:'', self.myData.columns[10]:'', self.myData.columns[11]:'', self.myData.columns[12]:'', self.myData.columns[13]:'', self.myData.columns[14]:'', self.myData.columns[15]:'', self.myData.columns[16]:''}, index=[position+1])
        # Name the columns like myData to avoid resorting of the columns
        newLine.columns = self.myData.columns
        # Concatenate the dataframes and reset the index, so there are no duplicate values. This would cause value chains.
        self.myData = pd.concat([self.myData.ix[:position], newLine, self.myData.ix[position+1:]]).reset_index(drop=True)
        # endInsertRows marks the end of the insert
        self.endInsertRows()
        # Return True, or the application crashes
        return True

    # Delete the current selected row
    def removeRows(self, position, row=1, parent=QModelIndex()):
        if len(self.myData) > 1:
            # beginRemoveRows marks the row, to delete
            if position == 0:
                # Row 0 causes an error, if you do not handle it this was
                self.beginRemoveRows(parent, 1, 1)
            else:
                self.beginRemoveRows(parent, position, position)
            # Delete the selected Row
            self.myData = self.myData.drop(self.myData.index[position]).reset_index(drop=True)
            self.endRemoveRows()
            return True
        else:
            return False

    # Move the rows up and down
    def moveRows(self, oldRow, newRow, parent=QModelIndex()):
        # Move the rows upwards
        if newRow < oldRow:
            self.beginMoveRows(parent, oldRow, oldRow, parent, newRow)
            # 1) Save the line you like to move
            self.moveLine = self.myData.ix[oldRow:oldRow].reset_index(drop=True)
            self.moveLine.columns = self.myData.columns
            # 2) Delete the line from the dataframe
            self.myData = self.myData.drop(self.myData.index[oldRow]).reset_index(drop=True)
            # 3) Concatenate the dataframe with the moved line
            # To move the line upwards
            self.myData = pd.concat([self.myData.ix[:newRow - 1], self.moveLine, self.myData.ix[newRow:]]).reset_index(drop=True)
            self.endMoveRows()
        # Move the row downwards
        else:
            self.beginMoveRows(parent, oldRow, oldRow, parent, newRow + 1)
            # 1) Save the line you like to move
            self.moveLine = self.myData.ix[oldRow:oldRow].reset_index(drop=True)
            self.moveLine.columns = self.myData.columns
            # 2) Delete the line from the dataframe
            self.myData = self.myData.drop(self.myData.index[oldRow]).reset_index(drop=True)
            # 3) Concatenate the dataframe with the moved line
            # To move the line upwards
            self.myData = pd.concat([self.myData.ix[:oldRow], self.moveLine, self.myData.ix[oldRow + 1:]]).reset_index(drop=True)
            self.endMoveRows()
        return True



class MyCharacteristicsAdjustView():
    def __init__(self, parent, row):
        super(MyCharacteristicsAdjustView, self).__init__()
        self.myParent = parent
        self.myCurrentRow = row

        # Set the labels according to the current characteristic
        self.myParent.myLabelType.setText('{0!s}'.format(self.myParent.myData.iloc[self.myCurrentRow, 5]))
        # Only show the brackets, if something is inside
        if self.myParent.myData.iloc[self.myCurrentRow, 14].strip() == '':
            self.myParent.myLabelReference.setText('{0!s}'.format(''))
        else:
            self.myParent.myLabelReference.setText('({0!s})'.format(self.myParent.myData.iloc[self.myCurrentRow, 14].strip()))
        self.myParent.myLabelEquipment.setText('{0!s}'.format(self.myParent.myData.iloc[self.myCurrentRow, 15].strip()))
        self.myParent.myLabelValue.setText('{0!s} {1!s}'.format(self.myParent.myData.iloc[self.myCurrentRow, 6].strip(), self.myParent.myData.iloc[self.myCurrentRow, 7].strip()))
        if (self.myParent.myData.iloc[self.myCurrentRow, 10].strip() == '') and (self.myParent.myData.iloc[self.myCurrentRow, 11].strip() == ''):
            self.myParent.myLabelTolerance.setText('')
        else:
            self.myParent.myLabelTolerance.setText('{0!s}: ({1!s} {2!s} {3!s})'.format('Toleranz', self.myParent.myData.iloc[self.myCurrentRow, 11].strip(), 'bis', self.myParent.myData.iloc[self.myCurrentRow, 10].strip()))
        if (self.myParent.myData.iloc[self.myCurrentRow, 12].strip() == '') and (self.myParent.myData.iloc[self.myCurrentRow, 13].strip() == ''):
            self.myParent.myLabelInterference.setText('')
        else:
            self.myParent.myLabelInterference.setText('{0!s}: ({1!s} {2!s} {3!s})'.format('Eingriffsgrenze', self.myParent.myData.iloc[self.myCurrentRow, 13].strip(), 'bis', self.myParent.myData.iloc[self.myCurrentRow, 12].strip()))

        # The description text of quantitative characteristics
        if int(self.myParent.myData.iloc[self.myCurrentRow, 2].strip()) == 2:
            # ID and step. Only show the brackets, if a step is inside
            if self.myParent.myData.iloc[self.myCurrentRow, 1].strip() == '':
                self.myDescriptionText0 = '{0!s}-{1!s} {2!s}:'.format('Merkmal', self.myParent.myData.columns[0], self.myParent.myData.iloc[self.myCurrentRow, 0].strip())
            else:
                self.myDescriptionText0 = '{0!s}-{1!s} {2!s} ({3!s}):'.format('Merkmal', self.myParent.myData.columns[0], self.myParent.myData.iloc[self.myCurrentRow, 0].strip(), self.myParent.myData.iloc[self.myCurrentRow, 1].strip())
            # Consider singular and plural
            if (int(self.myParent.myData.iloc[self.myCurrentRow, 3].strip()) == 1) and (int(self.myParent.myData.iloc[self.myCurrentRow, 4].strip()) == 1):
                self.myDescriptionText1 = '\'{0!s}\' {1!s}.'.format(self.myParent.myData.iloc[self.myCurrentRow, 5].strip(), 'bei jedem Programmdurchlauf, bei einem Teil messen')
            elif (int(self.myParent.myData.iloc[self.myCurrentRow, 3].strip()) == 1) and (int(self.myParent.myData.iloc[self.myCurrentRow, 4].strip()) > 1):
                self.myDescriptionText1 = '\'{0!s}\' {1!s} {2!s} {3!s}.'.format(self.myParent.myData.iloc[self.myCurrentRow, 5].strip(), 'bei jedem Programmdurchlauf, bei', self.myParent.myData.iloc[self.myCurrentRow, 4].strip(), 'Teilen messen')
            elif (int(self.myParent.myData.iloc[self.myCurrentRow, 3].strip()) > 1) and (int(self.myParent.myData.iloc[self.myCurrentRow, 4].strip()) == 1):
                self.myDescriptionText1 = '\'{0!s}\' {1!s} {2!s}. {3!s}.'.format(self.myParent.myData.iloc[self.myCurrentRow, 5].strip(), 'bei jedem', self.myParent.myData.iloc[self.myCurrentRow, 3].strip(), 'Programmdurchlauf, bei einem Teil messen')
            else:
                self.myDescriptionText1 = '\'{0!s}\' {1!s} {2!s}. {3!s} {4!s} {5!s}.'.format(self.myParent.myData.iloc[self.myCurrentRow, 5].strip(), 'bei jedem', self.myParent.myData.iloc[self.myCurrentRow, 3].strip(), 'Programmdurchlauf, bei', self.myParent.myData.iloc[self.myCurrentRow, 4].strip(), 'Teilen messen')
            # Only show the offset text, if there is a offset
            if self.myParent.myData.iloc[self.myCurrentRow, 8].strip() != '':
                self.myDescriptionText2 = '{0!s}. {1!s} {2!s} {3!s}.'.format('Der eingegebene Wert wird automatisch um das Offset korrigiert', 'Dieses beträgt', self.myParent.myData.iloc[self.myCurrentRow, 8].strip().replace(',', '.'), self.myParent.myData.iloc[self.myCurrentRow, 7].strip())
            else:
                self.myDescriptionText2 = ''
            # Only show the absolut text, if absolut is true
            if bool(int(self.myParent.myData.iloc[self.myCurrentRow, 9].strip())):
                self.myDescriptionText3 = '{0!s}'.format('Der eingegebene Wert wird als Absolutwert interpretiert. Also immer als positiver Wert, unabhängig vom Vorzeichen.')
            else:
                self.myDescriptionText3 = ''
            self.myParent.myTextBrowserDescription.setPlainText('{0!s}\n\n{1!s} {2!s} {3!s}\n\n{4!s}'.format(self.myDescriptionText0, self.myDescriptionText1, self.myDescriptionText2, self.myDescriptionText3, self.myParent.myData.iloc[self.myCurrentRow, 16].strip()))

        # The description text of qualitative characteristics
        if int(self.myParent.myData.iloc[self.myCurrentRow, 2].strip()) == 1:
            # ID and step. Only show the brackets, if a step is inside
            if self.myParent.myData.iloc[self.myCurrentRow, 1].strip() == '':
                self.myDescriptionText0 = '{0!s}-{1!s} {2!s}:'.format('Merkmal', self.myParent.myData.columns[0], self.myParent.myData.iloc[self.myCurrentRow, 0].strip())
            else:
                self.myDescriptionText0 = '{0!s}-{1!s} {2!s} ({3!s}):'.format('Merkmal', self.myParent.myData.columns[0], self.myParent.myData.iloc[self.myCurrentRow, 0].strip(), self.myParent.myData.iloc[self.myCurrentRow, 1].strip())
            # Consider singular and plural
            if (int(self.myParent.myData.iloc[self.myCurrentRow, 3].strip()) == 1) and (int(self.myParent.myData.iloc[self.myCurrentRow, 4].strip()) == 1):
                self.myDescriptionText1 = '\'{0!s}\' {1!s}.'.format(self.myParent.myData.iloc[self.myCurrentRow, 5].strip(), 'bei jedem Programmdurchlauf, bei einem Teil prüfen')
            elif (int(self.myParent.myData.iloc[self.myCurrentRow, 3].strip()) == 1) and (int(self.myParent.myData.iloc[self.myCurrentRow, 4].strip()) > 1):
                self.myDescriptionText1 = '\'{0!s}\' {1!s} {2!s} {3!s}.'.format(self.myParent.myData.iloc[self.myCurrentRow, 5].strip(), 'bei jedem Programmdurchlauf, bei', self.myParent.myData.iloc[self.myCurrentRow, 4].strip(), 'Teilen prüfen')
            elif (int(self.myParent.myData.iloc[self.myCurrentRow, 3].strip()) > 1) and (int(self.myParent.myData.iloc[self.myCurrentRow, 4].strip()) == 1):
                self.myDescriptionText1 = '\'{0!s}\' {1!s} {2!s}. {3!s}.'.format(self.myParent.myData.iloc[self.myCurrentRow, 5].strip(), 'bei jedem', self.myParent.myData.iloc[self.myCurrentRow, 3].strip(), 'Programmdurchlauf, bei einem Teil prüfen')
            else:
                self.myDescriptionText1 = '\'{0!s}\' {1!s} {2!s}. {3!s} {4!s} {5!s}.'.format(self.myParent.myData.iloc[self.myCurrentRow, 5].strip(), 'bei jedem', self.myParent.myData.iloc[self.myCurrentRow, 3].strip(), 'Programmdurchlauf, bei', self.myParent.myData.iloc[self.myCurrentRow, 4].strip(), 'Teilen prüfen')
            self.myParent.myTextBrowserDescription.setPlainText('{0!s}\n\n{1!s}\n\n{2!s}'.format(self.myDescriptionText0, self.myDescriptionText1, self.myParent.myData.iloc[self.myCurrentRow, 16].strip()))

        # The description text of informative characteristics
        if int(self.myParent.myData.iloc[self.myCurrentRow, 2].strip()) == 0:
            # ID and step. Only show the brackets, if a step is inside
            if self.myParent.myData.iloc[self.myCurrentRow, 1].strip() == '':
                self.myDescriptionText0 = '{0!s}-{1!s} {2!s}:'.format('Merkmal', self.myParent.myData.columns[0], self.myParent.myData.iloc[self.myCurrentRow, 0].strip())
            else:
                self.myDescriptionText0 = '{0!s}-{1!s} {2!s} ({3!s}):'.format('Merkmal', self.myParent.myData.columns[0], self.myParent.myData.iloc[self.myCurrentRow, 0].strip(), self.myParent.myData.iloc[self.myCurrentRow, 1].strip())
            self.myParent.myTextBrowserDescription.setPlainText('{0!s}\n\n{1!s}'.format(self.myDescriptionText0, self.myParent.myData.iloc[self.myCurrentRow, 16].strip()))


    def setImageAmount(self):
        self.mySupportedImageFormats = ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'pbm', 'pgm', 'ppm', 'xbm', 'xpm']

        #Check if a folder with the same name as the file exists. If not, create it.
        self.mySeperatedPath = os.path.split(os.path.normpath(self.myParent.myTestInstructionFile[0]))
        if not os.path.exists(os.path.join(self.mySeperatedPath[0] + os.sep + self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')] + os.sep + 'Images')):
            os.makedirs(os.path.join(self.mySeperatedPath[0] + os.sep + self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')] + os.sep + 'Images'))

        # Catch the images, which start with the ID of the current selected attribute, followed by a '_'
        self.myFiles = os.listdir(os.path.join(self.mySeperatedPath[0] + os.sep + self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')] + os.sep + 'Images'))
        self.myImageFiles = []
        for myFile in self.myFiles:
            if (myFile.split('.')[-1] in self.mySupportedImageFormats) and (myFile.startswith(self.myParent.myData.iloc[self.myCurrentRow, 0].strip() + '_')):
                self.myImageFiles.append(os.path.join(self.mySeperatedPath[0] + os.sep + self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')] + os.sep + 'Images' + os.sep + myFile))
        self.myImageFiles.sort()
        return self.myImageFiles

    def setVideoAmount(self):
        self.mySupportedVideoFormats =['asf', 'wmv', 'dvr-ms', 'avi', 'mpg', 'mpeg', 'm1v', 'mov', 'mp4', 'm4v', 'mp4v', '3g2', '3gp2', '3gp', 'm2ts', 'flv', 'ogm', 'ogg', 'mkv', 'mka', 'ts', 'nsc', 'nsv']

        #Check if a folder with the same name as the file exists. If not, create it.
        self.mySeperatedPath2 = os.path.split(os.path.normpath(self.myParent.myTestInstructionFile[0]))
        if not os.path.exists(os.path.join(self.mySeperatedPath2[0] + os.sep + self.mySeperatedPath2[1][:self.mySeperatedPath2[1].rfind('.')] + os.sep + 'Videos')):
            os.makedirs(os.path.join(self.mySeperatedPath2[0] + os.sep + self.mySeperatedPath2[1][:self.mySeperatedPath2[1].rfind('.')] + os.sep + 'Videos'))

        # Catch the videos, which start with the ID of the current selected attribute, followed by a '_'
        self.myFiles2 = os.listdir(os.path.join(self.mySeperatedPath2[0] + os.sep + self.mySeperatedPath2[1][:self.mySeperatedPath2[1].rfind('.')] + os.sep + 'Videos'))
        self.myVideoFiles = []
        for myFile2 in self.myFiles2:
            if (myFile2.split('.')[-1] in self.mySupportedVideoFormats) and (myFile2.startswith(self.myParent.myData.iloc[self.myCurrentRow, 0].strip() + '_')):
                self.myVideoFiles.append(os.path.join(self.mySeperatedPath2[0] + os.sep + self.mySeperatedPath2[1][:self.mySeperatedPath2[1].rfind('.')] + os.sep + 'Videos' + os.sep + myFile2))
        self.myVideoFiles.sort()
        return self.myVideoFiles

# The result table model
class MyResultTableModel(QAbstractTableModel):
    def __init__(self, resultData):
        super(MyResultTableModel, self).__init__()
        self.myResultData = resultData
        # Generate a list with the row numbers
        self.myRowNames = range(1, len(self.myResultData) + 1)

    # The number of rows of the table
    def rowCount(self, parent):
        return len(self.myResultData)

    # The number of columns of the table
    def columnCount(self, parent):
        return len(self.myResultData.columns)

    # The data of the table
    def data(self, QModelIndex, role=Qt.DisplayRole):

        # Correct error handling = retun an empty QVariant
        if not (QModelIndex.isValid()) or not (0 <= QModelIndex.row() < len(self.myRowNames)):
            return QVariant()

        # Return the data, to show in the table.
        if role == Qt.DisplayRole:
            # The current selected row number
            self.myTableRow = int(QModelIndex.row())
            # The current selected column number
            self.myTableColumn = int(QModelIndex.column())
            return QVariant(str(self.myResultData.iloc[self.myTableRow][self.myTableColumn]))

        # Set the text alignment of the values in the table
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))

        # Set the color of the values in the table
        elif (role == Qt.ForegroundRole) and (QModelIndex.column() == 6):
            self.inTolerance = self.toleranceCheck()
            # If the tolerance check return false, the tolerance is not met.
            if self.inTolerance:
                return QVariant(QBrush(Qt.black))
            # Color the result red, if it is out of the tolerance levels.
            else:
                return QVariant(QBrush(Qt.red))

        # Change the font of the values in the table
        elif role == Qt.FontRole:
            # Create a QFont instance
            myFont = QFont()
            # Set the font size to 12
            myFont.setPointSize(12)
            if QModelIndex.column() == 6:
                # Set the 6th column to bold
                myFont.setBold(True)
            return QVariant(myFont)

    # The header data of the table
    def headerData(self, p_int, Qt_Orientation, role=Qt.DisplayRole):

        # Return the horizontal header data
        if (Qt_Orientation == Qt.Horizontal) and (role == Qt.DisplayRole):
            return QVariant(self.myResultData.columns[p_int])

        # Return the vertical header data
        elif (Qt_Orientation == Qt.Vertical) and (role == Qt.DisplayRole):
            return QVariant(self.myRowNames[p_int])

        # Set the text alignment of the header
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))

        # Change the font of the header
        elif role == Qt.FontRole:
            myFont = QFont()
            myFont.setPointSize(12)
            myFont.setBold(True)
            return QVariant(myFont)
        else:
            return QVariant()

    # Check the tolerance. Return True, if the value is within the tolerance levels
    def toleranceCheck(self):
        try:
            # If the attribute is quantitative, this code will work
            self.value = Decimal(self.myResultData.iloc[self.myTableRow][6])
            self.utl = Decimal(self.myResultData.iloc[self.myTableRow][4])
            self.ltl = Decimal(self.myResultData.iloc[self.myTableRow][5])
            if (self.value > self.utl) or (self.value < self.ltl):
                return False
            else:
                return True
        except:
            # If the attribute is qualitative, this code wirll work
            if str(self.myResultData.iloc[self.myTableRow][6]) == 'n.i.O.':
                return False
            else:
                return True
