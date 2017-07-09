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

# for the csv file
import csv


# Class for handling the control csv file
class MyControl():
    def __init__(self, parent):
        super(MyControl, self).__init__()
        self.myParent = parent
        self.importCsv()

    # Import the control data
    def importCsv(self):
        # Check if a control data folder and file exists. If not, create it.
        self.mySeperatedPath = os.path.split(os.path.normpath(self.myParent.myTestInstructionFile[0]))
        if not os.path.exists(os.path.join(self.mySeperatedPath[0] + os.sep + self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')] + os.sep + 'Control')):
            os.makedirs(os.path.join(self.mySeperatedPath[0] + os.sep + self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')] + os.sep + 'Control'))
        # Check if a control data according to the contract exists. If not, create it.
        self.myColumnNames = ['ID', 'Frequency']
        self.myControlDataPath = os.path.join(self.mySeperatedPath[0] + os.sep + self.mySeperatedPath[1][:self.mySeperatedPath[1].rfind('.')] + os.sep + 'Control' + os.sep + self.myParent.myContractNumber + '.csv')
        # If the file already exists
        try:
            self.myControlData = pd.read_csv(os.path.abspath(self.myControlDataPath), sep=';', encoding='utf-8-sig', header=None, names=self.myColumnNames, keep_default_na=False, engine='c', dtype='int64')
            # Update the control date in case there are new or no longer id in the test instruction
            self.controlFrequencyDict = {}
            self.newFrequencyList = []
            for controlFrequency in range(0, len(self.myControlData.index)):
                self.controlFrequencyDict[self.myControlData.iloc[controlFrequency, 0]] = self.myControlData.iloc[controlFrequency, 1]
            for dataFrequency in range(0, len(self.myParent.myData.index)):
                try:
                    self.newFrequencyList.append([int(self.myParent.myData.iloc[dataFrequency, 0].strip()), self.controlFrequencyDict[int(self.myParent.myData.iloc[dataFrequency, 0].strip())]])
                except:
                    self.newFrequencyList.append([int(self.myParent.myData.iloc[dataFrequency, 0].strip()), 0])
            self.myControlDataNew = pd.DataFrame(data=self.newFrequencyList, columns=self.myColumnNames, dtype='int64')
            # If myControlDataNew is not equal to myControlData, save myControlDataNew as new default
            if not self.myControlData.equals(self.myControlDataNew):
                try:
                    self.myControlDataNew.to_csv(path_or_buf=os.path.abspath(self.myControlDataPath), sep=';', encoding='utf-8-sig', mode='w', index=False, header=False)
                    self.myControlData = self.myControlDataNew
                    self.myControlDataNew = None
                except Exception as e:
                    self.myParent.myErrorMessage(str(e))
        # If the file not exists. Create it with default value 0
        except Exception as e:
            # Create the new control csv
            try:
                with open(os.path.abspath(self.myControlDataPath), 'w', newline='', encoding='utf-8-sig') as myFile:
                    myCsvWriter = csv.writer(myFile, delimiter=';')
                    for line in range(0, len(self.myParent.myData)):
                        myCsvWriter.writerow([str(self.myParent.myData.iloc[line, 0]), 0])
            except Exception as e:
                self.myParent.myErrorMessage(str(e))
            # load the new created csv by running importCsv again
            self.importCsv()

    # Retun the Frequency of the current row
    def returnFrequency(self, id):
        self.currentId = id
        return self.myControlData.iloc[self.currentId, 1]

    # Save the new Frequency of the current row in the data field
    def saveFrequency(self, newFrequency):
        self.newFrequency = newFrequency
        self.myControlData.iloc[self.currentId][1] = self.newFrequency

    # Safe the data field in the csv on the HD
    def safeCsv(self):
        try:
            self.myControlData.to_csv(path_or_buf=os.path.abspath(self.myControlDataPath), sep=';', encoding='utf-8-sig', mode='w', index=False, header=False)
        except Exception as e:
            self.myParent.myErrorMessage(str(e))