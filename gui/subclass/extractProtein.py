# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'extractproteinname.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ExtractSeq(object):
    def setupUi(self, ExtractSeq):
        ExtractSeq.setObjectName("ExtractSeq")
        ExtractSeq.resize(479, 360)
        self.buttonBox = QtWidgets.QDialogButtonBox(ExtractSeq)
        self.buttonBox.setGeometry(QtCore.QRect(20, 290, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(ExtractSeq)
        self.lineEdit.setGeometry(QtCore.QRect(30, 40, 331, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.ProteinId = QtWidgets.QTextEdit(ExtractSeq)
        self.ProteinId.setGeometry(QtCore.QRect(30, 80, 331, 81))
        self.ProteinId.setObjectName("ProteinId")
        #self.ExtractAll = QtWidgets.QPushButton(ExtractSeq)
        #self.ExtractAll.setGeometry(QtCore.QRect(90, 230, 211, 31))
        #self.ExtractAll.setObjectName("ExtractAll")
        self.GHButton = QtWidgets.QRadioButton(ExtractSeq)
        self.GHButton.setGeometry(QtCore.QRect(30, 180, 161, 23))
        self.GHButton.setObjectName("GHButton")
        self.NXButton = QtWidgets.QRadioButton(ExtractSeq)
        self.NXButton.setGeometry(QtCore.QRect(210, 180, 112, 23))
        self.NXButton.setObjectName("NXButton")

        self.retranslateUi(ExtractSeq)
        self.buttonBox.accepted.connect(ExtractSeq.accept) # type: ignore
        self.buttonBox.rejected.connect(ExtractSeq.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ExtractSeq)

    def retranslateUi(self, ExtractSeq):
        _translate = QtCore.QCoreApplication.translate
        ExtractSeq.setWindowTitle(_translate("ExtractSeq", "Dialog"))
        self.lineEdit.setPlaceholderText(_translate("ExtractSeq", "Enter genome name"))
        self.ProteinId.setPlaceholderText(_translate("ExtractSeq", "Enter Protein Ids to extract. One Id each line"))
       # self.ExtractAll.setText(_translate("ExtractSeq", "Extract sequence"))
        self.GHButton.setText(_translate("ExtractSeq", "GET_HOMOLOGUES"))
        self.NXButton.setText(_translate("ExtractSeq", "NetworkX"))


    def getGenomeName(self):
        return self.lineEdit.text()
    

    def getProteinIds(self):
        myID =  self.ProteinId.toPlainText()
        return myID
    
    def getMethod(self):
        if self.GHButton.isChecked():
            return "GH"
        else:
            return "NX"

def extractProteinSeq():
    Data = QtWidgets.QDialog()
    ui = Ui_ExtractSeq()
    ui.setupUi(Data)
    if Data.exec_():
        return (ui.getGenomeName(), ui.getProteinIds(), ui.getMethod())
    else:
        return ()
