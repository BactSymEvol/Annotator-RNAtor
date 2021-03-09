# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newProjectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QDir

class Ui_NewProjectDialog(object):
    def setupUi(self, newProjectDialog):#checked
        newProjectDialog.setObjectName("newProjectDialog")
        newProjectDialog.resize(400, 300)

        self.gridLayout = QtWidgets.QGridLayout(newProjectDialog)
        self.gridLayout.setObjectName("gridLayout")

        self.buttonBox = QtWidgets.QDialogButtonBox(newProjectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)

        self.pathPushButton = QtWidgets.QPushButton(newProjectDialog)
        self.pathPushButton.setObjectName("pathPushButton")
        self.gridLayout.addWidget(self.pathPushButton, 1, 1, 1, 1)
        self.pathPushButton.clicked.connect(self.browseClicked)

        self.projectNameLineEdit = QtWidgets.QLineEdit(newProjectDialog)
        self.projectNameLineEdit.setObjectName("projectNameLineEdit")
        self.projectNameLineEdit.setEnabled(False)
        self.projectNameLineEdit.textChanged.connect(self.checkForOkEnable)
        self.gridLayout.addWidget(self.projectNameLineEdit, 2, 0, 1, 2)

        self.pathLineEdit = QtWidgets.QLineEdit(newProjectDialog)
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.pathLineEdit.textChanged.connect(self.checkForPNLEEnable)
        self.gridLayout.addWidget(self.pathLineEdit, 1, 0, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        

        self.retranslateUi(newProjectDialog)
        self.buttonBox.accepted.connect(newProjectDialog.accept)
        self.buttonBox.rejected.connect(newProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(newProjectDialog)


    def retranslateUi(self, newProjectDialog):#checked
        _translate = QtCore.QCoreApplication.translate
        self.projectNameLineEdit.setPlaceholderText(_translate("projectNameLineEdit", "Enter your project name"))
        self.pathLineEdit.setPlaceholderText(_translate("pathLineEdit", "Choose your project location"))
        newProjectDialog.setWindowTitle(_translate("newProjectDialog", "Project Creation"))
        self.pathPushButton.setText(_translate("newProjectDialog", "Browse..."))


    def browseClicked(self):#checked
        projectDirectory = QtWidgets.QFileDialog.getExistingDirectory(self.gridLayout.parentWidget(), "Choose project directory", "/home")
        self.pathLineEdit.setText(projectDirectory)


    def checkForPNLEEnable(self):#checked
        if QDir(self.pathLineEdit.text()).exists():
            self.projectNameLineEdit.setEnabled(True)
            if self.projectNameLineEdit.text() == "":
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
            else:
                self.checkForOkEnable()
        else:
            self.projectNameLineEdit.setEnabled(False)
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)


    def checkForOkEnable(self):#checked
        if not QDir(self.pathLineEdit.text()).exists(self.projectNameLineEdit.text()) and\
            self.projectNameLineEdit.isEnabled():
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)


    def getProjectPath(self):#checked
        return ("%s/%s" %(self.pathLineEdit.text(), self.projectNameLineEdit.text()), )


def getProjectInformation(pWidget):#checked
    newProjectDialog = QtWidgets.QDialog(pWidget)
    uiNewProjectDialog = Ui_NewProjectDialog()
    uiNewProjectDialog.setupUi(newProjectDialog)
    if newProjectDialog.exec_():
        return uiNewProjectDialog.getProjectPath()
    else:
        return ()

