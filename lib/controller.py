#!/bin/python3

from PyQt5.QtCore import QObject, pyqtSignal, QThread,QDir
from lib.models.project import Project
from lib.models.projectManagement import ProjectManagement
from lib.models.annotator import Annotator
from lib.models.rnator import RNAtor
from lib.models.cacheManagement import checkProjectCache, writeCache


class Controller(QObject):
    #Constructor
    def __init__(self, parent):
        super().__init__(parent)
        self.project = None
        self.workerThread = QThread()


    #_________________________________Project management signals__________________________________#
    openProjectFolder = pyqtSignal(tuple)
    writeCacheOperate = pyqtSignal(tuple)#checked
    addGenomeFromComputerOperate = pyqtSignal(str, tuple, tuple)#checked
    addGenomeOperate = pyqtSignal(str)#checked
    addGenomeFromNCBIOperate = pyqtSignal(str, str, tuple)#checked
    deleteGenomeOperate = pyqtSignal(str, tuple)#checked1
    addGenomesCSVOperate = pyqtSignal(str, tuple)#checked1
    modifyGenomeOperate = pyqtSignal(str, tuple, tuple)#checked1
    #______________________________________Annotator signals_______________________________________#
    annotatorStep1Operate = pyqtSignal(str, tuple, str, tuple)#checked1
    annotatorS2getBlastInformations = pyqtSignal(tuple, tuple)#checked1
    annotatorS2Operate = pyqtSignal(tuple, tuple)
    annotatorS2makeNewGffFile = pyqtSignal(tuple, tuple)
    #________________________________________RNAtor signals________________________________________#
    rnatorS1 = pyqtSignal(tuple, tuple)
    rnatorS2 = pyqtSignal(tuple, dict, str)


#_________________________________________General Functions________________________________________#


    def openProjectFolderController(self):
        self.openProjectFolder.emit((self.project,))


    def getProject(self):#checked
        return self.project


    def getAnnotator(self):
        return self.annotator


    def isProjectOpen(self):
        if self.project:
            return True
        else:
            return False


    def establishingConnections(self):
        #_____________________________Project management connections______________________________#
        self.openProjectFolder.connect(self.project.projectPathFolder)
        self.writeCacheOperate.connect(self.projectManagement.writeCache)#checked
        self.projectManagement.addGenomeDone.connect(self.addgenomeDoneController)#checked
        self.addGenomeFromComputerOperate.connect(self.projectManagement.addGenomeFromComputer)#checked
        self.addGenomeOperate.connect(self.project.addGenome)#checked
        self.addGenomeFromNCBIOperate.connect(self.projectManagement.addGenomeFromNCBI)#checked
        self.deleteGenomeOperate.connect(self.projectManagement.deleteGenome)#checked1
        self.projectManagement.removeGenome.connect(self.project.removeGenome)#checked1
        self.projectManagement.removeGenome.connect(self.writingCache)#checked1
        self.addGenomesCSVOperate.connect(self.projectManagement.addGenomesCSV)
        self.projectManagement.addGenomesCSVResult.connect(self.addGenomesCSVResultController)#checked1
        self.modifyGenomeOperate.connect(self.projectManagement.modifyGenome)#checked1
        #__________________________________Annotator connections__________________________________#
        self.annotatorStep1Operate.connect(self.annotator.annotatorStep1)#checked1
        self.annotator.annotatorStep1Done.connect(self.writingCache)#checked1
        self.annotatorS2getBlastInformations.connect(self.annotator.annotatorS2BlastInformations)#checked1
        self.annotatorS2Operate.connect(self.annotator.annotatorStep2)#checked1
        self.annotator.annotatorStep2Done.connect(self.writingCache)#checked1
        #____________________________________RNAtor connections___________________________________#
        self.rnatorS1.connect(self.rnator.makeGtfFiles)#checked1
        self.rnator.rnatorStep1Done.connect(self.writingCache)#checked1
        self.rnatorS2.connect(self.rnator.rnatorProcess)#checked1
        self.rnator.rnatorStep2Done.connect(self.writingCache)#checked1
        #_________________________________________________________________________________________#


    def stopWorkerThread(self):
        self.workerThread.quit()
        self.workerThread.wait()


    def initialization(self):#checked
        self.projectManagement = ProjectManagement()
        self.annotator = Annotator()
        self.rnator = RNAtor()


    def startWorkerThread(self):#checked
        self.project.moveToThread(self.workerThread)
        self.projectManagement.moveToThread(self.workerThread)
        self.annotator.moveToThread(self.workerThread)
        self.rnator.moveToThread(self.workerThread)
        self.workerThread.start()


    def writingCache(self):#checked1
        self.writeCacheOperate.emit((self.project,))


