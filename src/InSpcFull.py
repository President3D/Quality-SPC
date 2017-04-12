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

# InModel for test instruction data management
from InModel import MyCharacteristicsTableModel, MyResultTableModel

# decimal for correctly rounded float point arithmetic
from decimal import Decimal

#statistics and scipy for statistical operations
from scipy import stats
from statistics import mean, stdev


# The SPC fullscreen page
class MySpcFull():
    def __init__(self, parent, resultData):
        self.myParent = parent
        self.myResult = resultData
        # Create the table model
        self.mySpcTableModel = MyCharacteristicsTableModel(self.myParent.myData)
        # Create the table view
        self.myParent.myTableViewCharacteristicsPageSpc.setModel(self.mySpcTableModel)
        self.myParent.myTableViewCharacteristicsPageSpc.resizeColumnsToContents()
        # Show the file name
        self.myParent.myLabelTestInstructionNamePageSpc.setText(os.path.split(os.path.normpath(self.myParent.myTestInstructionFile[0]))[1])
        # Every Time a new line is selected, this code detects it and runs the newLineSelected-method.
        self.selectionModel = self.myParent.myTableViewCharacteristicsPageSpc.selectionModel()
        self.selectionModel.selectionChanged.connect(self.newLineSelection)
        # Hide the SPC Chart at the beginning
        self.myParent.myFrameSpcFull.hide()
        # Select row 0
        self.myParent.myTableViewCharacteristicsPageSpc.setFocus()
        self.myParent.myTableViewCharacteristicsPageSpc.selectRow(0)

    # If a new line is selected
    def newLineSelection(self):
        # The current selected row number
        self.selectedRow = self.myParent.myTableViewCharacteristicsPageSpc.selectionModel().selectedRows()
        self.selectedRowNumber = self.selectedRow[0].row()
        # Clear all labels
        self.myParent.myLabelSpcUtlValue.hide()
        self.myParent.myLabelSpcLtlValue.hide()
        self.myParent.myLabelSpcUilValue.hide()
        self.myParent.myLabelSpcLilValue.hide()
        self.myParent.myLabelSpcAverageValue.hide()
        self.myParent.myLabelSpcDeivationValue.hide()
        self.myParent.myLabelSpcAndSixSigmaValue.hide()
        self.myParent.myLabelSpcMinusSixSigmaValue.hide()
        self.myParent.myLabelSpcCpkValue.hide()
        self.myParent.myLabelSpcPpmValue.hide()
        # Hide the spc frame at first, in case the attribute ist not quantitative.
        self.myParent.myFrameSpcFull.hide()
        # If the current selected row is quantitative and there is enough result data, show it.
        if self.myParent.myData.iloc[self.selectedRowNumber, 2].strip() == '2':
            self.showSpcFull = self.myParent.spcFullPlot.update_figure_full(self.myParent.myResult.returnResult(), float(((self.myParent.myData.iloc[self.selectedRowNumber, 12]).strip()).replace(',', '.')), float(((self.myParent.myData.iloc[self.selectedRowNumber, 13]).strip()).replace(',', '.')), self.selectedRowNumber)
            if self.showSpcFull:
                self.myParent.myFrameSpcFull.show()
            else:
                self.myParent.myFrameSpcFull.hide()
            # Calculate the statistics
            self.mySpcStatisticData = self.myParent.spcFullPlot.currentResultData()
            # The upper tolerance level
            self.spcFullUpperTolerance = Decimal(((self.myParent.myData.iloc[self.selectedRowNumber, 10]).strip()).replace(',', '.'))
            self.myParent.myLabelSpcUtlValue.setText(str(self.spcFullUpperTolerance) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
            self.myParent.myLabelSpcUtlValue.show()
            # The lower tolerance level
            self.spcFullLowerTolerance = Decimal(((self.myParent.myData.iloc[self.selectedRowNumber, 11]).strip()).replace(',', '.'))
            self.myParent.myLabelSpcLtlValue.setText(str(self.spcFullLowerTolerance) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
            self.myParent.myLabelSpcLtlValue.show()
            # The upper interference level
            self.spcFullUpperInterference = Decimal(((self.myParent.myData.iloc[self.selectedRowNumber, 12]).strip()).replace(',', '.'))
            self.myParent.myLabelSpcUilValue.setText(str(self.spcFullUpperInterference) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
            self.myParent.myLabelSpcUilValue.show()
            # The lower interference level
            self.spcFullLowerInterference = Decimal(((self.myParent.myData.iloc[self.selectedRowNumber, 13]).strip()).replace(',', '.'))
            self.myParent.myLabelSpcLilValue.setText(str(self.spcFullLowerInterference) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
            self.myParent.myLabelSpcLilValue.show()
            # The result data of the current attribute
            self.mySpcAttributeResult = self.myResult.loc[self.myResult['ID'] == str(self.myParent.myData.iloc[self.selectedRowNumber, 0].strip())]
            if len(self.mySpcAttributeResult.index) >= 5:
                self.spcStatistic()

    # Calculate the statistics
    def spcStatistic(self):
        # Store all relevant date of this attribute in the list spcSpreadData, as a float.
        self.spcSpreadData = []
        for value in range(1, len(self.mySpcAttributeResult.index) + 1):
            self.spcSpreadData.append(float(self.mySpcAttributeResult.iloc[value - 1, 6]))
        # Calculate the arithmetic average
        self.mySpcSpreadAvg = mean(self.spcSpreadData)
        self.myParent.myLabelSpcAverageValue.setText(str(round(self.mySpcSpreadAvg, 4)) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
        self.myParent.myLabelSpcAverageValue.show()
        # Calculate the standard deviation
        self.mySpcSpreadStd = stdev(self.spcSpreadData)
        self.myParent.myLabelSpcDeivationValue.setText(str(round(self.mySpcSpreadStd, 4)) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
        self.myParent.myLabelSpcDeivationValue.show()
        # Calculate the upper six sigma level
        self.mySpcUpperSixSigma = self.mySpcSpreadAvg + (6*self.mySpcSpreadStd)
        self.myParent.myLabelSpcAndSixSigmaValue.setText(str(round(self.mySpcUpperSixSigma, 4)) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
        self.myParent.myLabelSpcAndSixSigmaValue.show()
        # Calculate the lower six sigma level
        self.mySpcLowerSixSigma = self.mySpcSpreadAvg - (6*self.mySpcSpreadStd)
        self.myParent.myLabelSpcMinusSixSigmaValue.setText(str(round(self.mySpcLowerSixSigma, 4)) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
        self.myParent.myLabelSpcMinusSixSigmaValue.show()
        # Calculate the Cpk
        try:
            self.mySpcCpk = min(float(self.mySpcSpreadAvg) - float(self.spcFullLowerTolerance), float(self.spcFullUpperTolerance) - float(self.mySpcSpreadAvg)) / (3 * float(self.mySpcSpreadStd))
            self.myParent.myLabelSpcCpkValue.setText(str(round(self.mySpcCpk, 2)))
            self.myParent.myLabelSpcCpkValue.show()
        # There are cases, the Cpk can not be calculated.
        except:
            self.myParent.myLabelSpcCpkValue.setText('-')
            self.myParent.myLabelSpcCpkValue.show()
        # Calculate the PPM with the cumulative probability density
        try:
            self.mySpcCumulativeDensityY = stats.norm.cdf([float(self.spcFullLowerTolerance), float(self.spcFullUpperTolerance)], float(self.mySpcSpreadAvg), float(self.mySpcSpreadStd))
            self.mySpcPpm = (1 - (self.mySpcCumulativeDensityY[1] - self.mySpcCumulativeDensityY[0])) * 1000000
            self.myParent.myLabelSpcPpmValue.setText(str(int(self.mySpcPpm)))
            self.myParent.myLabelSpcPpmValue.show()
        # There are cases, the PPM can not be calculated.
        except:
            self.myParent.myLabelSpcPpmValue.setText('-')
            self.myParent.myLabelSpcPpmValue.show()

# The Deviation fullscreen chart
class MyDeviationFull():
    def __init__(self, parent, resultData):
        self.myParent = parent
        self.myResult = resultData
        # Create the table model
        self.myDeviationTableModel = MyCharacteristicsTableModel(self.myParent.myData)
        # Create the table view
        self.myParent.myTableViewCharacteristicsDeviationFull.setModel(self.myDeviationTableModel)
        self.myParent.myTableViewCharacteristicsDeviationFull.resizeColumnsToContents()
        # Show the file name
        self.myParent.myLabelTestInstructionNamePageDeviation.setText(os.path.split(os.path.normpath(self.myParent.myTestInstructionFile[0]))[1])
        # Every Time a new line is selected, this code detects it and runs the newLineSelected-method.
        self.selectionModel = self.myParent.myTableViewCharacteristicsDeviationFull.selectionModel()
        self.selectionModel.selectionChanged.connect(self.newLineSelection)
        # Hide the SPC Chart at the beginning
        self.myParent.myFrameDeviationFull.hide()
        # Select row 0
        self.myParent.myTableViewCharacteristicsDeviationFull.setFocus()
        self.myParent.myTableViewCharacteristicsDeviationFull.selectRow(0)

    # If a new line is selected
    def newLineSelection(self):
        # The current selected row number
        self.selectedRow = self.myParent.myTableViewCharacteristicsDeviationFull.selectionModel().selectedRows()
        self.selectedRowNumber = self.selectedRow[0].row()
        # Clear all labels
        self.myParent.myLabelDeviationCpkValue.hide()
        self.myParent.myLabelDeviationAverageValue.hide()
        self.myParent.myLabelDeviationDeivationValue.hide()
        self.myParent.myLabelDeviationAndSixSigmaValue.hide()
        self.myParent.myLabelDeviationMinusSixSigmaValue.hide()
        self.myParent.myLabelDeviationPpmValue.hide()
        self.myParent.myLabelDeviationUtlValue.hide()
        self.myParent.myLabelDeviationLtlValue.hide()
        self.myParent.myLabelDeviationUilValue.hide()
        self.myParent.myLabelDeviationLilValue.hide()
        # Hide the deviation frame at first, in case the attribute ist not quantitative.
        self.myParent.myFrameDeviationFull.hide()
        # If the current selected row is quantitative and there is enough result data, show it.
        if self.myParent.myData.iloc[self.selectedRowNumber, 2].strip() == '2':
            self.showDeviationFull = self.myParent.deviationFullPlot.update_figure_full(self.myParent.myResult.returnResult(), self.selectedRowNumber)
            if self.showDeviationFull:
                self.myParent.myFrameDeviationFull.show()
            else:
                self.myParent.myFrameDeviationFull.hide()
            # Calculate the statistics
            self.myDeviationStatisticData = self.myParent.deviationFullPlot.currentResultData()
            # The upper tolerance level
            self.deviationFullUpperTolerance = Decimal(((self.myParent.myData.iloc[self.selectedRowNumber, 10]).strip()).replace(',', '.'))
            self.myParent.myLabelDeviationUtlValue.setText(str(self.deviationFullUpperTolerance) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
            self.myParent.myLabelDeviationUtlValue.show()
            # The lower tolerance level
            self.deviationFullLowerTolerance = Decimal(((self.myParent.myData.iloc[self.selectedRowNumber, 11]).strip()).replace(',', '.'))
            self.myParent.myLabelDeviationLtlValue.setText(str(self.deviationFullLowerTolerance) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
            self.myParent.myLabelDeviationLtlValue.show()
            # The upper interference level
            self.deviationFullUpperInterference = Decimal(((self.myParent.myData.iloc[self.selectedRowNumber, 12]).strip()).replace(',', '.'))
            self.myParent.myLabelDeviationUilValue.setText(str(self.deviationFullUpperInterference) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
            self.myParent.myLabelDeviationUilValue.show()
            # The lower interference level
            self.deviationFullLowerInterference = Decimal(((self.myParent.myData.iloc[self.selectedRowNumber, 13]).strip()).replace(',', '.'))
            self.myParent.myLabelDeviationLilValue.setText(str(self.deviationFullLowerInterference) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
            self.myParent.myLabelDeviationLilValue.show()
            # The result data of the current attribute
            self.myDeviationAttributeResult = self.myResult.loc[self.myResult['ID'] == str(self.myParent.myData.iloc[self.selectedRowNumber, 0].strip())]
            if len(self.myDeviationAttributeResult.index) >= 5:
                self.deviationStatistic()

    # Calculate the statistics
    def deviationStatistic(self):
        # Store all relevant date of this attribute in the list deviationSpreadData, as a float.
        self.deviationSpreadData = []
        for value in range(1, len(self.myDeviationAttributeResult.index) + 1):
            self.deviationSpreadData.append(float(self.myDeviationAttributeResult.iloc[value - 1, 6]))
        # Calculate the arithmetic average
        self.myDeviationSpreadAvg = mean(self.deviationSpreadData)
        self.myParent.myLabelDeviationAverageValue.setText(str(round(self.myDeviationSpreadAvg, 4)) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
        self.myParent.myLabelDeviationAverageValue.show()
        # Calculate the standard deviation
        self.myDeviationSpreadStd = stdev(self.deviationSpreadData)
        self.myParent.myLabelDeviationDeivationValue.setText(str(round(self.myDeviationSpreadStd, 4)) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
        self.myParent.myLabelDeviationDeivationValue.show()
        # Calculate the upper six sigma level
        self.myDeviationUpperSixSigma = self.myDeviationSpreadAvg + (6*self.myDeviationSpreadStd)
        self.myParent.myLabelDeviationAndSixSigmaValue.setText(str(round(self.myDeviationUpperSixSigma, 4)) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
        self.myParent.myLabelDeviationAndSixSigmaValue.show()
        # Calculate the lower six sigma level
        self.myDeviationLowerSixSigma = self.myDeviationSpreadAvg - (6*self.myDeviationSpreadStd)
        self.myParent.myLabelDeviationMinusSixSigmaValue.setText(str(round(self.myDeviationLowerSixSigma, 4)) + ' ' + self.myParent.myData.iloc[self.selectedRowNumber, 7].strip())
        self.myParent.myLabelDeviationMinusSixSigmaValue.show()
        # Calculate the Cpk
        try:
            self.myDeviationCpk = min(float(self.myDeviationSpreadAvg) - float(self.deviationFullLowerTolerance), float(self.deviationFullUpperTolerance) - float(self.myDeviationSpreadAvg)) / (3 * float(self.myDeviationSpreadStd))
            self.myParent.myLabelDeviationCpkValue.setText(str(round(self.myDeviationCpk, 2)))
            self.myParent.myLabelDeviationCpkValue.show()
        # There are cases, the Cpk can not be calculated.
        except:
            self.myParent.myLabelDeviationCpkValue.setText('-')
            self.myParent.myLabelDeviationCpkValue.show()
        # Calculate the PPM with the cumulative probability density
        try:
            self.myDeviationCumulativeDensityY = stats.norm.cdf([float(self.deviationFullLowerTolerance), float(self.deviationFullUpperTolerance)], float(self.myDeviationSpreadAvg), float(self.myDeviationSpreadStd))
            self.myDeviationPpm = (1 - (self.myDeviationCumulativeDensityY[1] - self.myDeviationCumulativeDensityY[0])) * 1000000
            self.myParent.myLabelDeviationPpmValue.setText(str(int(self.myDeviationPpm)))
            self.myParent.myLabelDeviationPpmValue.show()
        # There are cases, the PPM can not be calculated.
        except:
            self.myParent.myLabelDeviationPpmValue.setText('-')
            self.myParent.myLabelDeviationPpmValue.show()


# The result list page
class MyResultList():
    def __init__(self, parent, resultData):
        self.myParent = parent
        self.myResult = resultData
        # Create the table model
        self.myResultTableModel = MyCharacteristicsTableModel(self.myParent.myData)
        # Create the table view
        self.myParent.myTableViewCharacteristicsPageResult.setModel(self.myResultTableModel)
        self.myParent.myTableViewCharacteristicsPageResult.resizeColumnsToContents()
        # Show the file name
        self.myParent.myLabelTestInstructionNamePageResult.setText(os.path.split(os.path.normpath(self.myParent.myTestInstructionFile[0]))[1])
        # Every Time a new line is selected, this code detects it and runs the newLineSelected-method.
        self.selectionModel = self.myParent.myTableViewCharacteristicsPageResult.selectionModel()
        self.selectionModel.selectionChanged.connect(self.newLineSelection)
        # Select row 0
        self.myParent.myTableViewCharacteristicsPageResult.setFocus()
        self.myParent.myTableViewCharacteristicsPageResult.selectRow(0)

    # If a new line is selected
    def newLineSelection(self):
        # The current selected row number
        self.selectedRow = self.myParent.myTableViewCharacteristicsPageResult.selectionModel().selectedRows()
        self.selectedRowNumber = self.selectedRow[0].row()
        # myAttributeResult stores the results of only the current selected ID
        self.myAttributeResult = self.myResult.loc[self.myResult['ID'] == str(self.myParent.myData.iloc[self.selectedRowNumber, 0].strip())]
        # Create the table model of the current selected ID
        self.myAttributeResultTableModel = MyResultTableModel(self.myAttributeResult)
        # Show the table model
        self.myParent.myTableViewResult.setModel(self.myAttributeResultTableModel)
        self.myParent.myTableViewResult.resizeColumnsToContents()
