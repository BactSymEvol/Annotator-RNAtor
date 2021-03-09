# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addGenomeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!

from lib.models.project import Project
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddGenomeDialog(object):
    def setupUi(self, addGenomeDialog):
        addGenomeDialog.setObjectName("addGenomeDialog")
        addGenomeDialog.resize(400, 300)
        
        self.verticalLayout = QtWidgets.QVBoxLayout(addGenomeDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        self.genomeNameLineEdit = QtWidgets.QLineEdit(addGenomeDialog)
        self.genomeNameLineEdit.setObjectName("genomeNameLineEdit")
        self.genomeNameLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[^/; ]+")))
        self.genomeNameLineEdit.textChanged.connect(self.enableButtons)
        self.verticalLayout.addWidget(self.genomeNameLineEdit)
        
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
      
        self.buttonBox = QtWidgets.QDialogButtonBox(addGenomeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.addButton(QtWidgets.QDialogButtonBox.Cancel)        
       
        self.addFilesFromComputerPushButton = QtWidgets.QPushButton(addGenomeDialog)
        self.addFilesFromComputerPushButton.setObjectName("addFilesFromComputerPushButton")
        self.addFilesFromComputerPushButton.setEnabled(False)
        self.buttonBox.addButton(self.addFilesFromComputerPushButton, QtWidgets.QDialogButtonBox.ActionRole)

        self.addFilesFromNcbiPushButton = QtWidgets.QPushButton(addGenomeDialog)
        self.addFilesFromNcbiPushButton.setObjectName("addFilesFromNcbiPushButton")
        self.addFilesFromNcbiPushButton.setEnabled(False)
        self.buttonBox.addButton(self.addFilesFromNcbiPushButton, QtWidgets.QDialogButtonBox.ActionRole)

        self.buttonBox.rejected.connect(addGenomeDialog.reject)
        self.addFilesFromComputerPushButton.clicked.connect(self.addFromComputerClicked)
        self.addFilesFromNcbiPushButton.clicked.connect(self.addFromNCBIClicked)

        self.retranslateUi(addGenomeDialog)

        
        QtCore.QMetaObject.connectSlotsByName(addGenomeDialog)


    def retranslateUi(self, addGenomeDialog):
        _translate = QtCore.QCoreApplication.translate
        addGenomeDialog.setWindowTitle(_translate("addGenomeDialog", "Add Genome"))
        self.genomeNameLineEdit.setPlaceholderText(_translate("genomeNameLineEdit", "Enter your genome name"))
        self.addFilesFromNcbiPushButton.setText(_translate("addGenomeDialog", "Add From NCBI"))
        self.addFilesFromComputerPushButton.setText(_translate("addGenomeDialog", "Add From Computer"))


    def enableButtons(self):#checked
        if len(self.genomeNameLineEdit.text()) > 0:
            self.addFilesFromComputerPushButton.setEnabled(True)
            self.addFilesFromNcbiPushButton.setEnabled(True)
        else:
            self.addFilesFromComputerPushButton.setEnabled(False)
            self.addFilesFromNcbiPushButton.setEnabled(False)


    def addFromComputerClicked(self):#checked
        self.verticalLayout.parentWidget().done(2)


    def addFromNCBIClicked(self):#checked
        self.verticalLayout.parentWidget().done(3)


    def getGenomeName(self):#checked
        return self.genomeNameLineEdit.text()


def getGenomeInformation(pWidget):#checked
    addProjectDialog = QtWidgets.QDialog(pWidget)
    uiAddProjectDialog = Ui_AddGenomeDialog()
    uiAddProjectDialog.setupUi(addProjectDialog)
    signal = addProjectDialog.exec_()
    return (signal, uiAddProjectDialog.getGenomeName())


        