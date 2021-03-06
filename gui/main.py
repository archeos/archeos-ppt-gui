# -*- coding: utf-8 -*-
import os

from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4.QtCore import QProcess

"""
- Processes are defined in the Global scope because I noticed

- I also use an interleave stdout and stderr (MergedChannels).
we need to do that because CMVS write some output in stderr (?).
So, a proper error handling in a separate channel is impossible.
"""
procB = QProcess()
procB.setProcessChannelMode(QProcess.MergedChannels)
procC = QProcess()
procC.setProcessChannelMode(QProcess.MergedChannels)
procP = QProcess()
procP.setProcessChannelMode(QProcess.MergedChannels)
procCam = QProcess()
procCam.setProcessChannelMode(QProcess.MergedChannels)


class PPTGUI(QWidget):
    """The main Widget.
    TODO: PEP8
    TODO: Translations
    TODO: One Console, One process
    """

    def __init__(self):
        # Icons
        self.py_icon = QIcon(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                               'assets/icons/python_icon.png'))
        self.help_icon = QIcon(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                                'assets/icons/info_icon.png'))

        super(PPTGUI, self).__init__()
        ############################################################
        self.setWindowTitle('Python Photogrammetry Toolbox GUI v. 0.1')
        self.setGeometry(300, 300, 900, 580)
        self.setWindowIcon(self.py_icon)
        #############################################################
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 900, 580))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.initUI()
        # tabWidgets
        self.tabWidget.setTabText(
                self.tabWidget.indexOf(self.tab),
                QApplication.translate(
                    "MainWindow",
                    "1. Run Bundler",
                    None,
                    QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(
                self.tabWidget.indexOf(self.tab_3),
                QApplication.translate(
                    "MainWindow",
                    "2. Run CMVS/PMVS",
                    None,
                    QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(
                self.tabWidget.indexOf(self.tab_2),
                QApplication.translate(
                    "MainWindow",
                    "or run PMVS without CMVS",
                    None,
                    QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(
                self.tabWidget.indexOf(self.tab_4),
                QApplication.translate("MainWindow",
                    "Check Camera Database",
                    None,
                    QApplication.UnicodeUTF8))

    def initUI(self):
        """ Init GUI"""
        # BUNDLER
        # button 1 for pictures directory
        self.button1 = QPushButton('Select Photos Path', self.tab)
        self.button1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button1.move(20, 30)
        self.connect(self.button1,
                QtCore.SIGNAL('clicked()'),
                self.showDialog1)
        self.setFocus()

        # directory path label
        self.label9 = QLabel('path:', self.tab)
        self.label9.move(190, 34)
        self.text4 = QLineEdit(self.tab)
        self.text4.move(235, 30)
        self.text4.resize(550, 27)

        # help button select directory
        self.help_button1 = QPushButton("", self.tab)
        self.help_button1.setIcon(self.help_icon)
        self.help_button1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button1.move(800, 26)
        self.connect(
                self.help_button1,
                QtCore.SIGNAL('clicked()'),
                self.on_help1_clicked)
        self.setFocus()

        # features extractor combo
        self.label16 = QLabel('Select Feature Extractor:', self.tab)
        self.label16.move(20, 84)
        self.text15 = QLineEdit("siftvlfeat", self.tab)
        self.text15.setReadOnly(True)
        self.combo = QComboBox(self.tab)
        self.combo.addItem("siftvlfeat")
        self.combo.addItem("siftlowe")
        self.combo.move(200, 80)
        self.text15.move(360, 100)
        self.text15.resize(0, 0)
        self.connect(
                self.combo,
                QtCore.SIGNAL('activated(QString)'),
                self.onActivated)

        # help button features extractor
        self.help_button2 = QPushButton("", self.tab)
        self.help_button2.setIcon(self.help_icon)
        self.help_button2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button2.move(300, 76)
        self.connect(self.help_button2,
                QtCore.SIGNAL('clicked()'),
                self.on_help2_clicked)
        self.setFocus()

        # image width
        self.cb1 = QCheckBox('Set desired Photos Width:', self.tab)
        self.cb1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb1.move(380, 80)
        self.cb1.toggle()
        self.connect(
                self.cb1,
                QtCore.SIGNAL('stateChanged(int)'),
                self.changesize1)
        self.text13 = QLineEdit('1200', self.tab)
        self.text13.move(600, 78)
        self.text13.resize(70, 27)

        # help button width
        self.help_button3 = QPushButton("", self.tab)
        self.help_button3.setIcon(self.help_icon)
        self.help_button3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button3.move(720, 76)
        self.connect(self.help_button3,
                QtCore.SIGNAL('clicked()'),
                self.on_help3_clicked)
        self.setFocus()

        # image resize
        self.cb2 = QCheckBox(
                'Scale Photos with a Scaling Factor',
                self.tab)
        self.cb2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb2.move(380, 130)
        self.cb2.toggle()
        self.cb2.setChecked(False)
        self.connect(
                self.cb2,
                QtCore.SIGNAL('stateChanged(int)'),
                self.changesize2)
        self.text11 = QLineEdit("1", self.tab)
        self.text11.setReadOnly(True)
        self.combo2 = QComboBox(self.tab)
        self.combo2.hide()
        self.combo2.addItem("1")
        self.combo2.addItem("0.75")
        self.combo2.addItem("0.5")
        self.combo2.addItem("0.25")
        self.combo2.move(650, 130)
        self.text11.move(390, 100)
        self.text11.resize(0, 0)
        self.connect(
                self.combo2,
                QtCore.SIGNAL('activated(QString)'),
                self.onActivated2)

        # help button resize
        self.help_button4 = QPushButton("", self.tab)
        self.help_button4.setIcon(self.help_icon)
        self.help_button4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button4.move(720, 126)
        self.connect(
                self.help_button4,
                QtCore.SIGNAL('clicked()'),
                self.on_help4_clicked)
        self.setFocus()

        # button 4 for start bundler
        self.button4 = QPushButton('Run', self.tab)
        self.button4.setIcon(self.py_icon)
        self.button4.move(20, 180)
        self.connect(
                self.button4,
                QtCore.SIGNAL('clicked()'),
                self.startbundler)
        self.text2 = QLineEdit(self.tab)
        self.text2.move(120, 184)
        self.text2.setReadOnly(True)
        self.text2.resize(760, 27)
        self.connect(
                self.text4,
                QtCore.SIGNAL('textChanged(QString)'),
                self.onChangedpathbundler)
        self.connect(
                self.text15,
                QtCore.SIGNAL('textChanged(QString)'),
                self.onChangedextractor)
        self.connect(self.text13,
                QtCore.SIGNAL('textChanged(QString)'),
                self.onChangedwidth)
        self.connect(self.text11,
                QtCore.SIGNAL('textChanged(QString)'),
                self.onChangedsize)

        # output
        self.line1 = QFrame(self.tab)
        self.line1.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setObjectName("line1")
        self.label20 = QLabel('Output Bundler:', self.tab)
        self.label20.move(20, 240)
        self.output1 = QTextBrowser(self.tab)
        self.output1.move(20, 264)
        self.output1.resize(850, 270)
        self.output1.setAcceptRichText(True)
        self.output1.setAutoFormatting(QTextEdit.AutoBulletList)
        self.scroll1 = self.output1.verticalScrollBar()


        # CMVS/PMVS
        # button 2 for Bundler output directory
        self.button2 = QPushButton(
                'Select Bundler Output Path',
                self.tab_3)
        self.button2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button2.move(20, 30)
        self.connect(
                self.button2,
                QtCore.SIGNAL('clicked()'),
                self.showDialog2)
        self.setFocus()

        # directory output path label
        self.label10 = QLabel('path:', self.tab_3)
        self.label10.move(240, 34)
        self.text3 = QLineEdit(self.tab_3)
        self.text3.move(285, 30)
        self.text3.resize(500, 27)

        # help button 5 select bundler output directory
        self.help_button5 = QPushButton("", self.tab_3)
        self.help_button5.setIcon(self.help_icon)
        self.help_button5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button5.move(800, 26)
        self.connect(
                self.help_button5,
                QtCore.SIGNAL('clicked()'),
                self.on_help5_clicked)
        self.setFocus()

        # number images for cluster
        self.label11 = QLabel(
                'Number of Photos in each Cluster:',
                self.tab_3)
        self.label11.move(240, 84)
        self.text5 = QLineEdit('10', self.tab_3)
        self.text5.move(490, 82)
        self.text5.resize(70, 27)

        # help button 6 select bundler output directory
        self.help_button6 = QPushButton("", self.tab_3)
        self.help_button6.setIcon(self.help_icon)
        self.help_button6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button6.move(580, 79)
        self.connect(
                self.help_button6,
                QtCore.SIGNAL('clicked()'),
                self.on_help6_clicked)
        self.setFocus()

        # button run CMVS
        self.button5 = QPushButton('Run', self.tab_3)
        self.button5.setIcon(self.py_icon)
        self.button5.move(20, 130)
        self.connect(
                self.button5,
                QtCore.SIGNAL('clicked()'),
                self.startcmvs)
        self.text6 = QLineEdit(self.tab_3)
        self.text6.move(120, 134)
        self.text6.setReadOnly(True)
        self.text6.resize(760, 27)
        self.connect(
                self.text3,
                QtCore.SIGNAL('textChanged(QString)'),
                self.onChangedpathcmvs)
        self.connect(
                self.text5,
                QtCore.SIGNAL('textChanged(QString)'),
                self.onChangedcluster)

        # output
        self.line3 = QFrame(self.tab_3)
        self.line3.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        self.line3.setObjectName("line3")
        self.label21 = QLabel('Output CMVS/PMVS:', self.tab_3)
        self.label21.move(20, 240)
        self.output2 = QTextBrowser(self.tab_3)
        self.output2.move(20, 264)
        self.output2.resize(850, 270)
        self.output2.setAcceptRichText(True)
        self.output2.setAutoFormatting(QTextEdit.AutoBulletList)
        self.scroll2 = self.output2.verticalScrollBar()


        # run only PMVS
        self.cb3 = QCheckBox(
                'Use directly PMVS2 (without CMVS):',
                self.tab_2)
        self.cb3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cb3.move(20, 30)
        self.cb3.toggle()
        self.cb3.setChecked(False)
        self.connect(
                self.cb3,
                QtCore.SIGNAL('stateChanged(int)'),
                self.openpmvs)

        # button 3 for output directory
        self.button3 = QPushButton(
                'Select Bundler Output Path',
                self.tab_2)
        self.button3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button3.move(20, 80)
        self.button3.hide()
        self.connect(
                self.button3,
                QtCore.SIGNAL('clicked()'),
                self.showDialog3)
        self.setFocus()

        # directory output path label
        self.label14 = QLabel('path:', self.tab_2)
        self.label14.move(240, 84)
        self.label14.hide()

        self.text7 = QLineEdit(self.tab_2)
        self.text7.move(280, 80)
        self.text7.hide()
        self.text7.resize(500, 27)

        # help button 7 select bundler output directory
        self.help_button7 = QPushButton("", self.tab_2)
        self.help_button7.setIcon(self.help_icon)
        self.help_button7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button7.move(800, 76)
        self.help_button7.hide()
        self.connect(
                self.help_button7,
                QtCore.SIGNAL('clicked()'),
                self.on_help5_clicked)
        self.setFocus()

        # run PMVS
        self.button6 = QPushButton('Run', self.tab_2)
        self.button6.setIcon(self.py_icon)
        self.button6.move(20, 130)
        self.button6.hide()
        self.connect(
                self.button6,
                QtCore.SIGNAL('clicked()'),
                self.startpmvs)
        self.text8 = QLineEdit(self.tab_2)
        self.text8.move(120, 134)
        self.text8.setReadOnly(True)
        self.text8.hide()
        self.text8.resize(760, 27)
        self.connect(
                self.text7,
                QtCore.SIGNAL('textChanged(QString)'),
                self.onChangedpathpmvs)

        # output
        self.line2 = QFrame(self.tab_2)
        self.line2.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setObjectName("line2")
        self.label22 = QLabel('Output PMVS:', self.tab_2)
        self.label22.move(20, 240)
        self.output3 = QTextBrowser(self.tab_2)
        self.output3.move(20, 264)
        self.output3.resize(850, 270)
        self.output3.setAcceptRichText(True)
        self.output3.setAutoFormatting(QTextEdit.AutoBulletList)
        self.scroll3 = self.output3.verticalScrollBar()


        # CAMERA DATABASE
        # button 1 for pictures directory
        self.button8 = QPushButton('Select Photos Path', self.tab_4)
        self.button8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button8.move(20, 30)
        self.connect(
                self.button8,
                QtCore.SIGNAL('clicked()'),
                self.showDialog4)
        self.setFocus()

        # directory path label
        self.label12 = QLabel('path:', self.tab_4)
        self.label12.move(190, 34)
        self.text9 = QLineEdit(self.tab_4)
        self.text9.move(235, 30)
        self.text9.resize(550, 27)

        # help button select directory
        self.help_button9 = QPushButton("", self.tab_4)
        self.help_button9.setIcon(self.help_icon)
        self.help_button9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.help_button9.move(800, 26)
        self.connect(
                self.help_button9,
                QtCore.SIGNAL('clicked()'),
                self.on_help9_clicked)
        self.setFocus()

        # button run Camera Database
        self.button10 = QPushButton('Run', self.tab_4)
        self.button10.setIcon(self.py_icon)
        self.button10.move(20, 80)
        self.connect(
                self.button10,
                QtCore.SIGNAL('clicked()'),
                self.startcamdat)
        self.text10 = QLineEdit(self.tab_4)
        self.text10.move(120, 84)
        self.text10.setReadOnly(True)
        self.text10.resize(760, 27)
        self.connect(self.text9,
                QtCore.SIGNAL('textChanged(QString)'),
                self.onChangedpathcamdat)

        # output
        self.line4 = QFrame(self.tab_4)
        self.line4.setGeometry(QtCore.QRect(10, 220, 880, 20))
        self.line4.setFrameShape(QFrame.HLine)
        self.line4.setFrameShadow(QFrame.Sunken)
        self.line4.setObjectName("line1")
        self.label23 = QLabel(
                'Output Camera Database:',
                self.tab_4)
        self.label23.move(20, 240)
        self.output4 = QTextBrowser(self.tab_4)
        self.output4.move(20, 264)
        self.output4.resize(850, 270)
        self.output4.setAcceptRichText(True)
        self.output4.setAutoFormatting(QTextEdit.AutoBulletList)
        self.scroll4 = self.output4.verticalScrollBar()


    # select directory with photos
    def showDialog1(self):
        directoryname = QFileDialog.getExistingDirectory(
                self,
                'Open directory with photos',
                '/home')
        self.text4.setText(directoryname)

    # combo vlfeat-sift
    def onActivated(self, text):
        self.text15.setText(text)

    # combo size-image
    def onActivated2(self, text):
        self.text11.setText(text)

    # width-size select
    def changesize1(self, value):
        if self.cb1.isChecked():
            self.combo2.hide()
            self.text13.show()
            self.cb2.setChecked(False)
            self.text2.setText(
                    "RunBundler --photos=" +
                    self.text4.displayText() +
                    " --featureExtractor=" +
                    self.text15.displayText() +
                    " --maxPhotoDimension=" +
                    self.text13.displayText())

    def changesize2(self, text):
        if self.cb2.isChecked():
            self.combo2.show()
            self.text13.hide()
            self.cb1.setChecked(False)
            self.text2.setText(
                "RunBundler --photos=" +
                self.text4.displayText() +
                " --featureExtractor=" +
                self.text15.displayText() +
                " --photoScalingFactor=" +
                self.text11.displayText())

    # help button 1 - select directory
    def on_help1_clicked(self):
        QMessageBox.information(
                self,
                "Help!",
                "Select the directory with original photos." +
                "Pictures have to be in JPG file format.",
                QMessageBox.Ok)

    # help button 2 - feature extractor
    def on_help2_clicked(self):
        QMessageBox.information(
                self,
                "Help!",
                "Select the feature extractor: VLFEAT or SIFT." +
                "\n\n - VLFEAT (http://www.vlfeat.org/) is released" +
                "under GPL v.2 license." +
                "\n\n - SIFT (http://www.cs.ubc.ca/~lowe/keypoints/) is" +
                "being made available for individual research use only." +
                "Any commercial use or any redistribution of this" +
                "software requires a license from the University of" +
                "British Columbia. Before use SIFT download and copy" +
                "the binary into the <software/sift-lowe> folder.",
                QMessageBox.Ok)

    # help button 3 - feature extractor
    def on_help3_clicked(self):
        QMessageBox.information(
                self,
                "Help!",
                "Copy of a photo will be scaled down if either width or" +
                "height exceeds the value insert in <maxPhotoDimension>." +
                "After scaling the maximum of width and height will be" +
                "equal to the value insert in <maxPhotoDimension>." +
                "\n\nDefault value is 1200: an image of 3008x2000 px" +
                "will be scale into a copy of 1200x798 px.",
                QMessageBox.Ok)

    # help button 4 - feature extractor
    def on_help4_clicked(self):
        QMessageBox.information(self,
                "Help!",
                "Scale all photos to the specified scaling factor:" +
                "\n\n 1 = original size \n\n 0.75 = 75% of" +
                "the original size \n\n 0.5 = half size" +
                "\n\n 0.25 = 25% of the original size.",
                QMessageBox.Ok)

    # connection path-command
    def onChangedpathbundler(self, text):
        if self.cb2.isChecked():
            self.text2.setText(
                    "RunBundler --photos=" +
                    self.text4.displayText() +
                    " --featureExtractor=" +
                    self.text15.displayText() +
                    "--photoScalingFactor=" +
                    self.text11.displayText())
        if self.cb1.isChecked():
            self.text2.setText(
                    "RunBundler --photos=" +
                    self.text4.displayText() +
                    " --featureExtractor=" +
                    self.text15.displayText() +
                    " --maxPhotoDimension=" +
                    self.text13.displayText())

    # connection extractor-command
    def onChangedextractor(self, text):
        if self.cb2.isChecked():
            self.text2.setText(
                    "RunBundler --photos=" +
                    self.text4.displayText() +
                    " --featureExtractor=" +
                    self.text15.displayText() +
                    " --photoScalingFactor=" +
                    self.text11.displayText())
        if self.cb1.isChecked():
            self.text2.setText(
                    "RunBundler --photos=" +
                    self.text4.displayText() +
                    " --featureExtractor=" +
                    self.text15.displayText() +
                    " --maxPhotoDimension="
                    + self.text13.displayText())

    # connection width-command
    def onChangedwidth(self, text):
        self.cb2.setChecked(False)
        self.cb1.setChecked(True)
        self.text2.setText(
                "RunBundler --photos=" +
                self.text4.displayText() +
                " --featureExtractor=" +
                self.text15.displayText() +
                " --maxPhotoDimension=" +
                self.text13.displayText())

    # connection size-command
    def onChangedsize(self, text):
        self.cb1.setChecked(False)
        self.cb2.setChecked(True)
        self.text2.setText(
                "RunBundler --photos=" +
                self.text4.displayText() +
                " --featureExtractor=" +
                self.text15.displayText() +
                " --photoScalingFactor=" +
                self.text11.displayText())

    # select directory with photos
    def showDialog2(self):
        directoryname = QFileDialog.getExistingDirectory(
                self,
                'Open directory with Bundler output files.',
                '/home')
        self.text3.setText(directoryname)

    # help button 5 - select directory
    def on_help5_clicked(self):
        QMessageBox.information(
                self,
                "Help!",
                "Select the Bundler output directory.",
                QMessageBox.Ok)

    # connection path-command
    def onChangedpathcmvs(self, text):
        self.text6.setText(
                "RunCMVS --bundlerOutputPath=" +
                self.text3.displayText() +
                " --ClusterToCompute=" +
                self.text5.displayText())

    # connection number cluster
    def onChangedcluster(self, text):
        self.text6.setText(
                "RunCMVS --bundlerOutputPath=" +
                self.text3.displayText() +
                " --ClusterToCompute="
                + self.text5.displayText())

    # help button 6 - cluster
    def on_help6_clicked(self):
        QMessageBox.information(
                self,
                "Help!",
                "Select the max number of photos for each cluster that" +
                "CMVS should compute. Separated PLY output files will be" +
                "created. \n\n - Depends on the CPUs of your computer:" +
                "if infinite loop occur, stop the process and try a" +
                "different value. \n\n - Default value is 10: an image" +
                "set with 28 photos will be compute in 3 separated" +
                "clusters.",
                QMessageBox.Ok)

    # open pmvs
    def openpmvs(self, text):
        if self.cb3.isChecked():
            self.button3.show()
            self.button6.show()
            self.text7.show()
            self.text8.show()
            self.label14.show()
            self.help_button7.show()
        else:
            self.label14.hide()
            self.button3.hide()
            self.button6.hide()
            self.text7.hide()
            self.text8.hide()
            self.help_button7.hide()

    # select directory with bundler output
    def showDialog3(self):
        directoryname = QFileDialog.getExistingDirectory(
                self,
                'Open directory with Bundler output files',
                '/home')
        self.text7.setText(directoryname)

    # connection path-command
    def onChangedpathpmvs(self, text):
        self.text8.setText(
                "RunPMVS --bundlerOutputPath=" +
                self.text7.displayText())

    #format text functions
    def format_out(self, array):
        """ Format standard output as Html """
        return unicode(array).replace("\n", "<br>")

    # QPROCESS signals
    """
    Multiple signals for the same thing...
    This is a violatation of the DRY principle / Only for test now
    Proper solution is to use heritage (QtTab... see docstring)

    on_start should toggle "Run" Button to "Cancel" and block access to
    others tabs?
    on_finish/on_error, invert toggle
    """
    def on_bundler_start(self):
        self.output1.insertHtml("<h4>Process has started...</h4><br>")

    def on_cmvs_start(self):
        self.output2.insertHtml("<h4>Process has started...</h4><br>")

    def on_pmvs_start(self):
        self.output3.insertHtml("<h4>Process has started...</h4><br>")

    def on_cam_start(self):
        self.output4.insertHtml("<h4>Process has started...</h4><br>")

    def on_bundler_out(self):
        self.output1.insertHtml(
                 self.format_out(procB.readAllStandardOutput()))
        self.scroll1.setValue(self.scroll1.maximum())

    def on_cmvs_out(self):
        self.output2.insertHtml(
                self.format_out(procC.readAllStandardOutput()))
        self.scroll2.setValue(self.scroll2.maximum())

    def on_pmvs_out(self):
        self.output3.insertHtml(
                self.format_out(procP.readAllStandardOutput()))
        self.scroll3.setValue(self.scroll3.maximum())

    def on_cam_out(self):
        out = unicode(procCam.readAllStandardOutput())
        if out.startswith("Type CCD width"):
            label = out.split(". Press")[0]
            ccd = list(QInputDialog.getDouble(
                self,
                "CCD width",
                label,
                0, 0, 3000, 1))
            arg = unicode(ccd[0]) + u"\n" if(ccd[1] and
                    ccd[0] != 0.0) else u"\n"
            procCam.write(arg)
        else:
            self.output4.insertHtml(self.format_out(out))
            self.scroll4.setValue(self.scroll4.maximum())


    def on_bundler_finish(self, status):
        self.output1.insertHtml("<h4>Process is finished!</h4><br><br>")

    def on_cmvs_finish(self, status):
        self.output2.insertHtml("<h4>Process is finished!</h4><br><br>")

    def on_pmvs_finish(self, status):
        self.output3.insertHtml("<h4>Process is finished!</h4><br><br>")

    def on_cam_finish(self, status):
        self.output4.insertHtml("<h4>Check is finished!</h4><br><br>")

    def kill_bundler_process(self):
        procB.terminate()
        procB.kill()
        # Need to disconnect to avoid multiple
        # start/ finish msg
        procB.disconnect(
                procB,
                QtCore.SIGNAL("started()"),
                self.on_bundler_start)
        procB.waitForFinished()
        procB.disconnect(
                procB,
                QtCore.SIGNAL("finished(int)"),
                self.on_bundler_finish)

    def kill_cmvs_process(self):
        procC.terminate()
        procC.kill()
        # Need to disconnect to avoid multiple
        # start/ finish msg
        procC.disconnect(
                procC,
                QtCore.SIGNAL("started()"),
                self.on_cmvs_start)
        procC.waitForFinished()
        procC.disconnect(
                procC,
                QtCore.SIGNAL("finished(int)"),
                self.on_cmvs_finish)

    def kill_pmvs_process(self):
        procP.terminate()
        procP.kill()
        # Need to disconnect to avoid multiple
        # start/ finish msg
        procP.disconnect(
                procP,
                QtCore.SIGNAL("started()"),
                self.on_pmvs_start)
        procP.waitForFinished()
        procP.disconnect(
                procP,
                QtCore.SIGNAL("finished(int)"),
                self.on_pmvs_finish)

    def kill_cam_process(self):
        procCam.terminate()
        procCam.kill()
        # Need to disconnect to avoid multiple
        # start/ finish msg
        procCam.disconnect(
                procCam,
                QtCore.SIGNAL("started()"),
                self.on_cam_start)
        procCam.waitForFinished()
        procCam.disconnect(
                procCam,
                QtCore.SIGNAL("finished(int)"),
                self.on_cam_finish)

    # Start bundler
    def startbundler(self):
        if procB.state() == QProcess.Running:
            self.kill_bundler_process()
        command = self.text2.displayText()
        procB.connect(
                procB,
                QtCore.SIGNAL("started()"),
                self.on_bundler_start)
        procB.connect(
                procB,
                QtCore.SIGNAL("finished(int)"),
                self.on_bundler_finish)
        procB.connect(
                procB,
                QtCore.SIGNAL("readyReadStandardOutput()"),
                self.on_bundler_out)
        procB.start(command)
        procB.waitForStarted()

    # Start cmvs
    def startcmvs(self):
        if procC.state() == QProcess.Running:
            self.kill_cmvs_process()
        command = self.text6.displayText()
        procC.connect(
                procC,
                QtCore.SIGNAL("started()"),
                self.on_cmvs_start)
        procC.connect(
                procC,
                QtCore.SIGNAL("finished(int)"),
                self.on_cmvs_finish)
        procC.connect(
                procC,
                QtCore.SIGNAL("readyReadStandardOutput()"),
                self.on_cmvs_out)
        procC.start(command)
        procC.waitForStarted()

    # Start pmvs
    def startpmvs(self):
        if procP.state() == QProcess.Running:
            self.kill_pmvs_process()
        command = self.text8.displayText()
        procP.connect(
                procP,
                QtCore.SIGNAL("started()"),
                self.on_pmvs_start)
        procP.connect(
                procP,
                QtCore.SIGNAL("finished(int)"),
                self.on_pmvs_finish)
        procP.connect(
                procP,
                QtCore.SIGNAL("readyReadStandardOutput()"),
                self.on_pmvs_out)
        procP.start(command)
        procP.waitForStarted()

    # select directory with photos (Camera Database)
    def showDialog4(self):
        directoryname = QFileDialog.getExistingDirectory(
                self,
                'Open directory with photos',
                '/home')
        self.text9.setText(directoryname)

# help button 9 - select directory
    def on_help9_clicked(self):
        QMessageBox.information(self,
                "Help!",
                "Select the directory with original photos. Pictures" +
                "have to be in JPG file format.\n\n - Press the RUN" +
                "button to check if the camera is already inside the" +
                "database.\n\n - If the camera is not correctly" +
                "saved, please insert in the windows the CCD width in mm",
                QMessageBox.Ok)

# connection path-command
    def onChangedpathcamdat(self, text):
        self.text10.setText(
                "RunBundler --photos=" +
                self.text9.displayText() +
                " --checkCameraDatabase")

# start Camera Database
    def startcamdat(self):
        self.kill_cam_process()
        command = self.text10.displayText()
        procCam.connect(
                procCam,
                QtCore.SIGNAL("started()"),
                self.on_cam_start)
        procCam.connect(
                procCam,
                QtCore.SIGNAL("finished(int)"),
                self.on_cam_finish)
        procCam.connect(
                procCam,
                QtCore.SIGNAL("readyReadStandardOutput()"),
                self.on_cam_out)
        procCam.start(command)
        procCam.waitForStarted()
