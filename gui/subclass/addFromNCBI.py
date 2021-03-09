# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addfromncbi.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addFromNCBI(object):
    def setupUi(self, addFromNCBI):#checked
        addFromNCBI.setObjectName("addFromNCBI")
        addFromNCBI.resize(400, 300)

        self.verticalLayout = QtWidgets.QVBoxLayout(addFromNCBI)
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.ftpLinkLineEdit = QtWidgets.QLineEdit(addFromNCBI)
        self.ftpLinkLineEdit.setObjectName("ftpLinkLineEdit")
        self.ftpLinkLineEdit.textChanged.connect(self.checkForOkEnable)
        self.verticalLayout.addWidget(self.ftpLinkLineEdit)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.buttonBox = QtWidgets.QDialogButtonBox(addFromNCBI)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(addFromNCBI)
        self.buttonBox.accepted.connect(addFromNCBI.accept)
        self.buttonBox.rejected.connect(addFromNCBI.reject)
        QtCore.QMetaObject.connectSlotsByName(addFromNCBI)


    def retranslateUi(self, addFromNCBI):#checked
        _translate = QtCore.QCoreApplication.translate
        addFromNCBI.setWindowTitle(_translate("addFromNCBI", "Adding from NCBI"))
        self.ftpLinkLineEdit.setPlaceholderText(_translate("addFromNCBI", "Paste the NCBI Genome ftp link"))


    def checkForOkEnable(self):#checked
        if self.ftpLinkLineEdit.text().startswith("ftp://ftp.ncbi.nlm.nih.gov/genomes"):
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)


    def getFtpLink(self):#checked
        return self.ftpLinkLineEdit.text()


def getGenomeURL(pWidget):#checked
    genomeURLDialog = QtWidgets.QDialog(pWidget)
    uiGenomeURLDialog = Ui_addFromNCBI()
    uiGenomeURLDialog.setupUi(genomeURLDialog)
    if genomeURLDialog.exec_():
        return (uiGenomeURLDialog.getFtpLink(),)
    else:
        return ()
