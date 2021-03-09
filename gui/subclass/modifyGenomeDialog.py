# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modifyGenomeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFile

class Ui_modifyGenomeDialog(object):
    def setupUi(self, Dialog, genometPath):
        """-------------------------------------------------"""
        #self.projectPath = projectPath
        """-------------------------------------------------"""
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.gffPushButton = QtWidgets.QPushButton(Dialog)
        self.gffPushButton.setObjectName("gffPushButton")
        self.gffPushButton.clicked.connect(self.gffClicked)
        self.gridLayout.addWidget(self.gffPushButton, 5, 1, 1, 1)
        
        self.fnaPushButton = QtWidgets.QPushButton(Dialog)
        self.fnaPushButton.setObjectName("fnaPushButton")
        self.fnaPushButton.clicked.connect(self.fnaClicked)
        self.gridLayout.addWidget(self.fnaPushButton, 3, 1, 1, 1)

        self.ffnPushButton = QtWidgets.QPushButton(Dialog)
        self.ffnPushButton.setObjectName("ffnPushButton")
        self.ffnPushButton.clicked.connect(self.ffnClicked)
        self.gridLayout.addWidget(self.ffnPushButton, 2, 1, 1, 1)

        self.fnaLineEdit = QtWidgets.QLineEdit(Dialog)
        self.fnaLineEdit.setObjectName("fnaLineEdit")
        self.fnaLineEdit.textChanged.connect(self.checkForOkEnable)
        self.gridLayout.addWidget(self.fnaLineEdit, 3, 0, 1, 1)

        self.faaPushButton = QtWidgets.QPushButton(Dialog)
        self.faaPushButton.setObjectName("faaPushButton")
        self.faaPushButton.clicked.connect(self.faaClicked)
        self.gridLayout.addWidget(self.faaPushButton, 4, 1, 1, 1)

        self.featureTabPushButton = QtWidgets.QPushButton(Dialog)
        self.featureTabPushButton.setObjectName("featureTabPushButton")
        self.featureTabPushButton.clicked.connect(self.featureTabClicked)
        self.gridLayout.addWidget(self.featureTabPushButton, 6, 1, 1, 1)

        self.faaLineEdit = QtWidgets.QLineEdit(Dialog)
        self.faaLineEdit.setObjectName("faaLineEdit")
        self.faaLineEdit.textChanged.connect(self.checkForOkEnable)
        self.gridLayout.addWidget(self.faaLineEdit, 4, 0, 1, 1)

        self.ffnLineEdit = QtWidgets.QLineEdit(Dialog)
        self.ffnLineEdit.setObjectName("ffnLineEdit")
        self.ffnLineEdit.textChanged.connect(self.checkForOkEnable)
        self.gridLayout.addWidget(self.ffnLineEdit, 2, 0, 1, 1)

        self.gffLineEdit = QtWidgets.QLineEdit(Dialog)
        self.gffLineEdit.setObjectName("gffLineEdit")
        self.gffLineEdit.textChanged.connect(self.checkForOkEnable)
        self.gridLayout.addWidget(self.gffLineEdit, 5, 0, 1, 1)

        self.featureTabLineEdit = QtWidgets.QLineEdit(Dialog)
        self.featureTabLineEdit.setObjectName("featureTabLineEdit")
        self.featureTabLineEdit.textChanged.connect(self.checkForOkEnable)
        self.gridLayout.addWidget(self.featureTabLineEdit, 6, 0, 1, 1)
        
        self.verticalLayout.addLayout(self.gridLayout)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog, genometPath)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, genometPath):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "%s" %(genometPath.split("/")[-1])))
        self.gffPushButton.setText(_translate("Dialog", "Browse..."))
        self.gffLineEdit.setPlaceholderText(_translate("Dialog", "Choose the annotation file (gff)"))
        self.gffLineEdit.setText(_translate("Dialog", "%s/GFF/%s.gff" %(genometPath, genometPath.split("/")[-1])))
        self.fnaPushButton.setText(_translate("Dialog", "Browse..."))
        self.fnaLineEdit.setPlaceholderText(_translate("Dialog", "Choose the genomic file (fna)"))
        self.fnaLineEdit.setText(_translate("Dialog", "%s/FNA/%s.fna" %(genometPath, genometPath.split("/")[-1])))
        self.ffnPushButton.setText(_translate("Dialog", "Browse..."))
        self.ffnLineEdit.setPlaceholderText(_translate("Dialog", "Choose the CDS from genomic file (ffn or fna)"))
        self.ffnLineEdit.setText(_translate("Dialog", "%s/FFN/%s.ffn" %(genometPath, genometPath.split("/")[-1])))
        self.faaPushButton.setText(_translate("Dialog", "Browse..."))
        self.faaLineEdit.setPlaceholderText(_translate("Dialog", "Choose the protein file (faa)"))
        self.faaLineEdit.setText(_translate("Dialog", "%s/FAA/%s.faa" %(genometPath, genometPath.split("/")[-1])))
        self.featureTabPushButton.setText(_translate("Dialog", "Browse..."))
        self.featureTabLineEdit.setPlaceholderText(_translate("Dialog", "Choose the feature table file (txt)"))
        self.featureTabLineEdit.setText(_translate("Dialog", "%s/FeatureTable/%s.txt" %(genometPath, genometPath.split("/")[-1])))


    def gffClicked(self):#checked1
        newGffFile = QtWidgets.QFileDialog.getOpenFileName(self.verticalLayout.parentWidget(), \
            "%s: GFF file" %(self.gffLineEdit.text().split("/")[-1][:-4]), \
            "%s" %(self.gffLineEdit.text()), "Files (*.gff)")
        if newGffFile[0]:
            self.gffLineEdit.setText(newGffFile[0])

        
    def fnaClicked(self):#checked1
        newFnaFile = QtWidgets.QFileDialog.getOpenFileName(self.verticalLayout.parentWidget(), \
            "%s: FNA file" %(self.gffLineEdit.text().split("/")[-1][:-4]), \
            "%s" %(self.fnaLineEdit.text()), "Files (*.fna)")
        if newFnaFile[0]:
            self.fnaLineEdit.setText(newFnaFile[0])

    
    def ffnClicked(self):#checked1
        newFfnFile = QtWidgets.QFileDialog.getOpenFileName(self.verticalLayout.parentWidget(), \
            "%s: FFN file" %(self.gffLineEdit.text().split("/")[-1][:-4]), \
            "%s" %(self.ffnLineEdit.text()), "Files (*.ffn *.fna)")
        if newFfnFile[0]:
            self.ffnLineEdit.setText(newFfnFile[0])


    def faaClicked(self):#checked1
        newFaaFile = QtWidgets.QFileDialog.getOpenFileName(self.verticalLayout.parentWidget(), \
            "%s: FAA file" %(self.gffLineEdit.text().split("/")[-1][:-4]), \
            "%s" %(self.faaLineEdit.text()), "Files (*.faa)")
        if newFaaFile[0]:
            self.faaLineEdit.setText(newFaaFile[0])

    
    def featureTabClicked(self):#checked1
        newFeatureTabFile = QtWidgets.QFileDialog.getOpenFileName(self.verticalLayout.parentWidget(), \
            "%s: feature table file" %(self.gffLineEdit.text().split("/")[-1][:-4]), \
            "%s" %(self.featureTabLineEdit.text()), "Files (*.txt)")
        if newFeatureTabFile[0]:
            self.featureTabLineEdit.setText(newFeatureTabFile[0])

    
    def checkForOkEnable(self):#checked1
        if QFile.exists(self.gffLineEdit.text()) and \
            QFile.exists(self.fnaLineEdit.text()) and \
                QFile.exists(self.ffnLineEdit.text()) and \
                    QFile.exists(self.faaLineEdit.text()) and \
                        QFile.exists(self.featureTabLineEdit.text()):
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)


    def getFilesPath(self):#checked1
        return (self.ffnLineEdit.text(), self.fnaLineEdit.text(), self.faaLineEdit.text(), self.gffLineEdit.text(), self.featureTabLineEdit.text())



def startModifyGenomeDialog(pWidget, genometPath):#checked1
    modifyGenomeDialog = QtWidgets.QDialog(pWidget)
    uiModifyGenome = Ui_modifyGenomeDialog()
    uiModifyGenome.setupUi(modifyGenomeDialog, genometPath)
    if modifyGenomeDialog.exec_():
        return uiModifyGenome.getFilesPath()
    else:
        return ()