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
from PyQt5.QtWidgets import QWidget

# Own UIs
from Ui.InFormEditTestInstruction import Ui_myFormEdit


# The charecteristics edit form
class MyEditWidget(QWidget, Ui_myFormEdit):
    def __init__(self, parent):
        super(MyEditWidget, self).__init__()
        self.myParent = parent

    # The UI for quantitative attributes
    def startUi(self):
        # Set up the ui from designer
        self.setupUi(self)

