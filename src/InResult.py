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

# pandas for csv handling
import pandas as pd


# Class for handling the result csv file
class MyResult():
    def __init__(self, parent):
        super(MyResult, self).__init__()
        self.myParent = parent
        self.importCsv()

    def importCsv(self):
        # Check if the result data folder and file exist. If not, create it
        self.mySeperatedPath = os.path.split(os.path.normpath(self.myParent.myTestInstructionFile[0]))
        if not os.path.exists(os.path.join(self.mySeperatedPath[0] + os.sep + self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')] + os.sep + 'Result')):
            os.makedirs(os.path.join(self.mySeperatedPath[0] + os.sep + self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')] + os.sep + 'Result'))
        # Use the full test instruction name if no _ is there. Else use the name until the _
        if self.mySeperatedPath[1].find('_') == -1:
            self.firstInstructionName = self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')]
        else:
            self.firstInstructionName = self.mySeperatedPath[1][:self.mySeperatedPath[1].find('_')]
        # Check if a result data according to the contract exists. If not, create it.
        self.myColumnNames = ['ID', 'Kurztext', 'Nennwert', 'Einheit', 'Obere Toleranzgrenze', 'Untere Toleranzgrenze', 'Messergebnis', 'Serien-Nr', 'Datum', 'Uhrzeit', 'Personal-Nr', 'Bemerkung']
        self.myResultDataPath = os.path.join(self.mySeperatedPath[0] + os.sep + self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')] + os.sep + 'Result' + os.sep + self.firstInstructionName + '_' + self.myParent.myContractNumber + '.csv')
        try:
            self.myResultData = pd.read_csv(os.path.abspath(self.myResultDataPath), sep=';', encoding='utf-8-sig', header=0, names=self.myColumnNames, keep_default_na=False, engine='c', dtype='str')
        except:
            self.myResultData = pd.DataFrame(data=None, index=None, columns=self.myColumnNames, dtype='str')
            try:
                self.myResultData.to_csv(path_or_buf=os.path.abspath(self.myResultDataPath), sep=';', encoding='utf-8-sig', mode='w', index=False, header=True)
            except Exception as e:
                self.myParent.myErrorMessage(str(e))

    # Append the result data csv with the result of the current measurement
    def saveResult(self, id, value, serial, myDate, myTime, personnel, comment):
        # The new line to save the data
        self.rowAmountResult = len(self.myResultData.index) + 1
        # Append the data with the new line
        self.myResultData.loc[self.rowAmountResult] = [str(id), str(self.myParent.myData.iloc[self.myParent.currentRow, 5].strip()), str((self.myParent.myData.iloc[self.myParent.currentRow, 6].strip()).replace(',', '.')), str(self.myParent.myData.iloc[self.myParent.currentRow, 7].strip()), str((self.myParent.myData.iloc[self.myParent.currentRow, 10].strip()).replace(',', '.')), str((self.myParent.myData.iloc[self.myParent.currentRow, 11].strip()).replace(',', '.')), str(value), str(serial), str(myDate), str(myTime), str(personnel), str(comment)]
        # Save the date on the hd
        try:
            self.myResultData.to_csv(path_or_buf=os.path.abspath(self.myResultDataPath), sep=';', encoding='utf-8-sig', mode='w', index=False, header=True)
        except Exception as e:
            self.myParent.myErrorMessage(str(e))

    # Return the whole available result data
    def returnResult(self):
        return self.myResultData