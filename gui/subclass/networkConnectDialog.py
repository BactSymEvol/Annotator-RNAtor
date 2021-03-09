# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'networkconnectdialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_networkConnectDialog(object):
    def setupUi(self, networkConnectDialog):
        networkConnectDialog.setObjectName("networkConnectDialog")
        networkConnectDialog.resize(400, 300)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(networkConnectDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.informationVerticalLayout = QtWidgets.QVBoxLayout()
        self.informationVerticalLayout.setObjectName("informationVerticalLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.informationVerticalLayout.addItem(spacerItem)
        
        self.genomeDbRefComboBox = QtWidgets.QComboBox(networkConnectDialog)
        self.genomeDbRefComboBox.setObjectName("genomeDbRefComboBox")
        self.genomeDbRefComboBox.addItem("Unify locus tag according to a database genome.")
        self.genomeDbRefComboBox.addItem("_No_")
        self.genomeDbRefComboBox.currentTextChanged.connect(self.checkForOkEnable)
        self.informationVerticalLayout.addWidget(self.genomeDbRefComboBox)

        self.unifiedLocusTNameLineEdit = QtWidgets.QLineEdit(networkConnectDialog)
        self.unifiedLocusTNameLineEdit.setObjectName("unifiedLocusTNameLineEdit")
        self.unifiedLocusTNameLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("\w+")))
        self.unifiedLocusTNameLineEdit.textChanged.connect(self.checkForOkEnable)
        self.informationVerticalLayout.addWidget(self.unifiedLocusTNameLineEdit)

        self.similarityThresholdLineEdit = QtWidgets.QLineEdit(networkConnectDialog)
        self.similarityThresholdLineEdit.setObjectName("similarityThresholdLineEdit")
        self.similarityThresholdLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("(\d\d{0,1}|100)")))
        self.similarityThresholdLineEdit.textChanged.connect(self.checkForOkEnable)
        self.informationVerticalLayout.addWidget(self.similarityThresholdLineEdit)

        self.blastComboBox = QtWidgets.QComboBox(networkConnectDialog)
        self.blastComboBox.setObjectName("blastComboBox")
        self.blastComboBox.currentTextChanged.connect(self.checkForOkEnable)
        self.informationVerticalLayout.addWidget(self.blastComboBox)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.informationVerticalLayout.addItem(spacerItem1)

        self.verticalLayout_2.addLayout(self.informationVerticalLayout)

        self.buttonBox = QtWidgets.QDialogButtonBox(networkConnectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(networkConnectDialog)
        self.buttonBox.accepted.connect(networkConnectDialog.accept)
        self.buttonBox.rejected.connect(networkConnectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(networkConnectDialog)


    def retranslateUi(self, networkConnectDialog):
        _translate = QtCore.QCoreApplication.translate
        networkConnectDialog.setWindowTitle(_translate("networkConnectDialog", "Network connection"))
        self.unifiedLocusTNameLineEdit.setPlaceholderText(_translate("unifiedLocusTNameLineEdit", "Enter unified locus tag name."))
        self.similarityThresholdLineEdit.setPlaceholderText(_translate("unifiedLocusTNameLineEdit", "Enter similarity threshold."))
    
    
    def checkForOkEnable(self):
        if self.genomeDbRefComboBox.currentText() == "Unify locus tag according to a database genome." or\
            self.genomeDbRefComboBox.currentIndex() == 0 or\
                self.unifiedLocusTNameLineEdit.text() == "" or\
                    self.similarityThresholdLineEdit.text() == "" or\
                        self.blastComboBox.currentText() == "":
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)


    def getGenomeDerDbChoice(self):#checked1
        return self.genomeDbRefComboBox.currentText()


    def getUnifiedLTName(self):#checked1
        return self.unifiedLocusTNameLineEdit.text()


    def getSimilarityThreshold(self):#checked1
        return self.similarityThresholdLineEdit.text()

    
    def getDesiredBlast(self):#checked1
        return self.blastComboBox.currentText()


    def setBlastComboBox(self, blastPerformed):#checked1
        if blastPerformed["Blastn"]:
            self.blastComboBox.addItem("Blastn")
        if blastPerformed["Blastp"]:
            self.blastComboBox.addItem("Blastp")


    def setGenomeDbRefComboBox(self, genomeLocusDict, tickedGenomes):#checked1
        for genome in tickedGenomes:
            if genome in genomeLocusDict:
                self.genomeDbRefComboBox.addItem(genome + " - " + genomeLocusDict[genome])


def getNetworkInformation(pWidget, genomeLocusDict, blastTypeInfo, tickedGenomes):
    networkInformationDialog = QtWidgets.QDialog(pWidget)
    uiNetworkInformation = Ui_networkConnectDialog()
    uiNetworkInformation.setupUi(networkInformationDialog)
    uiNetworkInformation.setBlastComboBox(blastTypeInfo)
    uiNetworkInformation.setGenomeDbRefComboBox(genomeLocusDict, tickedGenomes)
    if networkInformationDialog.exec_():
        return (tickedGenomes, \
            uiNetworkInformation.getGenomeDerDbChoice(), \
                uiNetworkInformation.getUnifiedLTName(), \
                    float(uiNetworkInformation.getSimilarityThreshold()), \
                        uiNetworkInformation.getDesiredBlast())
    else:
        return ()

