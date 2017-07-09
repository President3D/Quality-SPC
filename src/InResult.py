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

# json for the json log file
import json


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

    # Append the result data csv with the result of the current measurement and add the result to the log folder
    def saveResult(self, id, value, serial, myDate, myTime, personnel, comment):
        # The new line to save the data
        self.rowAmountResult = len(self.myResultData.index) + 1
        # Append the data with the new line
        self.myResultData.loc[self.rowAmountResult] = [str(id), str(self.myParent.myData.iloc[self.myParent.currentRow, 5].strip()), str((self.myParent.myData.iloc[self.myParent.currentRow, 6].strip()).replace(',', '.')), str(self.myParent.myData.iloc[self.myParent.currentRow, 7].strip()), str((self.myParent.myData.iloc[self.myParent.currentRow, 10].strip()).replace(',', '.')), str((self.myParent.myData.iloc[self.myParent.currentRow, 11].strip()).replace(',', '.')), str(value), str(serial), str(myDate), str(myTime), str(personnel), str(comment)]
        # Save the data in the result file
        try:
            self.myResultData.to_csv(path_or_buf=os.path.abspath(self.myResultDataPath), sep=';', encoding='utf-8-sig', mode='w', index=False, header=True)
        except Exception as e:
            self.myParent.myErrorMessage(str(e))
        # Call the function for the log file
        try:
            self.saveResultLog(id, value, serial, myDate, myTime, comment)
        except Exception as e:
            self.myParent.myErrorMessage(str(e))

    # Add the result to to dict for the json file in the log folder
    def saveResultLog(self, id, value, serial, myDate, myTime, comment):
        # Format the id to int to fit for json
        self.myId = int(id)
        # Format the description to fit for json
        if str(self.myParent.myData.iloc[self.myParent.currentRow, 5].strip()) != '':
            self.myDescription = str(self.myParent.myData.iloc[self.myParent.currentRow, 5].strip())
        else:
            self.myDescription = None
        # Format the nominal value to fit for json
        if str((self.myParent.myData.iloc[self.myParent.currentRow, 6].strip()).replace(',', '.')) != '':
            self.myNominalValue = float((self.myParent.myData.iloc[self.myParent.currentRow, 6].strip()).replace(',', '.'))
        else:
            self.myNominalValue = None
        # Format the unit to fit for json
        if str(self.myParent.myData.iloc[self.myParent.currentRow, 7].strip()) != '':
            self.myUnit = str(self.myParent.myData.iloc[self.myParent.currentRow, 7].strip())
        else:
            self.myUnit = None
        # Format the upper and lower tolerance to fit for json
        if (str((self.myParent.myData.iloc[self.myParent.currentRow, 10].strip()).replace(',', '.')) != '') and (str((self.myParent.myData.iloc[self.myParent.currentRow, 11].strip()).replace(',', '.')) != ''):
            self.myUpperTolerance = float((self.myParent.myData.iloc[self.myParent.currentRow, 10].strip()).replace(',', '.'))
            self.myLowerTolerance = float((self.myParent.myData.iloc[self.myParent.currentRow, 11].strip()).replace(',', '.'))
        else:
            self.myUpperTolerance = True
            self.myLowerTolerance = True
        # Format the result to fit for json
        try:
            self.myResult = float(value)
        except:
            if str(value) == 'i.O.':
                self.myResult = True
            else:
                self.myResult = False
        # Format the serial number to fit for json
        if str(serial) != '':
            self.mySerialNo = str(serial)
        else:
            self.mySerialNo = None
        # Format the date to fit for json
        self.myDate = str(myDate)
        # Format the time to fit for json
        self.myTime = str(myTime)
        # Format the comment to fit for json
        if str(comment) != '':
            self.myComment = str(comment)
        else:
            self.myComment = None
        # The datatype of the value and tolerances must be the same.
        if (isinstance(self.myUpperTolerance, bool)) and (isinstance(self.myResult, float)):
            self.myUpperTolerance = str(self.myUpperTolerance)
            self.myLowerTolerance = str(self.myLowerTolerance)
            self.myResult = str(self.myResult)
        elif (isinstance(self.myUpperTolerance, float)) and (isinstance(self.myResult, bool)):
            self.myUpperTolerance = str(self.myUpperTolerance)
            self.myLowerTolerance = str(self.myLowerTolerance)
            self.myResult = str(self.myResult)
        # Detect the current body-number of the dict for the json log file
        self.counter = 1
        while str(self.counter) in self.myParent.myResultLog:
            self.counter = self.counter + 1
        # Add the data to the dict for the json file
        self.myParent.myResultLog[str(self.counter)] = {'ID' : self.myId, 'Description' : self.myDescription, 'Nominal_Value' : self.myNominalValue, 'Unit' : self.myUnit, 'Upper_Tolerance' : self.myUpperTolerance, 'Lower_Tolerance' : self.myLowerTolerance, 'Result' : self.myResult, 'Serial_No' : self.mySerialNo, 'Date' : self.myDate, 'Time' : self.myTime, 'Comment' : self.myComment}

    # Save the result as json file to the hd.
    def saveResultLog2(self, timestamp):
        self.saveTimeStamp = str(timestamp)
        # Check if the Log folder exist. If not, create it
        if not os.path.exists(os.path.join(self.mySeperatedPath[0] + os.sep + 'Log')):
            os.makedirs(os.path.join(self.mySeperatedPath[0] + os.sep + 'Log'))
        # Save the json file in the log folder
        self.countLog = 0
        while (os.path.exists(os.path.join(self.mySeperatedPath[0] + os.sep + 'Log' + os.sep + self.saveTimeStamp + '_' + self.firstInstructionName + '_' + self.myParent.myContractNumber + '_' + str(self.countLog) + '.json'))):
            self.countLog = self.countLog + 1
        try:
            with open(os.path.join(self.mySeperatedPath[0] + os.sep + 'Log' + os.sep + self.saveTimeStamp + '_' + self.firstInstructionName + '_' + self.myParent.myContractNumber + '_' + str(self.countLog) + '.json'), 'w', newline='', encoding='utf-8-sig') as myFile:
                # Create the json file
                myJsonFile = json.dumps(self.myParent.myResultLog, sort_keys=False, ensure_ascii=False, indent=4)
                # Write the json file to the hd
                myFile.write(myJsonFile)
        except Exception as e:
            self.myParent.myErrorMessage(str(e))

    # Return the whole available result data
    def returnResult(self):
        return self.myResultData