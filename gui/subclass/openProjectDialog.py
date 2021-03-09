# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'openprojectdialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDir

class Ui_openProjectDialog(object):
    def setupUi(self, openProjectDialog):
        openProjectDialog.setObjectName("openProjectDialog")
        openProjectDialog.resize(400, 300)

        self.verticalLayout = QtWidgets.QVBoxLayout(openProjectDialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pathLineEdit = QtWidgets.QLineEdit(openProjectDialog)
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.pathLineEdit.textChanged.connect(self.checkForOkEnable)
        self.horizontalLayout.addWidget(self.pathLineEdit)

        self.browsePushButton = QtWidgets.QPushButton(openProjectDialog)
        self.browsePushButton.setObjectName("browsePushButton")
        self.horizontalLayout.addWidget(self.browsePushButton)
        self.browsePushButton.clicked.connect(self.browseClicked)

        topSpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(topSpacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        bottomSpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(bottomSpacerItem)

        self.buttonBox = QtWidgets.QDialogButtonBox(openProjectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(openProjectDialog)
        self.buttonBox.accepted.connect(openProjectDialog.accept)
        self.buttonBox.rejected.connect(openProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(openProjectDialog)


    def retranslateUi(self, openProjectDialog):
        _translate = QtCore.QCoreApplication.translate
        openProjectDialog.setWindowTitle(_translate("openProjectDialog", "Open project"))
        self.browsePushButton.setText(_translate("openProjectDialog", "Browse..."))
        self.pathLineEdit.setPlaceholderText(_translate("pathLineEdit", "Enter the project path"))


    def checkForOkEnable(self):#checked
        if QDir(self.pathLineEdit.text()).exists():
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)


    def browseClicked(self):#checked
        projectPath = QtWidgets.QFileDialog.getExistingDirectory(self.verticalLayout.parentWidget(), "Project path", "/home")
        self.pathLineEdit.setText(projectPath)


    def getPathProject(self):#checked
        return self.pathLineEdit.text()


def getProjectPath(pWidget):#checked
    openProjectDialog = QtWidgets.QDialog(pWidget)
    uiOpenProjectDialog = Ui_openProjectDialog()
    uiOpenProjectDialog.setupUi(openProjectDialog)
    if openProjectDialog.exec_():
        return (uiOpenProjectDialog.getPathProject(),)
    else:
        return ()