# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addfromcomputer.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFile


class Ui_addFromComputer(object):
    def setupUi(self, addFromComputer):
        addFromComputer.setObjectName("addFromComputer")
        addFromComputer.resize(400, 300)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(addFromComputer)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.ffnFileLayout = QtWidgets.QHBoxLayout()
        self.ffnFileLayout.setObjectName("ffnFileLayout")

        self.ffnFileLineEdit = QtWidgets.QLineEdit(addFromComputer)
        self.ffnFileLineEdit.setObjectName("ffnFileLineEdit")
        self.ffnFileLineEdit.textChanged.connect(self.checkForOkEnable)
        self.ffnFileLayout.addWidget(self.ffnFileLineEdit)

        self.ffnFilePushButton = QtWidgets.QPushButton(addFromComputer)
        self.ffnFilePushButton.setObjectName("ffnFilePushButton")
        self.ffnFileLayout.addWidget(self.ffnFilePushButton)
        self.ffnFilePushButton.clicked.connect(self.ffnFilePushButtonClicked)

        self.verticalLayout_2.addLayout(self.ffnFileLayout)

        self.fnaFileLayout = QtWidgets.QHBoxLayout()
        self.fnaFileLayout.setObjectName("fnaFileLayout")

        self.fnaFileLineEdit = QtWidgets.QLineEdit(addFromComputer)
        self.fnaFileLineEdit.setObjectName("fnaFileLineEdit")
        self.fnaFileLineEdit.textChanged.connect(self.checkForOkEnable)
        self.fnaFileLayout.addWidget(self.fnaFileLineEdit)

        self.fnaFilePushButton = QtWidgets.QPushButton(addFromComputer)
        self.fnaFilePushButton.setObjectName("fnaFilePushButton")
        self.fnaFileLayout.addWidget(self.fnaFilePushButton)
        self.fnaFilePushButton.clicked.connect(self.fnaFilePushButtonClicked)

        self.verticalLayout_2.addLayout(self.fnaFileLayout)

        self.faaFileLayout = QtWidgets.QHBoxLayout()
        self.faaFileLayout.setObjectName("faaFileLayout")

        self.faaFileLineEdit = QtWidgets.QLineEdit(addFromComputer)
        self.faaFileLineEdit.setObjectName("faaFileLineEdit")
        self.faaFileLineEdit.textChanged.connect(self.checkForOkEnable)
        self.faaFileLayout.addWidget(self.faaFileLineEdit)

        self.faaFilePushButton = QtWidgets.QPushButton(addFromComputer)
        self.faaFilePushButton.setObjectName("faaFilePushButton")
        self.faaFileLayout.addWidget(self.faaFilePushButton)
        self.faaFilePushButton.clicked.connect(self.faaFilePushButtonClicked)

        self.verticalLayout_2.addLayout(self.faaFileLayout)

        self.gffFileLayout = QtWidgets.QHBoxLayout()
        self.gffFileLayout.setObjectName("gffFileLayout")

        self.gffFileLineEdit = QtWidgets.QLineEdit(addFromComputer)
        self.gffFileLineEdit.setObjectName("gffFileLineEdit")
        self.gffFileLineEdit.textChanged.connect(self.checkForOkEnable)
        self.gffFileLayout.addWidget(self.gffFileLineEdit)

        self.gffFilePushButton = QtWidgets.QPushButton(addFromComputer)
        self.gffFilePushButton.setObjectName("gffFilePushButton")
        self.gffFileLayout.addWidget(self.gffFilePushButton)
        self.gffFilePushButton.clicked.connect(self.gffFilePushButtonClicked)

        self.verticalLayout_2.addLayout(self.gffFileLayout)

        self.featureTableFileLayout = QtWidgets.QHBoxLayout()
        self.featureTableFileLayout.setObjectName("featureTableFileLayout")

        self.featureTableFileLineEdit = QtWidgets.QLineEdit(addFromComputer)
        self.featureTableFileLineEdit.setObjectName("featureTableFileLineEdit")
        self.featureTableFileLineEdit.textChanged.connect(self.checkForOkEnable)
        self.featureTableFileLayout.addWidget(self.featureTableFileLineEdit)

        self.featureTableFilePushButton = QtWidgets.QPushButton(addFromComputer)
        self.featureTableFilePushButton.setObjectName("featureTableFilePushButton")
        self.featureTableFileLayout.addWidget(self.featureTableFilePushButton)
        self.featureTableFilePushButton.clicked.connect(self.featureTableFilePushButtonClicked)

        self.verticalLayout_2.addLayout(self.featureTableFileLayout)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)

        self.buttonBox = QtWidgets.QDialogButtonBox(addFromComputer)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(addFromComputer)
        self.buttonBox.accepted.connect(addFromComputer.accept)
        self.buttonBox.rejected.connect(addFromComputer.reject)
        QtCore.QMetaObject.connectSlotsByName(addFromComputer)


    def retranslateUi(self, addFromComputer):#checked
        _translate = QtCore.QCoreApplication.translate
        addFromComputer.setWindowTitle(_translate("addFromComputer", "Adding from computer"))
        self.ffnFilePushButton.setText(_translate("addFromComputer", "Browse..."))
        self.ffnFileLineEdit.setPlaceholderText(_translate("addFromComputer", "Choose the CDS from genomic file (ffn or fna)"))
        self.fnaFilePushButton.setText(_translate("addFromComputer", "Browse..."))
        self.fnaFileLineEdit.setPlaceholderText(_translate("addFromComputer", "Choose the genomic file (fna)"))
        self.faaFilePushButton.setText(_translate("addFromComputer", "Browse..."))
        self.faaFileLineEdit.setPlaceholderText(_translate("addFromComputer", "Choose the protein file (faa)"))
        self.gffFilePushButton.setText(_translate("addFromComputer", "Browse..."))
        self.gffFileLineEdit.setPlaceholderText(_translate("addFromComputer", "Choose the annotation file (gff)"))
        self.featureTableFilePushButton.setText(_translate("addFromComputer", "Browse..."))
        self.featureTableFileLineEdit.setPlaceholderText(_translate("addFromComputer", "Choose the feature table file (txt)"))


    def ffnFilePushButtonClicked(self):#checked
        ffnFilePath = QtWidgets.QFileDialog.getOpenFileName(self.verticalLayout_2.parentWidget(), \
            "CDS from genomic file", "/home", "Files (*.ffn *.fna)")
        self.ffnFileLineEdit.setText(ffnFilePath[0])


    def fnaFilePushButtonClicked(self):#checked
        fnaFilePath = QtWidgets.QFileDialog.getOpenFileName(self.verticalLayout_2.parentWidget(), \
            "Genomic file", "/home", "Files (*.fna)")
        self.fnaFileLineEdit.setText(fnaFilePath[0])


    def faaFilePushButtonClicked(self):#checked
        faaFilePath = QtWidgets.QFileDialog.getOpenFileName(self.verticalLayout_2.parentWidget(), \
            "Protein file", "/home", "Files (*.faa)")
        self.faaFileLineEdit.setText(faaFilePath[0])


    def gffFilePushButtonClicked(self):#checked
        gffFilePath = QtWidgets.QFileDialog.getOpenFileName(self.verticalLayout_2.parentWidget(), \
            "Annotation file", "/home", "Files (*.gff)")
        self.gffFileLineEdit.setText(gffFilePath[0])


    def featureTableFilePushButtonClicked(self):#checked
        featureTableFilePath = QtWidgets.QFileDialog.getOpenFileName(self.verticalLayout_2.parentWidget(), \
            "Feature table file", "/home", "Files (*.txt)")
        self.featureTableFileLineEdit.setText(featureTableFilePath[0])


    def checkForOkEnable(self):#checked
        if QFile.exists(self.ffnFileLineEdit.text()) and \
            QFile.exists(self.fnaFileLineEdit.text()) and \
                QFile.exists(self.faaFileLineEdit.text()) and \
                    QFile.exists(self.gffFileLineEdit.text()) and \
                        (QFile.exists(self.featureTableFileLineEdit.text()) or \
                            self.featureTableFileLineEdit.text() == ""):
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)


    def getFfnFilePath(self):#checked
        return self.ffnFileLineEdit.text()


    def getFnaFilePath(self):#checked
        return self.fnaFileLineEdit.text()


    def getFaaFilePath(self):#checked
        return self.faaFileLineEdit.text()    


    def getGffFilePath(self):#checked
        return self.gffFileLineEdit.text()


    def getFeatureTableFilePath(self):#checked
        return self.featureTableFileLineEdit.text()



def getGenomeFilesPath(pWidget):#checked
    genomeFilesDialog = QtWidgets.QDialog(pWidget)
    uiGenomeFilesDialog = Ui_addFromComputer()
    uiGenomeFilesDialog.setupUi(genomeFilesDialog)
    if genomeFilesDialog.exec_():
        if uiGenomeFilesDialog.getFeatureTableFilePath() == "":
            return (uiGenomeFilesDialog.getFfnFilePath(), uiGenomeFilesDialog.getFnaFilePath(), \
                uiGenomeFilesDialog.getFaaFilePath(), uiGenomeFilesDialog.getGffFilePath())
        else:
            return (uiGenomeFilesDialog.getFfnFilePath(), uiGenomeFilesDialog.getFnaFilePath(), \
                uiGenomeFilesDialog.getFaaFilePath(), uiGenomeFilesDialog.getGffFilePath(), \
                    uiGenomeFilesDialog.getFeatureTableFilePath())
    else:
        return ()