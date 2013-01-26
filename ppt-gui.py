#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, signal

from gui.main import PPTGUI

from PyQt4 import QtGui

def main():
    """The Main Loop !"""
    app = QtGui.QApplication(sys.argv)
    ppt = PPTGUI()
    ppt.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL) 
    main()