#__________________________________Project Management Controllers__________________________________#


    def newProjectController(self, projectPath):#checked
        self.project = Project(projectPath=projectPath[0])
        self.initialization()
        self.projectManagement.newProject(self.project.getPath())
        self.startWorkerThread()
        self.establishingConnections()
        self.writeCacheOperate.emit((self.project,))


    def openProjectController(self, projectPath):#checked
        from lib.models.projectManagement import checkProjectCache

        genomes = checkProjectCache(projectPath[0])
        if genomes:
            self.project = Project(projectPath=projectPath[0], genomesList=genomes[0])
            self.project.setGenomesNameLocus(genomes[-5])
            self.project.setAnnotatorStep1Info(genomes[-4])
            self.project.setAnnotatorStep2Info(genomes[-3])
            self.project.setRNAtorStep1Info(genomes[-2])
            self.project.setRNAtorStep2Info(genomes[-1])
            self.initialization()
            self.startWorkerThread()
            self.establishingConnections()
            self.writeCacheOperate.emit((self.project,))
            return True
        else:
            return False


    def addGenomeFromComputerController(self, genomeName, filesPath):#checked
        self.addGenomeFromComputerOperate.emit(genomeName, filesPath, (self.project,))


    def addGenomeFromNCBIController(self, genomeName, ftpLink):#checked
        self.addGenomeFromNCBIOperate.emit(genomeName, ftpLink[0], (self.project,))


    def addgenomeDoneController(self, genomeName):#checked
        self.addGenomeOperate.emit(genomeName)
        self.writeCacheOperate.emit((self.project,))

    
    def deleteGenomeController(self, genomeName):#checked1
        self.deleteGenomeOperate.emit(genomeName, (self.project,))


    def addGenomesCSVController(self, csvPath):#checked1
        self.addGenomesCSVOperate.emit(csvPath, (self.project,))

    
    def addGenomesCSVResultController(self, genomes):#checked1
        for genomeName, paths in genomes.items():
            self.addGenomeFromComputerController(genomeName, tuple(paths))


    def modifyGenomeController(self, genomeName, filesPath):#checked1
        self.modifyGenomeOperate.emit(genomeName, filesPath, (self.project,))


#_______________________________________Annotator functions________________________________________#


    def annotatorStep1Controller(self, blast, genomes, threads):#checked1
        self.annotatorStep1Operate.emit(blast, genomes, threads, (self.project,))


    def annotatorStep2Controller(self, tickedGenomes):#checked1
        self.annotatorS2getBlastInformations.emit((self.project,), tickedGenomes)

    
    def annotatorStep2UserChoicesController(self, userChoices):#checked1
        self.annotatorS2Operate.emit((self.project,) , userChoices)


#_________________________________________RNAtor functions_________________________________________#


    def rnatorStep1(self, tickedGenomes):#checked1
        self.rnatorS1.emit((self.project,), tickedGenomes)


    def rnatorStep2(self, genomesInformation, threads):#checked1
        self.rnatorS2.emit((self.project, ), genomesInformation, threads)


#__________________________________________________________________________________________________#