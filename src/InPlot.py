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

# matplotlib for plotting
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')

# Necessary modules of matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Necessary QT Modules
from PyQt5 import QtWidgets

#Numpy and scipy for statistical operations
import numpy as np
from scipy import stats


# The basic canvas to pin the charts on. It is a QWidget
class MyCanvas(FigureCanvas):
    def __init__(self, parent, parentWidget, width, height, dpi):
        # Set up the variables
        self.myParentWidget = parentWidget
        self.myParent = parent
        self.myWidth = width
        self.myHeight = height
        self.myDpi = dpi
        # Set up the canvas 1/2
        self.fig = Figure(figsize=(self.myWidth, self.myHeight), dpi=self.myDpi)
        self.axes = self.fig.add_subplot(111)
        # Run the calculation of the specified plot
        self.compute_initial_figure()
        # Set up the canvas 2/2
        FigureCanvas.__init__(self, self.fig)
        self.setParent(self.myParentWidget)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    # All classes which inherit from MyCanvas, override compute_initial_figure. So here we can just pass.
    def compute_initial_figure(self):
        pass

# The SPC Chart
class MySpcCanvas(MyCanvas):
    # Compute the SPC plot for the first time
    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], 'r')

    # Update the SPC plot
    def update_figure(self, data, uil, lil):
        # myResultData is a pandas dataframe with all the results
        self.myResultData = data
        # The interference level for all of the data
        self.upperInterferenceLevel = uil
        self.lowerInterferenceLevel = lil
        try:
            # Clear all axes
            self.axes.cla()
            # Update the plot
            # myAttributeResult stores the results of only the current selected ID
            self.myAttributeResult = self.myResultData.loc[self.myResultData['ID'] == str(self.myParent.myData.iloc[self.myParent.currentRow, 0].strip())]
            # If there is no data, do not update and show the plot
            if len(self.myAttributeResult.index) == 0:
                return False
            # If there is data, update and show the plot
            else:
                # Generate the xValues (Max. the last ten result numbers)
                if (len(self.myAttributeResult.index) - 10) <= 0:
                    self.xValues = list(range(1, len(self.myAttributeResult.index) + 1))
                else:
                    self.xValues = list(range(len(self.myAttributeResult.index) - 9, len(self.myAttributeResult.index) + 1))
                # Read all data according to the generated xValues
                self.yValues = []
                self.upperTolerance = []
                self.lowerTolerance = []
                self.upperInterference = []
                self.lowerInterference = []
                for value in self.xValues:
                    # The yValues (Measured result)
                    self.yValues.append(float(self.myAttributeResult.iloc[value - 1, 6]))
                    # The upper tolerance level
                    self.upperTolerance.append(float(self.myAttributeResult.iloc[value - 1, 4]))
                    # The lower tolerance level
                    self.lowerTolerance.append(float(self.myAttributeResult.iloc[value - 1, 5]))
                    # The upper interference level
                    self.upperInterference.append(self.upperInterferenceLevel)
                    # The lower interference level
                    self.lowerInterference.append(self.lowerInterferenceLevel)
                # Set the name for the y axis
                self.axes.set_ylabel('[' + self.myAttributeResult.iloc[len(self.myAttributeResult.index) - 1, 3] + ']')
                # Set up the plot
                self.axes.plot(self.xValues, self.yValues, 'k-', lw=1, marker='.', markerfacecolor='red', markeredgecolor='black', markersize=6)
                self.axes.plot(self.xValues, self.upperTolerance, 'r-', lw=1.5)
                self.axes.plot(self.xValues, self.lowerTolerance, 'r-', lw=1.5)
                self.axes.plot(self.xValues, self.upperInterference, 'b--', lw=1)
                self.axes.plot(self.xValues, self.lowerInterference, 'b--', lw=1)


                # Draw the new plot
                self.draw()
                return True
        except Exception as e:
            self.myParent.myErrorMessage(str(e))

    # Update the SPC fullscreen plot
    def update_figure_full(self, data, uil, lil, row):
        # myResultData is a pandas dataframe with all the results
        self.myResultData = data
        # The interference level for all of the data
        self.upperInterferenceLevel = uil
        self.lowerInterferenceLevel = lil
        # The row to show
        self.myRow = row
        try:
            # Clear all axes
            self.axes.cla()
            # Update the plot
            # myAttributeResult stores the results of only the current selected ID
            self.myAttributeResult = self.myResultData.loc[self.myResultData['ID'] == str(self.myParent.myData.iloc[self.myRow, 0].strip())]
            # If there is no data, do not update and show the plot
            if len(self.myAttributeResult.index) == 0:
                return False
            # If there is data, update and show the plot
            else:
                # Generate the xValues
                self.xValues = list(range(1, len(self.myAttributeResult.index) + 1))
                # Read all data according to the generated xValues
                self.yValues = []
                self.upperTolerance = []
                self.lowerTolerance = []
                self.upperInterference = []
                self.lowerInterference = []
                for value in self.xValues:
                    # The yValues (Measured result)
                    self.yValues.append(float(self.myAttributeResult.iloc[value - 1, 6]))
                    # The upper tolerance level
                    self.upperTolerance.append(float(self.myAttributeResult.iloc[value - 1, 4]))
                    # The lower tolerance level
                    self.lowerTolerance.append(float(self.myAttributeResult.iloc[value - 1, 5]))
                    # The upper interference level
                    self.upperInterference.append(self.upperInterferenceLevel)
                    # The lower interference level
                    self.lowerInterference.append(self.lowerInterferenceLevel)
                # Set the name for the y axis
                self.axes.set_ylabel('[' + self.myAttributeResult.iloc[len(self.myAttributeResult.index) - 1, 3] + ']')
                # Set the name for the x axis
                self.axes.set_xlabel('Messpunkte')
                # Set up the plot
                self.axes.plot(self.xValues, self.yValues, 'k-', lw=1, marker='.', markerfacecolor='red', markeredgecolor='black', markersize=6)
                self.axes.plot(self.xValues, self.upperTolerance, 'r-', lw=1.5, label='Toleranzgrenze')
                self.axes.plot(self.xValues, self.lowerTolerance, 'r-', lw=1.5)
                self.axes.plot(self.xValues, self.upperInterference, 'b--', lw=1, label='Eingriffsgrenze')
                self.axes.plot(self.xValues, self.lowerInterference, 'b--', lw=1)
                # Put the legend in the upper left corner of the chart
                self.axes.legend(loc=2)
                # Draw the new plot
                self.draw()
                # Add the navigation toolbar
                self.mySpcFullToolbar = NavigationToolbar(self, self.myParent.myFrameSpcFull)
                return True
        except Exception as e:
            self.myParent.myErrorMessage(str(e))

    def currentResultData(self):
        return self.myAttributeResult

