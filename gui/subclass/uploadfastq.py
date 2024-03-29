# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo
import os
import fnmatch
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.AutomaticButton = QtWidgets.QPushButton(Dialog)
        self.AutomaticButton.setGeometry(QtCore.QRect(110, 110, 161, 31))
        self.AutomaticButton.setObjectName("AutomaticButton")
        self.AutomaticButton.clicked.connect(self.Automatic)
        self.ManualButton = QtWidgets.QPushButton(Dialog)
        self.ManualButton.setGeometry(QtCore.QRect(110, 160, 161, 31))
        self.ManualButton.setObjectName("ManualButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 50, 301, 31))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.AutomaticButton.setText(_translate("Dialog", "Automatic Upload"))
        self.AutomaticButton.clicked.connect(lambda: self.Automatic())
        self.ManualButton.setText(_translate("Dialog", "Manual Upload"))
        self.label.setText(_translate("Dialog", "Upload r1.fastq, r2.fastq, .gtf and .fna files "))

    def Automatic(self):#checked1
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Choose Directory', directory=os.getcwd())
        for root, dirnames, filenames in os.walk(folderpath):
            for filename in fnmatch.filter(filenames,'*.txt'):
                print(filename)
'''
def getInfo(Dialog):
    Dialog = QtWidgets.QDialog()
    uiDialog = Ui_Dialog()
    uiDialog.setupUi(Dialog)
    if Dialog.exec_() :
        return (uiDialog.Automatic())

    else:
        return 0
'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
        