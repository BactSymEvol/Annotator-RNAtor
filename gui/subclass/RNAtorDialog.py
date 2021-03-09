# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rnatordialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo

class Ui_RNAtorDialog(object):
    def setupUi(self, RNAtorDialog, genomeName):
        RNAtorDialog.setObjectName("RNAtorDialog")
        RNAtorDialog.resize(400, 300)

        self.verticalLayout = QtWidgets.QVBoxLayout(RNAtorDialog)
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.r1HorizontalLayout = QtWidgets.QHBoxLayout()
        self.r1HorizontalLayout.setObjectName("r1HorizontalLayout")

        self.r1LineEdit = QtWidgets.QLineEdit(RNAtorDialog)
        self.r1LineEdit.setObjectName("r1LineEdit")
        self.r1LineEdit.textChanged.connect(self.checkForOkEnable)
        self.r1HorizontalLayout.addWidget(self.r1LineEdit)

        self.r1PushButton = QtWidgets.QPushButton(RNAtorDialog)
        self.r1PushButton.setObjectName("r1PushButton")
        self.r1HorizontalLayout.addWidget(self.r1PushButton)
        self.r1PushButton.clicked.connect(self.r1BrowseClicked)

        self.verticalLayout.addLayout(self.r1HorizontalLayout)

        self.r2HorizontalLayout = QtWidgets.QHBoxLayout()
        self.r2HorizontalLayout.setObjectName("r2HorizontalLayout")

        self.r2LineEdit = QtWidgets.QLineEdit(RNAtorDialog)
        self.r2LineEdit.setObjectName("r2LineEdit")
        self.r2LineEdit.textChanged.connect(self.checkForOkEnable)
        self.r2HorizontalLayout.addWidget(self.r2LineEdit)

        self.r2PushButton = QtWidgets.QPushButton(RNAtorDialog)
        self.r2PushButton.setObjectName("r2PushButton")
        self.r2HorizontalLayout.addWidget(self.r2PushButton)
        self.r2PushButton.clicked.connect(self.r2BrowseClicked)

        self.verticalLayout.addLayout(self.r2HorizontalLayout)

        self.genomeHorizontalLayout = QtWidgets.QHBoxLayout()
        self.genomeHorizontalLayout.setObjectName("genomeHorizontalLayout")

        self.genomeLineEdit = QtWidgets.QLineEdit(RNAtorDialog)
        self.genomeLineEdit.setObjectName("genomeLineEdit")
        self.genomeLineEdit.textChanged.connect(self.checkForOkEnable)
        self.genomeHorizontalLayout.addWidget(self.genomeLineEdit)

        self.genomePushButton = QtWidgets.QPushButton(RNAtorDialog)
        self.genomePushButton.setObjectName("genomePushButton")
        self.genomeHorizontalLayout.addWidget(self.genomePushButton)
        self.genomePushButton.clicked.connect(self.genomeBrowseClicked)

        self.verticalLayout.addLayout(self.genomeHorizontalLayout)

        self.gtfHorizontalLayout = QtWidgets.QHBoxLayout()
        self.gtfHorizontalLayout.setObjectName("gtfHorizontalLayout")

        self.gtfLineEdit = QtWidgets.QLineEdit(RNAtorDialog)
        self.gtfLineEdit.setObjectName("gtfLineEdit")
        self.gtfLineEdit.textChanged.connect(self.checkForOkEnable)
        self.gtfHorizontalLayout.addWidget(self.gtfLineEdit)

        self.gtfPushButton = QtWidgets.QPushButton(RNAtorDialog)
        self.gtfPushButton.setObjectName("gtfPushButton")
        self.gtfHorizontalLayout.addWidget(self.gtfPushButton)
        self.gtfPushButton.clicked.connect(self.gtfBrowseClicked)

        self.verticalLayout.addLayout(self.gtfHorizontalLayout)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.buttonBox = QtWidgets.QDialogButtonBox(RNAtorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RNAtorDialog, genomeName)
        self.buttonBox.accepted.connect(RNAtorDialog.accept)
        self.buttonBox.rejected.connect(RNAtorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RNAtorDialog)


    def retranslateUi(self, RNAtorDialog, genomeName):
        _translate = QtCore.QCoreApplication.translate
        RNAtorDialog.setWindowTitle(_translate("RNAtorDialog", genomeName))
        self.r1PushButton.setText(_translate("RNAtorDialog", "Browse..."))
        self.r1LineEdit.setPlaceholderText(_translate("RNAtorDialog", "Enter r1 RNAseq file path (fastq)"))
        self.r2PushButton.setText(_translate("RNAtorDialog", "Browse..."))
        self.r2LineEdit.setPlaceholderText(_translate("RNAtorDialog", "Enter r2 RNAseq file path (fastq)"))
        self.genomePushButton.setText(_translate("RNAtorDialog", "Browse..."))
        self.genomeLineEdit.setPlaceholderText(_translate("RNAtorDialog", "Enter genome file path (fna)"))
        self.gtfPushButton.setText(_translate("RNAtorDialog", "Browse..."))
        self.gtfLineEdit.setPlaceholderText(_translate("RNAtorDialog", "Enter annotation file path (GTF)"))
        

    def r1BrowseClicked(self):#checked1
        featureTableFilePath = QtWidgets.QFileDialog.getOpenFileName(
            self.verticalLayout.parentWidget(), 
                "r1 RNAseq file", "/home", "Files (*.fastq)")
        self.r1LineEdit.setText(featureTableFilePath[0])


    def r2BrowseClicked(self):#checked1
        featureTableFilePath = QtWidgets.QFileDialog.getOpenFileName(
            self.verticalLayout.parentWidget(), 
                "r2 RNAseq file", "/home", "Files (*.fastq)")
        self.r2LineEdit.setText(featureTableFilePath[0])

    
    def genomeBrowseClicked(self):#checked1
        featureTableFilePath = QtWidgets.QFileDialog.getOpenFileName(
            self.verticalLayout.parentWidget(), 
                "Genome file", "/home", "Files (*.fna)")
        self.genomeLineEdit.setText(featureTableFilePath[0])


    def gtfBrowseClicked(self):#checked1
        featureTableFilePath = QtWidgets.QFileDialog.getOpenFileName(
            self.verticalLayout.parentWidget(), 
                "GTF file", "/home", "Files (*.gtf)")
        self.gtfLineEdit.setText(featureTableFilePath[0])


    def checkForOkEnable(self):#checked1
        if QFileInfo(self.r1LineEdit.text()).isFile() and \
            QFileInfo(self.r2LineEdit.text()).isFile() and \
                QFileInfo(self.genomeLineEdit.text()).isFile() and \
                    QFileInfo(self.gtfLineEdit.text()).isFile():
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
    

    def getR1Path(self):#checked1
        return self.r1LineEdit.text()
    

    def getR2Path(self):#checked1
        return self.r2LineEdit.text()

    
    def getGenomePath(self):#checked1
        return self.genomeLineEdit.text()

    
    def getGTFPath(self):#checked1
        return self.gtfLineEdit.text()


def getRNAtorInformation(pWidget, genomeName):
    RNAtorDialog = QtWidgets.QDialog(pWidget)
    uiRNAtorDialog = Ui_RNAtorDialog()
    uiRNAtorDialog.setupUi(RNAtorDialog, genomeName)
    if RNAtorDialog.exec_() :
        return (uiRNAtorDialog.getR1Path(), uiRNAtorDialog.getR2Path(), uiRNAtorDialog.getGenomePath(), uiRNAtorDialog.getGTFPath())
    else:
        return 0