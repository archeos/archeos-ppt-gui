#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from gui.main import PPTGUI

from PyQt4 import QtGui

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    ppt = PPTGUI()
    ppt.show()
    app.exec_()