# The deviation chart
class MyDeviationCanvas(MyCanvas):
    # Compute the deviation chart for the first time
    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], 'r')
        self.axes2 = self.axes.twinx()
        self.axes2.plot([3, 2, 1, 0], 'k-')

    # Update the deviation chart
    def update_figure(self, data):
        # myResultData is a pandas dataframe with all the results
        self.myResultData = data
        try:
            # Clear all axes
            self.axes.cla()
            self.axes2.cla()
            # Update the plot
            # myAttributeResult stores the results of only the current selected ID
            self.myAttributeResult = self.myResultData.loc[self.myResultData['ID'] == str(self.myParent.myData.iloc[self.myParent.currentRow, 0].strip())]
            # Only show the graph if there are at least 5 Values
            if len(self.myAttributeResult.index) < 5:
                return False
            # If there is data, update and show the plot
            else:
                self.spreadData = []
                if (len(self.myAttributeResult.index) - 50) <= 0:
                    for value in range(1, len(self.myAttributeResult.index) + 1):
                        self.spreadData.append(float(self.myAttributeResult.iloc[value - 1, 6]))
                else:
                    for value in range(len(self.myAttributeResult.index) - 49, len(self.myAttributeResult.index) + 1):
                        self.spreadData.append(float(self.myAttributeResult.iloc[value - 1, 6]))
                # If min and max value are identical, you can not calculate the standard deviation.
                if min(self.spreadData) == max(self.spreadData):
                    return False
                else:
                    # The upper tolerance level
                    self.spreadUpperTolerance = float(self.myAttributeResult.iloc[len(self.myAttributeResult.index) - 1, 4])
                    # The lower tolerance level
                    self.spreadLowerTolerance = float(self.myAttributeResult.iloc[len(self.myAttributeResult.index) - 1, 5])
                    # Calculate the standard deviation
                    self.spreadStd = np.std(self.spreadData)
                    # Calculate the arithmetic average
                    self.spreadAvg = np.average(self.spreadData)
                    # Calculate the upper six sigma level
                    self.spreadPlusSigma = float(self.spreadAvg + (6 * self.spreadStd))
                    # Calculate the lower six sigma level
                    self.spreadMinusSigma = float(self.spreadAvg - (6 * self.spreadStd))
                    # The min. x value
                    self.xMin = min(float(min(self.spreadData)), self.spreadMinusSigma, self.spreadLowerTolerance)
                    # The max. x value
                    self.xMax = max(float(max(self.spreadData)), self.spreadPlusSigma, self.spreadUpperTolerance)
                    # Plot the histogram
                    self.axes.hist(self.spreadData, bins=30, range=(self.xMin, self.xMax), color='0.75')
                    self.axes.axvline(self.spreadUpperTolerance, color='red' , lw=1.5)
                    self.axes.axvline(self.spreadLowerTolerance, color='red' , lw=1.5)
                    self.axes.axvline(self.spreadPlusSigma, color='green', lw=1)
                    self.axes.axvline(self.spreadMinusSigma, color='green', lw=1)
                    self.axes.set_ylabel('Häufigkeit')
                    # Plot the probability density. Generate (self.xMax - self.xMin)/1000-digit x-values for a smooth deviation line
                    self.xValuesBestFit = np.arange(self.xMin, self.xMax, (self.xMax - self.xMin) / 1000)
                    self.yValuesBestFit = stats.norm.pdf(self.xValuesBestFit, self.spreadAvg, self.spreadStd)
                    # Plot the line and name the label
                    self.axes2.plot(self.xValuesBestFit, self.yValuesBestFit, 'k-', lw=1)
                    self.axes2.set_ylabel('Normalverteilung')
                   # Draw the new plot
                    self.draw()
                    return True
        except Exception as e:
            self.myParentWidget.myErrorMessage(str(e))

    # Update the deviation fullscreen plot
    def update_figure_full(self, data, row):
        # myResultData is a pandas dataframe with all the results
        self.myResultData = data
        # The row to show
        self.myRow = row
        try:
            # Clear all axes
            self.axes.cla()
            self.axes2.cla()
            # Update the plot
            # myAttributeResult stores the results of only the current selected ID
            self.myAttributeResult = self.myResultData.loc[self.myResultData['ID'] == str(self.myParent.myData.iloc[self.myRow, 0].strip())]
            # Only show the graph if there are at least 5 Values
            if len(self.myAttributeResult.index) < 5:
                return False
            # If there is data, update and show the plot
            else:
                self.spreadData = []
                for value in range(1, len(self.myAttributeResult.index) + 1):
                    self.spreadData.append(float(self.myAttributeResult.iloc[value - 1, 6]))
                # If min and max value are identical, you can not calculate the standard deviation.
                if min(self.spreadData) == max(self.spreadData):
                    return False
                else:
                    # The upper tolerance level
                    self.spreadUpperTolerance = float(self.myAttributeResult.iloc[len(self.myAttributeResult.index) - 1, 4])
                    # The lower tolerance level
                    self.spreadLowerTolerance = float(self.myAttributeResult.iloc[len(self.myAttributeResult.index) - 1, 5])
                    # Calculate the standard deviation
                    self.spreadStd = np.std(self.spreadData)
                    # Calculate the arithmetic average
                    self.spreadAvg = np.average(self.spreadData)
                    # Calculate the upper six sigma level
                    self.spreadPlusSigma = float(self.spreadAvg + (6 * self.spreadStd))
                    # Calculate the lower six sigma level
                    self.spreadMinusSigma = float(self.spreadAvg - (6 * self.spreadStd))
                    # The min. x value
                    self.xMin = min(float(min(self.spreadData)), self.spreadMinusSigma, self.spreadLowerTolerance)
                    # The max. x value
                    self.xMax = max(float(max(self.spreadData)), self.spreadPlusSigma, self.spreadUpperTolerance)
                    # Plot the histogram
                    self.axes.hist(self.spreadData, bins=30, range=(self.xMin, self.xMax), color='0.75')
                    self.axes.axvline(self.spreadUpperTolerance, color='red' , lw=1.5, label='Toleranzgrenze')
                    self.axes.axvline(self.spreadLowerTolerance, color='red' , lw=1.5)
                    self.axes.axvline(self.spreadPlusSigma, color='green', lw=1, label='Six Sigma Grenze')
                    self.axes.axvline(self.spreadMinusSigma, color='green', lw=1)
                    # Put the legend in the upper left corner of the chart
                    self.axes.legend(loc=2)
                    self.axes.set_ylabel('Häufigkeit')
                    self.axes.set_xlabel('[' + self.myAttributeResult.iloc[len(self.myAttributeResult.index) - 1, 3] + ']')
                    # Plot the probability density. Generate (self.xMax - self.xMin)/1000-digit x-values for a smooth deviation line
                    self.xValuesBestFit = np.arange(self.xMin, self.xMax, (self.xMax - self.xMin) / 1000)
                    self.yValuesBestFit = stats.norm.pdf(self.xValuesBestFit, self.spreadAvg, self.spreadStd)
                    # Plot the line and name the label
                    self.axes2.plot(self.xValuesBestFit, self.yValuesBestFit, 'k-', lw=1)
                    self.axes2.set_ylabel('Normalverteilung')
                    # Draw the new plot
                    self.draw()
                    # Add the navigation toolbar
                    self.myDefiationFullToolbar = NavigationToolbar(self, self.myParent.myFrameDeviationFull)
                    return True
        except Exception as e:
            self.myParentWidget.myErrorMessage(str(e))


    def currentResultData(self):
        return self.myAttributeResult