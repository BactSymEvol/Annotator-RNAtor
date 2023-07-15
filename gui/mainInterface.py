#!/bin/python3

from ast import IsNot
from numpy import sort
from lib.controller import Controller
from lib.models.project import Project
import subprocess, time

from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QProgressDialog
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, controller, app):

        """--------------------------------------------------------"""
        self.controller = controller
        """--------------------------------------------------------"""
        
        app.aboutToQuit.connect(self.controller.stopWorkerThread)
        
        MainWindow.setWindowIcon(QtGui.QIcon("./gui/pictures/appIcon.png"))
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)

        screenG = QtWidgets.QApplication.desktop().screenGeometry()
        x = (screenG.width()-MainWindow.width())/2
        y = (screenG.height()-MainWindow.height())/2
        MainWindow.move(800, 500)

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)
        self.completThreadsLayout = QtWidgets.QHBoxLayout()
        self.completThreadsLayout.setSpacing(6)
        self.completThreadsLayout.setObjectName("completThreadsLayout")

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.completThreadsLayout.addItem(spacerItem1)

        self.threadsLayout = QtWidgets.QHBoxLayout()
        self.threadsLayout.setSpacing(6)
        self.threadsLayout.setObjectName("threadsLayout")

        self.numberThreadsLabel = QtWidgets.QLabel(self.centralWidget)
        self.numberThreadsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.numberThreadsLabel.setObjectName("numberThreadsLabel")
        self.threadsLayout.addWidget(self.numberThreadsLabel)

        self.threadsSpinBox = QtWidgets.QSpinBox(self.centralWidget)
        self.threadsSpinBox.setMinimum(1)
        self.threadsSpinBox.setMaximum(self.getThreadsNumberFromOS())
        self.threadsSpinBox.setValue(self.threadsSpinBox.maximum())
        self.threadsSpinBox.setObjectName("threadsSpinBox")
        self.threadsLayout.addWidget(self.threadsSpinBox)

        self.completThreadsLayout.addLayout(self.threadsLayout)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.completThreadsLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.completThreadsLayout, 3, 1, 2, 1)

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 0, 1, 1, 1)

        self.completButtonsLayout = QtWidgets.QHBoxLayout()
        self.completButtonsLayout.setSpacing(6)
        self.completButtonsLayout.setObjectName("completButtonsLayout")

        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.completButtonsLayout.addItem(spacerItem5)
        self.buttonsLayout = QtWidgets.QVBoxLayout()
        self.buttonsLayout.setSpacing(6)
        self.buttonsLayout.setObjectName("buttonsLayout")
        
        self.addGenomeButton = QtWidgets.QPushButton(self.centralWidget)
        self.addGenomeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addGenomeButton.setAutoDefault(True)
        self.addGenomeButton.setObjectName("addGenomeButton")
        self.buttonsLayout.addWidget(self.addGenomeButton)
        self.addGenomeButton.clicked.connect(self.addGenomeClicked)

        self.addMultipleGenomeButton = QtWidgets.QPushButton(self.centralWidget)
        self.addMultipleGenomeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addMultipleGenomeButton.setAutoDefault(True)
        self.addMultipleGenomeButton.setObjectName("addMultipleGenomeButton")
        self.addMultipleGenomeButton.clicked.connect(self.addMultipleGenomeClicked)
        self.buttonsLayout.addWidget(self.addMultipleGenomeButton)

        self.addAnnotateFolderButton = QtWidgets.QPushButton(self.centralWidget)
        self.addAnnotateFolderButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addAnnotateFolderButton.setAutoDefault(True)
        self.addAnnotateFolderButton.setObjectName("addMultipleGenomeButton")
        self.addAnnotateFolderButton.clicked.connect(self.addannotate)
        self.buttonsLayout.addWidget(self.addAnnotateFolderButton)

        self.deleteTickedGenomeButton = QtWidgets.QPushButton(self.centralWidget)
        self.deleteTickedGenomeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deleteTickedGenomeButton.setAutoDefault(True)
        self.deleteTickedGenomeButton.setObjectName("deleteTickedGenomeButton")
        self.deleteTickedGenomeButton.clicked.connect(self.deleteGenomeClicked)
        self.buttonsLayout.addWidget(self.deleteTickedGenomeButton)

        self.modifyTickedGenomeButton = QtWidgets.QPushButton(self.centralWidget)
        self.modifyTickedGenomeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.modifyTickedGenomeButton.setAutoDefault(True)
        self.modifyTickedGenomeButton.setObjectName("modifyTickedGenomeButton")
        self.modifyTickedGenomeButton.clicked.connect(self.modifyGenomeClicked)
        self.buttonsLayout.addWidget(self.modifyTickedGenomeButton)

        self.completButtonsLayout.addLayout(self.buttonsLayout)

        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.completButtonsLayout.addItem(spacerItem6)

        self.gridLayout.addLayout(self.completButtonsLayout, 6, 1, 1, 1)

        self.completProgressionLayout = QtWidgets.QVBoxLayout()
        self.completProgressionLayout.setSpacing(6)
        self.completProgressionLayout.setObjectName("completProgressionLayout")

        self.progressionLabel = QtWidgets.QLabel(self.centralWidget)
        self.progressionLabel.setObjectName("progressionLabel")
        self.progressionLabel.setWordWrap(True)
        self.progressionLabel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.progressionLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.progressionLabel.setAlignment(Qt.AlignHCenter)
        self.completProgressionLayout.addWidget(self.progressionLabel)

        self.gridLayout.addLayout(self.completProgressionLayout, 1, 1, 1, 1)

        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 5, 1, 1, 1)

        self.genomeListWidget = QtWidgets.QListWidget(self.centralWidget)
        self.genomeListWidget.setMinimumSize(QtCore.QSize(200, 0))
        self.genomeListWidget.setMaximumSize(QtCore.QSize(250, 16777215))
        self.genomeListWidget.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.genomeListWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.genomeListWidget.setObjectName("genomeListWidget")
        self.genomeListWidget.setSpacing(3)
        self.gridLayout.addWidget(self.genomeListWidget, 0, 0, 8, 1)

        MainWindow.setCentralWidget(self.centralWidget)

        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menuBar.setObjectName("menuBar")

        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")

        self.menuAnnotator = QtWidgets.QMenu(self.menuBar)
        self.menuAnnotator.setObjectName("menuAnnotator")

        self.menuRNAtor = QtWidgets.QMenu(self.menuBar)
        self.menuRNAtor.setObjectName("menuRNAtor")

        #self.menuComparator = QtWidgets.QMenu(self.menuBar)
        #self.menuComparator.setObjectName("menuComparator")

        MainWindow.setMenuBar(self.menuBar)

        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")

        self.projectLocationToolButton = QtWidgets.QToolButton(self.centralWidget)
        self.projectLocationToolButton.setIcon(QtGui.QIcon("./gui/pictures/iconFolder.png"))
        self.projectLocationToolButton.setAutoRaise(True)
        self.projectLocationToolButton.setObjectName("projectLocationToolButton")
        self.statusBar.addPermanentWidget(self.projectLocationToolButton)
        self.projectLocationToolButton.clicked.connect(self.openProjectFolder)

        self.ncbiWebToolButton = QtWidgets.QToolButton(self.centralWidget)
        self.ncbiWebToolButton.setIcon(QtGui.QIcon("./gui/pictures/iconNCBI.png"))
        self.ncbiWebToolButton.setAutoRaise(True)
        self.ncbiWebToolButton.setObjectName("ncbiWebToolButton")
        self.ncbiWebToolButton.clicked.connect(self.openNCBIWeb)
        self.statusBar.addPermanentWidget(self.ncbiWebToolButton)
        
        self.projectOpenLabel = QtWidgets.QLabel(self.centralWidget)
        self.projectOpenLabel.setObjectName("projectOpen")
        self.statusBar.addWidget(self.projectOpenLabel)

        MainWindow.setStatusBar(self.statusBar)

        self.actionNewProject = QtWidgets.QAction(MainWindow)
        self.actionNewProject.setObjectName("actionNewProject")
        self.actionNewProject.triggered.connect(self.newProjectClicked)

        self.actionOpenProject = QtWidgets.QAction(MainWindow)
        self.actionOpenProject.setObjectName("actionOpenProject")
        self.actionOpenProject.triggered.connect(self.openProjectClicked)

        self.annotateGenome = QtWidgets.QAction(MainWindow)
        self.annotateGenome.setObjectName("annotateGenome")
        self.annotateGenome.triggered.connect(self.annotate)

        self.actionReplaceANbyLocusTagBLAST = QtWidgets.QAction(MainWindow)
        self.actionReplaceANbyLocusTagBLAST.setObjectName("actionReplaceANbyLocusTagBLAST")
        self.actionReplaceANbyLocusTagBLAST.triggered.connect(self.replaceANbyLTBlastClicked)

        self.actionNetworkConnection = QtWidgets.QAction(MainWindow)
        self.actionNetworkConnection.setObjectName("actionNetworkConnection")
        self.actionNetworkConnection.triggered.connect(self.networkConnectClicked)

        self.actionGethomologConnection = QtWidgets.QAction(MainWindow)
        self.actionGethomologConnection.setObjectName("actionNetworkConnection")
        self.actionGethomologConnection.triggered.connect(self.gethomologclicked)

        self.actionGFFtoGTF = QtWidgets.QAction(MainWindow)
        self.actionGFFtoGTF.setObjectName("actionGFFtoGTF")
        self.actionGFFtoGTF.triggered.connect(self.gffTOgtfClicked)

        self.actionRNAtor = QtWidgets.QAction(MainWindow)
        self.actionRNAtor.setObjectName("actionRNAtor")
        self.actionRNAtor.triggered.connect(self.RNAtorClickedshort)

        self.actionRNAtorlong = QtWidgets.QAction(MainWindow)
        self.actionRNAtorlong.setObjectName("actionRNAtorlong")
        self.actionRNAtorlong.triggered.connect(self.RNAtorClickedlong)

        self.actionExtractSeq = QtWidgets.QAction(MainWindow)
        self.actionExtractSeq.setObjectName("actionExtractSeq")
        self.actionExtractSeq.triggered.connect(self.extractSeq)

        self.actionChromosomeComparison = QtWidgets.QAction(MainWindow)
        self.actionChromosomeComparison.setObjectName("actionChromosomeComparison")

        self.menuFile.addAction(self.actionNewProject)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpenProject)
        self.menuAnnotator.addAction(self.annotateGenome)
        self.menuAnnotator.addSeparator()
        self.menuAnnotator.addAction(self.actionReplaceANbyLocusTagBLAST)
        self.menuAnnotator.addSeparator()
        self.menuAnnotator.addAction(self.actionNetworkConnection)
        self.menuAnnotator.addSeparator()
        self.menuAnnotator.addAction(self.actionGethomologConnection)
        self.menuRNAtor.addAction(self.actionGFFtoGTF)
        self.menuRNAtor.addSeparator()
        self.menuRNAtor.addAction(self.actionRNAtor)
        self.menuRNAtor.addSeparator()
        self.menuRNAtor.addAction(self.actionRNAtorlong)
        self.menuRNAtor.addSeparator()
        self.menuRNAtor.addAction(self.actionExtractSeq)
        #self.menuComparator.addAction(self.actionChromosomeComparison)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAnnotator.menuAction())
        self.menuBar.addAction(self.menuRNAtor.menuAction())
        #self.menuBar.addAction(self.menuComparator.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.change("Welcome to Annotator/RNAtor.", 0, 5000)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Mainrun command only if tuple is not emptyWindow", "RNAnnotator"))
        self.numberThreadsLabel.setText(_translate("MainWindow", "Number of threads to use"))
        self.addGenomeButton.setText(_translate("MainWindow", "Add Genome"))
        self.addMultipleGenomeButton.setText(_translate("MainWindow", "Add Multiple Genome"))
        self.addAnnotateFolderButton.setText(_translate("MainWindow", "Add folder to Annotate"))
        self.deleteTickedGenomeButton.setText(_translate("MainWindow", "Delete Ticked Genome"))
        self.modifyTickedGenomeButton.setText(_translate("MainWindow", "Modify Ticked Genome"))
        self.genomeListWidget.setSortingEnabled(True)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAnnotator.setTitle(_translate("MainWindow", "Annotator"))
        self.menuRNAtor.setTitle(_translate("MainWindow", "RNAtor"))
        #self.menuComparator.setTitle(_translate("MainWindow", "Comparator"))
        self.actionNewProject.setText(_translate("MainWindow", "New Project"))
        self.actionOpenProject.setText(_translate("MainWindow", "Open Project"))
        self.annotateGenome.setText(_translate("MainWindow", "Annotate Genomes"))
        self.actionReplaceANbyLocusTagBLAST.setText(_translate("MainWindow", "BLAST"))
        self.actionNetworkConnection.setText(_translate("MainWindow", "Network Connect"))
        self.actionGethomologConnection.setText(_translate("MainWindow", "Get Homologs"))
        self.actionGFFtoGTF.setText(_translate("MainWindow", "GFF to GTF"))
        self.actionRNAtor.setText(_translate("MainWindow", "RNAtor for Illumina"))
        self.actionRNAtorlong.setText(_translate("MainWindow", "RNAtor for Nanopore"))
        self.actionExtractSeq.setText(_translate("MainWindow", "Extract protein sequence"))
        self.actionChromosomeComparison.setText(_translate("MainWindow", "Chromosome Comparison"))
        self.threadsSpinBox.setSuffix(" / "+ str(self.threadsSpinBox.maximum()))
        self.projectOpenLabel.setText(_translate("MainWindow", "No open project."))


    def printMessage(self, message):
        self.progressionLabel.setText("<b>%s</b>" %(message))
        self.progressionLabel.setVisible(True)


    def hideMessage(self):
        self.progressionLabel.setVisible(False)


    def change(self, message, msAfter, msKeep):
        QtCore.QTimer.singleShot(msAfter, lambda: self.printMessage(message))
        QtCore.QTimer.singleShot(msKeep, lambda: self.hideMessage())


    def addItem(self, genomeName):
        self.item = QtWidgets.QListWidgetItem(genomeName, self.genomeListWidget)
        self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsUserCheckable)
        self.item.setCheckState(QtCore.Qt.Unchecked)


    def getCheckedItems(self):
        checkedItems = []
        for index in range(self.genomeListWidget.count()):
            if self.genomeListWidget.item(index).checkState() == Qt.Checked:
                checkedItems.append(self.genomeListWidget.item(index))
        return checkedItems


    def getCheckedItemsName(self):
        checkedItems = []
        for index in range(self.genomeListWidget.count()):
            if self.genomeListWidget.item(index).checkState() == Qt.Checked:
                checkedItems.append(self.genomeListWidget.item(index).text())
        return tuple(checkedItems)


    def getAllItems(self):
        allGenomes = []
        for index in range(self.genomeListWidget.count()):
            allGenomes.append(self.genomeListWidget.item(index).text())
        return tuple(allGenomes)


    def getThreadsNumberFromOS(self):
        return int(os.cpu_count())


    def establishingConnexions(self):
        self.controller.project.openFolderSignal.connect(self.openFolder)#checked
        self.controller.projectManagement.addGenomeDone.connect(self.addGenomeGUI)#checked
        #self.controller.projectManagement.addGenomeDone.connect(self.addannotate)#checked
        self.controller.projectManagement.addGenomeError.connect(self.errorGUI)#checked
        self.controller.projectManagement.removeGenome.connect(self.removeGenomeGUI)#checked
        self.controller.projectManagement.addGenomeCSVError.connect(self.errorGUI)#checked
        self.controller.projectManagement.genomeModified.connect(self.genomeModifiedGUI)#checked
        #_________________________________________________________________________________________#
        self.controller.annotategenome.annotateStepDone.connect(self.annotation)
        self.controller.annotator.annotatorStep1Error.connect(self.errorGUI)#checked
        self.controller.annotator.annotatorStep1Done.connect(self.replaceANbyLTBlastGUI)#checked
        self.controller.annotator.blastInformations.connect(self.startNetworkGUI)#checked
        self.controller.annotator.annotatorStep2Error.connect(self.errorGUI)#checked
        self.controller.annotator.annotatorStep2Done.connect(self.networkDoneGUI)#checked
        self.controller.proteinHomolog.annotatorStep2Done.connect(self.getHomologues)#checked
        #_________________________________________________________________________________________#
        
        self.controller.rnator.rnatorStep1Error.connect(self.errorGUI)#checked
        self.controller.rnator.rnatorStep1Done.connect(self.gffTOgtfDoneGUI)#checked
        self.controller.rnator.rnatorStep2Error.connect(self.errorGUI)#checked
        self.controller.rnator.rnatorStep2Done.connect(self.RNAtorDoneGUI)#checked
        self.controller.rnator.progressDialog.connect(self.setProgressDialog)#checked


    #_____________________________________________________________________________________________#


    def newProjectClicked(self):#checked
        from gui.subclass.newprojectdialog import getProjectInformation

        projectPath = getProjectInformation(self.centralWidget)
        if projectPath:
            self.controller.newProjectController(projectPath)
            self.genomeListWidget.clear()
            self.projectOpenLabel.setText("Project : <b>%s</b>" 
                %(self.controller.getProject().getName()))
            self.establishingConnexions()
            self.change("Workspace created !", 0, 5000)

    def openProjectClicked(self):#checked
        from gui.subclass.openProjectDialog import getProjectPath
        projectInformation = getProjectPath(self.centralWidget)
        if projectInformation:
            if self.controller.openProjectController(projectInformation):
                print("1")
                self.genomeListWidget.clear()
                count = len(self.controller.getProject().getGenomes())
                print(f"count:{count}")
                for genome in self.controller.getProject().getGenomes():
                    self.addItem(genome)
                self.projectOpenLabel.setText("Project : <b>%s</b>" %(self.controller.getProject().getName()))
                self.establishingConnexions()
                self.change("Workspace has been opened successuflly.", 0, 5000)
            else:
                QtWidgets.QMessageBox.critical(self.centralWidget, "Invalid project directory", \
                    "Some errors were encountered during project verification. Here is some reasons:\n\t"\
                        "- The project was not created by the tool itself.\n\t"\
                            "- Some files were modified or deleted.")


    def addGenomeClicked(self):#checked
        from gui.subclass.addgenomedialog import getGenomeInformation
        from gui.subclass.addFromComputer import getGenomeFilesPath
        from gui.subclass.addFromNCBI import getGenomeURL

        if self.controller.isProjectOpen():
            genomeInformations = getGenomeInformation(self.centralWidget)
            print(genomeInformations)
            if genomeInformations[0] != 0:
                if genomeInformations[-1] not in self.getAllItems():
                    if genomeInformations[0] == 2:
                        genomeFilesPath = getGenomeFilesPath(self.centralWidget)
                        print(genomeFilesPath)
                        print(genomeInformations[-1])
                        if genomeFilesPath:
                            self.controller.addGenomeFromComputerController(genomeInformations[-1], genomeFilesPath)
                    elif genomeInformations[0] == 3:
                        ftpLink = getGenomeURL(self.centralWidget)
                        if ftpLink:
                            self.controller.addGenomeFromNCBIController(genomeInformations[-1], ftpLink)
                else:
                    QtWidgets.QMessageBox.critical(self.centralWidget, "Existing genome", "The entered genome name already exist. "\
                        "Please enter an other genome name.")
        else:
            QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")


    def addGenomeGUI(self, genomeName):#checked
        self.addItem(genomeName)
        self.change("%s has been added successfully to the database." %(genomeName), 0, 5000)


    def errorGUI(self, errorInformations):#checked
        QtWidgets.QMessageBox.critical(self.centralWidget,  
            errorInformations[0], errorInformations[-1])


    def deleteGenomeClicked(self):#checked1
        if self.controller.isProjectOpen():
            for genome in self.getCheckedItemsName():
                self.controller.deleteGenomeController(genome)
        else:
            QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")


    def removeGenomeGUI(self, genomeName):#checked1
        for genome in self.getCheckedItems():
            if genome.text() == genomeName:
                self.genomeListWidget.takeItem(self.genomeListWidget.row(genome))
                self.change("%s has been seccessuflly deleted." %(genome.text()), 0, 5000)
                break


    def addMultipleGenomeClicked(self):#checked1
        if self.controller.isProjectOpen():
            
            QtWidgets.QMessageBox.information(self.centralWidget, "Note", 
            "The csv file values must be separated by ';'.\n\
            Each line represent a genome. A line must be as follow:\n\
            \tgenomeName;ffnFilePath;fnaFilePath;faaFilePath;gffFilePath;featureTableFilePath;")
            csvPath = QtWidgets.QFileDialog.getOpenFileName(self.centralWidget, 
                "CSV file", "/home", "Files (*.csv)")
            if csvPath[0] != "":
                self.controller.addGenomesCSVController(csvPath[0])
        else:
            QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")


    def modifyGenomeClicked(self):#checked1
        from gui.subclass.modifyGenomeDialog import startModifyGenomeDialog

        if self.controller.isProjectOpen():
            for genome in self.getCheckedItemsName():
                filesPath = startModifyGenomeDialog(self.centralWidget, self.controller.getProject().getPath().path() + 
                                                    "/Database/%s" %(genome))
                if filesPath:
                    self.controller.modifyGenomeController(genome, filesPath)
        else:
             QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")


    def genomeModifiedGUI(self, genomeName):#checked1
        self.change("%s has been successfuly modified." %(genomeName), 0, 5000)


    def openNCBIWeb(self):#checked1
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://www.ncbi.nlm.nih.gov/genome/browse#!/overview/"))


    def openProjectFolder(self):#checked1
        if not self.controller.isProjectOpen():
            QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")
        else:
            self.controller.openProjectFolderController()


    def openFolder(self, projectPath):#checked1
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(projectPath))
    
    
    def addannotate(self):
        from gui.subclass.prokka_upload import uploadgenome
        print("20")
        if self.controller.isProjectOpen():
            global genomeUpload
            genomeUpload = uploadgenome()
            return genomeUpload
        else:
            QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")
    
    
    def annotate(self):
        if self.controller.isProjectOpen():
            #tickedGenomes = self.getCheckedItemsName()
            genomeNames = []
            print("100")
            for file in os.listdir(genomeUpload):
                genomeName = file.rsplit('.', 1)[0]
                genomeNames.append(genomeName)
            genomeNames = tuple(genomeNames)
            print(genomeNames)
            if genomeNames:
                self.controller.annotateGenomeStepController(genomeNames, str(self.threadsSpinBox.value()), genomeUpload)
            projectPath = self.controller.getProject().getPath().path()
            genomeAnnotation = os.path.join(projectPath, "Annotation")
            if len(genomeNames) == 1:
                lastDir = os.path.join(genomeAnnotation, genomeNames[0])
            else:
                lastDir = os.path.join(genomeAnnotation, genomeNames[-1])
            print(lastDir)
            lastFile = genomeNames[-1]
            print(lastFile)
            lastFilePath = os.path.join(lastDir, lastFile + '.gbk')
            print(lastFilePath)
            while not os.path.isfile(lastFilePath):
                time.sleep(10)
            genomeInformation = {}
            for genome in genomeNames:
                genomeFilePath = []
                for root, dirnames, filenames in os.walk(genomeAnnotation):
                    for name in filenames:
                        if (genome in name) and (name.endswith('.ffn')):
                            ffnPath = os.path.join(genomeAnnotation, genome, name)
                            genomeFilePath.append(ffnPath)
                        elif (genome in name) and (name.endswith('.fna')):
                            fnaPath = os.path.join(genomeAnnotation, genome, name)
                            genomeFilePath.append(fnaPath)
                        elif (genome in name) and (name.endswith('.faa') and ('tmp' not in name)):
                            faaPath = os.path.join(genomeAnnotation, genome, name)
                            genomeFilePath.append(faaPath)
                        elif(genome in name) and name.endswith('.gff'):
                            gffPath = os.path.join(genomeAnnotation, genome, name)
                            genomeFilePath.append(gffPath)
                ext_list = [".ffn", ".fna", ".faa", ".gff"]
                for filePath in genomeFilePath:
                    def mycompare(filePath):
                        return ext_list.index(os.path.splitext(filePath)[1])
                genomeFilePath = sorted(genomeFilePath, key=mycompare)
                genomeInformation[genome] = tuple(genomeFilePath)
                print(genomeInformation[genome])
                self.controller.addGenomeFromComputerController(genome, genomeInformation[genome])
            
        else:
            QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")
        


    def annotation(self):#checked1
        self.change("Prokka annotations completed", 0, 5000)


    def replaceANbyLTBlastClicked(self):#checked1
        from gui.subclass.blastdialog import startBlastDialog

        if self.controller.isProjectOpen():
            tickedGenomes = self.getCheckedItemsName()
            if len(tickedGenomes) <= 1:
                QtWidgets.QMessageBox.critical(self.centralWidget, "Not enough selcted genomes", "At least two genomes must be ticked.")
            else:
                blastInformations = startBlastDialog(self.centralWidget)
                if blastInformations:
                    self.controller.annotatorStep1Controller(blastInformations[0], tickedGenomes, str(self.threadsSpinBox.value()))
        else:
            QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")


    def replaceANbyLTBlastGUI(self):#checked1
        self.change("Blast process has been successfully done.", 0, 5000)


    def networkConnectClicked(self):#checked1
        if self.controller.isProjectOpen():
            tickedGenomes = self.getCheckedItemsName()
            if len(tickedGenomes) <= 1:
                QtWidgets.QMessageBox.critical(self.centralWidget, "Not enough selcted genomes", "At least two genomes must be ticked.")
            else:
                self.controller.annotatorStep2Controller(tickedGenomes)
        else:
            QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")


    def gethomologclicked(self):#checked1
        if self.controller.isProjectOpen():
            from gui.subclass.get_homologs_method import get_homolog_data
            get_method, get_Lt, get_similarity = get_homolog_data()
            tickedGenomes = self.getCheckedItemsName()
            self.controller.homologStepController(tickedGenomes, str(self.threadsSpinBox.value()), get_method, get_Lt, get_similarity)
        else:
            QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")
            

    
    def startNetworkGUI(self, genomeLocusDict, blastTypeInfo, tickedGenomes):#checked1
        from gui.subclass.networkConnectDialog import getNetworkInformation

        userChoices = getNetworkInformation(self.centralWidget, genomeLocusDict, blastTypeInfo, tickedGenomes)
        if userChoices:
            self.controller.annotatorStep2UserChoicesController(userChoices)


    def networkDoneGUI(self):#checked1
        self.change("Gene association file has been successfully created.", 0, 5000)

    def getHomologues(self):
        self.change("Gene association file has been successfully created.", 0, 5000)


    def gffTOgtfClicked(self):#checked1
        if not self.controller.isProjectOpen():
            QtWidgets.QMessageBox.critical(self.centralWidget, "No current project", "Please create or open an existing porject.")
        else:
            not self.controller.rnatorStep1(self.getCheckedItemsName())


    def gffTOgtfDoneGUI(self):#checked1
        self.change("GTF files were successfully created.", 0, 5000)
    

    def RNAtorClickedshort(self):#checked1
        from gui.subclass.window1 import uploaddata
        import fnmatch, shutil
        attempt = uploaddata()

        if not self.controller.isProjectOpen():
                QtWidgets.QMessageBox.critical(self.centralWidget, 
                    "No current project", "Please create or open an existing porject.")
        
        if attempt == "Automatic":
            from gui.subclass.window2 import automatic_upload
            automaticupload = automatic_upload()
            getlist = list(automaticupload)
            dbpath = getlist[0]
            fqpath = getlist[1]
            
            genomesInfo = {}
            import re
            for genome in self.getCheckedItemsName():
                print(genome)
                files = []
                fqname = os.listdir(fqpath)
                for file in fqname:
                    gen = str(genome)
                    if gen.lower() in file.lower():
                        file = os.path.join(fqpath, file)
                        files.append(file)
                        files.sort()
                    else:
                        continue   
                        
                for root, dirnames, filenames in os.walk(dbpath):
                    for fna in fnmatch.filter(filenames,'*.fna'):
                        if genome in fna:
                            file_fna = os.path.join(dbpath, genome, 'FNA', fna)
                        #fnafile.append(file)
                            files.append(file_fna)
                    
                for root, dirnames, filenames in os.walk(dbpath):
                    for filename in fnmatch.filter(filenames,'*.gtf'):
                        if genome in filename:
                            gtf = os.path.join(dbpath, genome, 'GTF', filename)
                        # gtffile.append(gtf)
                            files.append(gtf)
                
                genomesInfo[genome] = tuple(files)       
            print(genomesInfo)                     
            if genomesInfo:
                self.controller.rnatorStep2(genomesInfo, str(self.threadsSpinBox.value()))
                
        elif attempt == "Manual":
            from gui.subclass.RNAtorDialog import getRNAtorInformation

            if not self.controller.isProjectOpen():
                QtWidgets.QMessageBox.critical(self.centralWidget, 
                    "No current project", "Please create or open an existing porject.")
            else:
                genomesInformation = {}
                for genome in self.getCheckedItemsName():
                    filesInformation = getRNAtorInformation(self.centralWidget, genome)
                    if filesInformation:
                        genomesInformation[genome] = filesInformation
                        
                        
                if genomesInformation:
                    self.controller.rnatorStep2(genomesInformation, str(self.threadsSpinBox.value()))
       
    def RNAtorClickedlong(self):#checked1
        from gui.subclass.window1 import uploaddata
        import fnmatch, shutil
        attempt = uploaddata()

        if not self.controller.isProjectOpen():
                QtWidgets.QMessageBox.critical(self.centralWidget, 
                    "No current project", "Please create or open an existing porject.")
        
        if attempt == "Automatic":
            from gui.subclass.window2 import automatic_upload
            automaticupload = automatic_upload()
            getlist = list(automaticupload)
            dbpath = getlist[0]
            fqpath = getlist[1]
            
            genomesInfo = {}
            import re
            for genome in self.getCheckedItemsName():
                files = []
                fqname = os.listdir(fqpath)
                for file in fqname:
                    gen = str(genome)
                    if gen.lower() in file.lower():
                        file = os.path.join(fqpath, file)
                        files.append(file)
                        files.sort()
                    else:
                        continue   
                        
                for root, dirnames, filenames in os.walk(dbpath):
                    for fna in fnmatch.filter(filenames,'*.fna'):
                        if genome in fna:
                            file_fna = os.path.join(dbpath, genome, 'FNA', fna)
                        #fnafile.append(file)
                            files.append(file_fna)
                    
                for root, dirnames, filenames in os.walk(dbpath):
                    for filename in fnmatch.filter(filenames,'*.gtf'):
                        if genome in filename:
                            gtf = os.path.join(dbpath, genome, 'GTF', filename)
                        # gtffile.append(gtf)
                            files.append(gtf)
                
                genomesInfo[genome] = tuple(files)       
            print(genomesInfo)                     
            if genomesInfo:
                self.controller.rnatorStep3(genomesInfo, str(self.threadsSpinBox.value()))
                
        elif attempt == "Manual":
            print("yes")

    def extractSeq(self):#checked1
        from gui.subclass.extractProtein import extractProteinSeq

        if not self.controller.isProjectOpen():
                QtWidgets.QMessageBox.critical(self.centralWidget, 
                    "No current project", "Please create or open an existing porject.")
        else:
            getGenome, getProteinId, getMethod = extractProteinSeq()
            print(getGenome, getProteinId, getMethod)

    def RNAtorDoneGUI(self, rnaS1NotPerfGenomes):#checked1
        if rnaS1NotPerfGenomes:
            QtWidgets.QMessageBox.critical(self.centralWidget, "Steps not performed", 
                "For some genomes, there are some steps that were not performed.\n\
                Please perfrome the steps before.\n\
                Here is the concerned genomes :\n%s" %(", ".join(rnaS1NotPerfGenomes)))
        else:
            self.change("RNAtor process was successfully done.", 0, 5000)


    def setProgressDialog(self):#checked1
        self.popUp = QProgressDialog(self.centralWidget, Qt.Dialog)
        self.popUp.setModal(Qt.WindowModal)
        self.popUp.setWindowTitle("RNAtor progression")
        self.controller.rnator.progressSetValue.connect(self.popUp.setValue)
        self.controller.rnator.progressSetTextLabel.connect(self.popUp.setLabelText)
        self.controller.rnator.progressSetMin.connect(self.popUp.setMinimum)
        self.controller.rnator.progerssSetMax.connect(self.popUp.setMaximum)
        self.controller.rnator.rnatorStep2Done.connect(self.popUp.close)


def startGUI(controller):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, controller, app)
    MainWindow.show()
    sys.exit(app.exec_())

