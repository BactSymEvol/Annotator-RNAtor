# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'blastdialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_blastDialog(object):
    def setupUi(self, blastDialog):
        blastDialog.setObjectName("blastDialog")
        blastDialog.resize(400, 300)

        self.verticalLayout = QtWidgets.QVBoxLayout(blastDialog)
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.blastpRadioButton = QtWidgets.QRadioButton(blastDialog)
        self.blastpRadioButton.setChecked(QtCore.Qt.Checked)
        self.blastpRadioButton.setObjectName("blastpRadioButton")
        self.horizontalLayout.addWidget(self.blastpRadioButton)

        self.blastnRadioButton = QtWidgets.QRadioButton(blastDialog)
        self.blastnRadioButton.setObjectName("blastnRadioButton")
        self.horizontalLayout.addWidget(self.blastnRadioButton)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.buttonBox = QtWidgets.QDialogButtonBox(blastDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(blastDialog)
        self.buttonBox.accepted.connect(blastDialog.accept)
        self.buttonBox.rejected.connect(blastDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(blastDialog)

    def retranslateUi(self, blastDialog):
        _translate = QtCore.QCoreApplication.translate
        blastDialog.setWindowTitle(_translate("blastDialog", "Blast type"))
        self.blastpRadioButton.setText(_translate("blastDialog", "Blastp"))
        self.blastnRadioButton.setText(_translate("blastDialog", "Blastn"))


    def getCheckedBlast(self):
        if self.blastpRadioButton.isChecked():
            return "Blastp"
        else:
            return "Blastn"


def startBlastDialog(pWidget):
    blastDialog = QtWidgets.QDialog(pWidget)
    uiBlastDialog = Ui_blastDialog()
    uiBlastDialog.setupUi(blastDialog)
    if blastDialog.exec_():
        return (uiBlastDialog.getCheckedBlast(),)
    else:
        return ()