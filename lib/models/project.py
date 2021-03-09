#!/bin/python3

from PyQt5.QtCore import QObject, QDir, pyqtSignal

class Project(QObject):

    def __init__(self, **kwargs):
        super().__init__(None)
        if "projectPath" in kwargs:
            self.path = QDir(kwargs["projectPath"])
        else:
            self.path = QDir()
        if "genomesList" in kwargs:
            if type(kwargs["genomesList"]) == list and not kwargs["genomesList"] == "-":
                self.genomesList = kwargs["genomesList"]
            else:
                self.genomesList = []
        else:
            self.genomesList = []

        self.genomeNameLocus = {}
        self.annotatorStep1 = {"Blastn":{}, "Blastp":{}}
        self.annotatorStep2 = {}
        self.rnatorStep1 = {}
        self.rnatorStep2 = {}


    #Signals
    openFolderSignal = pyqtSignal(str)#checked1

    #_________________________________________Getter______________________________________________#


    def getPath(self):#checked
        return self.path


    def getGenomes(self):#checked
        return self.genomesList


    def getName(self):
        return self.path.dirName()


    def getAnnotatorStep1Info(self):#checked1
        return self.annotatorStep1


    def getAnnotatorStep2Info(self):#checked1
        return self.annotatorStep2

    
    def getRNAtorStep1Info(self):#checked1
        return self.rnatorStep1

    
    def getRNAtorStep2Info(self):
        return self.rnatorStep2


    def getGenomesNameLocus(self):#checked1
        return self.genomeNameLocus

    #Setter
    def setPath(self, projectPath):
        self.path.setPath(projectPath)

    
    def setGenomes(self, genomes):
        self.genomesList = genomes

    
    def setGenomesNameLocus(self, genomeNameLocusDict):#checked1
        self.genomeNameLocus = genomeNameLocusDict


    def setAnnotatorStep1Info(self, dictInfo):#checked1
        self.annotatorStep1 = dictInfo

    
    def setAnnotatorStep2Info(self, dictInfo):#checked1
        self.annotatorStep2 = dictInfo


    def setRNAtorStep1Info(self, dictInfo):#checked1
        self.rnatorStep1 = dictInfo


    def setRNAtorStep2Info(self, dictInfo):#checked1
        self.rnatorStep2 = dictInfo


    def setGenomeNameLocus(self, genomeName, locus):#checked1
        self.genomeNameLocus[genomeName] = locus


    def setAnnotatorStep1Genome(self, blast, genomeName, value):#checked1
        self.annotatorStep1[blast][genomeName] = value
    

    def setAnnotatorStep2Genome(self, genomeName, value):#checked1
        self.annotatorStep2[genomeName] = value


    def setRNAtorStep1Genome(self, genomeName, value):#checked1
        self.rnatorStep1[genomeName] = value


    def setRNAtorStep2Genome(self, genomeName, value):#checked1
        self.rnatorStep2[genomeName] = value


    def setAllStepsGenome(self, genomeName, value):#checked1
        self.genomeNameLocus[genomeName] = ""
        self.setAnnotatorStep1Genome("Blastn", genomeName, value)
        self.setAnnotatorStep1Genome("Blastp", genomeName, value)
        self.setAnnotatorStep2Genome(genomeName, value)
        self.setRNAtorStep1Genome(genomeName, value)
        self.setRNAtorStep2Genome(genomeName, value)


    def addGenome(self, genomeName):#checked
        self.genomesList.append(genomeName)
        self.genomeNameLocus[genomeName] = ""
        self.annotatorStep1["Blastn"][genomeName] = False
        self.annotatorStep1["Blastp"][genomeName] = False
        self.annotatorStep2[genomeName] = False
        self.rnatorStep1[genomeName] = False
        self.rnatorStep2[genomeName] = False


    def removeGenome(self, genomeName):#checked
        self.genomesList.remove(genomeName)
        del self.genomeNameLocus[genomeName]
        del self.annotatorStep1["Blastn"][genomeName]
        del self.annotatorStep1["Blastp"][genomeName]
        del self.annotatorStep2[genomeName]
        del self.rnatorStep1[genomeName]
        del self.rnatorStep2[genomeName]
        

    def projectPathFolder(self, project):#checked1
        self.openFolderSignal.emit(project[0].getPath().path())
