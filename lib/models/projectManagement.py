#!/bin/python3

from PyQt5.QtCore import QObject, QDir, QFile, QIODevice, QTextStream, pyqtSignal
from lib.models.project import Project
import json

class ProjectManagement(QObject):

    def __init__(self):
        super().__init__(None)
        self.directories = ("FFN", "FNA", "FAA", "GFF", "FeatureTable")
        self.fileExtensions = ("ffn", "fna", "faa", "gff", "txt")
        self.realExtensions = ("_cds_from_genomic.fna", "_genomic.fna", "_protein.faa", 
            "_genomic.gff", "_feature_table.txt")


    #________________________________________Signals______________________________________________#
    addGenomeDone = pyqtSignal(str)#checked1
    addGenomeError = pyqtSignal(tuple)#checked1
    checkProjectCacheResultOperate = pyqtSignal(tuple, str)#checked1
    removeGenome = pyqtSignal(str)#checked1
    addGenomesCSVResult = pyqtSignal(dict)#checked1
    addGenomeCSVError = pyqtSignal(tuple)#checked1
    genomeModified = pyqtSignal(str)#checked1


    def newProject(self, projectPath):#checked
        projectPath.mkpath("Cache")
        projectPath.mkdir("BLASTresults")
        projectPath.mkdir("BWA")
        projectPath.mkdir("Counts")
        projectPath.mkdir("Database")


    def addGenomeFromComputer(self, genomeName, filesPath, project):#checked
        for i, filePath in enumerate(filesPath):
            project[0].getPath().mkpath("Database/%s/%s" %(genomeName, self.directories[i]))
            QFile.copy(filePath, "%s/Database/%s/%s/%s.%s" 
                %(project[0].getPath().path(), genomeName, self.directories[i], genomeName, 
                    self.fileExtensions[i]))
        if not project[0].getPath().exists("Database/%s/%s" %(genomeName, self.directories[-1])):
            project[0].getPath().mkpath("Database/%s/%s" %(genomeName, self.directories[-1]))
            if not self.makeFeatureTable(genomeName, project[0].getPath().path()):
                QDir('%s/Database/%s' 
                    %(project[0].getPath().path(), genomeName)).removeRecursively()
                return
        self.addGenomeDone.emit(genomeName)
    

    def makeFeatureTable(self, genomeName, projectQDir):#checked
        featureTableFile = QFile("%s/Database/%s/FeatureTable/%s.txt" 
            %(projectQDir, genomeName, genomeName))
        if featureTableFile.open(QIODevice.WriteOnly | QIODevice.Text):
            ffnFile = QFile("%s/Database/%s/FFN/%s.ffn" %(projectQDir, genomeName, genomeName))
            if ffnFile.open(QIODevice.ReadOnly | QIODevice.Text):
                featureTableIn = QTextStream(featureTableFile)
                ffnOut = QTextStream(ffnFile)
                line = ffnOut.readLine().strip()
                if line.startswith(">lcl"):
                    while not ffnOut.atEnd():
                        if line.startswith(">"):
                            locusTag = line.split("[locus_tag=")[1].split("]")[0]
                            if "[protein_id" in line:
                                accessionN = line.strip().split("[protein_id=")[1].split("]")[0]
                                featureTableIn << "CDS\t.\t.\t.\t.\t.\t.\t.\t.\t.\t%s\t.\t.\t.\t.\t.\t%s\n" \
                                    %(accessionN, locusTag)
                            else:
                                featureTableIn << "CDS\t.\t.\t.\t.\t.\t.\t.\t.\t.\t%s\t.\t.\t.\t.\t.\t%s\n" \
                                    %(locusTag, locusTag)
                        line = ffnOut.readLine().strip()
                else:
                    while not ffnOut.atEnd():
                        if line.startswith(">"):
                            accessionLocus = line.strip().split(" ")[0][1:]
                            featureTableIn << "CDS\t.\t.\t.\t.\t.\t.\t.\t.\t.\t%s\t.\t.\t.\t.\t.\t%s\n" \
                                %(accessionLocus, accessionLocus)
                        line = ffnOut.readLine().strip()
                return True
            else:
                self.addGenomeError.emit(("%s: ffn file" %(genomeName), 
                    "Encountered some difficulties to read ffn file."))
                return False
        else:
            self.addGenomeError.emit(("%s: feature table file" %(genomeName), 
                "Encountered some difficulties to create feature table file."))
            return False


    def writeCache(self, project):#checked
        projectCacheFile = QFile("%s/Cache/project.cache" %(project[0].getPath().path()))
        if projectCacheFile.open(QIODevice.WriteOnly | QIODevice.Text):
            projectCacheOut = QTextStream(projectCacheFile)
            projectCacheOut << "Project path:\t%s\n" %(project[0].getPath().path())
            projectCacheOut << "Genomes:\t"
            tmp = ""
            for genome in project[0].getGenomes():
                tmp += genome + ","
            if tmp:
                projectCacheOut << "%s\n" %(tmp[:-1])
            else:
                projectCacheOut << "-\n"
            projectCacheOut << "GenomeName Loucs:\t" + json.dumps(project[0].getGenomesNameLocus()) + "\n"
            projectCacheOut << "Annotator step1:\t" + json.dumps(project[0].getAnnotatorStep1Info()) + "\n"
            projectCacheOut << "Annotator step2:\t" + json.dumps(project[0].getAnnotatorStep2Info()) + "\n"
            projectCacheOut << "RNAtor step1:\t" + json.dumps(project[0].getRNAtorStep1Info()) + "\n"
            projectCacheOut << "RNAtor step2:\t" + json.dumps(project[0].getRNAtorStep2Info()) + "\n"


    def addGenomeFromNCBI(self, genomeName, ftpLink, project):#checked
        import urllib.request as request
        from contextlib import closing
        import gzip, shutil

        for i, directory in enumerate(self.directories):
            with closing(request.urlopen("%s/%s%s.gz" 
                %(ftpLink, ftpLink.split("/")[-1], self.realExtensions[i]))) as fileContent:
                    project[0].getPath().mkpath("Database/%s/%s" %(genomeName, self.directories[i]))
                    with open("%s/Database/%s/%s/%s%s.gz" 
                        %(project[0].getPath().path(), genomeName, self.directories[i], 
                            genomeName, self.fileExtensions[i]), "wb") as fileToWrite:
                                shutil.copyfileobj(fileContent, fileToWrite)

            with gzip.open("%s/Database/%s/%s/%s%s.gz" 
                %(project[0].getPath().path(), genomeName, self.directories[i],
                    genomeName, self.fileExtensions[i]), "rb") as compressedFile:
                        with open("%s/Database/%s/%s/%s.%s" 
                            %(project[0].getPath().path(), genomeName, self.directories[i],
                                genomeName, self.fileExtensions[i]), "wb") as fileToWrite:
                                    fileToWrite.write(compressedFile.read())
        self.addGenomeDone.emit(genomeName)


    def deleteGenome(self, genomeName, projectDir):#checked1
        projectDir = projectDir[0].getPath().path()
        #Deleting from database
        QDir("%s/Database/%s" %(projectDir, genomeName)).removeRecursively()
        #Deleting from BLASTResults (blast and blast database)
        genomeFileDir = QDir()
        for blast, db in {"BPresults": "DBp", "BNresults": "DBn"}.items():
            genomeFileDir.setPath("%s/BLASTresults/%s" %(projectDir, blast))
            if genomeFileDir.exists():
                for f in genomeFileDir.entryList(["%s-*" %(genomeName), "*-%s.*" %(genomeName)], QDir.Files):
                        genomeFileDir.remove(f)
                genomeFileDir.setPath("%s/BLASTresults/%s" %(projectDir, db))
                for f in genomeFileDir.entryList(["%s.*" %(genomeName)], QDir.Files):
                    genomeFileDir.remove(f)
        #Deleting SAM file
        genomeFileDir.setPath("%s/BWA" %(projectDir))
        for f in genomeFileDir.entryList(["%s.sam" %(genomeName)], QDir.Files):
            genomeFileDir.remove(f)
        #Deleting featureCounts results
        genomeFileDir.setPath("%s/Counts" %(projectDir))
        for f in genomeFileDir.entryList(["counts_%s.txt*" %(genomeName), "featoutput_%s.txt" %(genomeName)], QDir.Files):
            genomeFileDir.remove(f)
        self.removeGenome.emit(genomeName)
    

    def addGenomesCSV(self, csvPath, project):#checked1
        namePathsDict = {}
        csvFile = QFile(csvPath)
        if csvFile.open(QIODevice.ReadOnly | QIODevice.Text):
            csvIn = QTextStream(csvFile)
            lineNumber = 0
            while not csvIn.atEnd():
                line = csvIn.readLine().strip().split(";")
                lineNumber += 1
                if line[0] != "" and line[0] not in project[0].getGenomes():
                        if (line[1].endswith(".ffn") or line[1].endswith(".fna")) and \
                            QFile.exists(line[1]) and\
                            line[2].endswith(".fna") and QFile.exists(line[2]) and\
                            line[3].endswith(".faa") and QFile.exists(line[3]) and\
                            line[4].endswith(".gff") and QFile.exists(line[4]) :
                            if len(line) == 6 and line[-1] != "":
                                if line[5].endswith(".txt") and QFile.exists(line[5]):
                                    namePathsDict[line[0]] = [line[1], line[2], line[3], line[4], line[5]]
                                else:
                                    self.addGenomeCSVError.emit(("%s: feature table file error" %(line[0]), 
                                    "Worng file extension or file path does not exist in line %d of csv file." 
                                        %(lineNumber)))
                                    pass
                            else:
                                namePathsDict[line[0]] = [line[1], line[2], line[3], line[4]]
                        else:
                            self.addGenomeCSVError.emit(("%s: feature table file error" %(line[0]), 
                                "Worng file extension or file path does not exist in line %d of csv file." 
                                    %(lineNumber)))
                            pass
                else:
                    self.addGenomeCSVError.emit(("Genome name error", 
                        "Check the name in line %d of csv file." %(lineNumber)))
            self.addGenomesCSVResult.emit(namePathsDict)
        else:
            self.addGenomeCSVError.emit(("File reading error",
                "We encountered some errors while reading csv file. Please check the csv file."))

    
    def modifyGenome(self, genomeName, filesPath, project):#checked1
        for i, newFile in enumerate(filesPath):
            directory = "%s/Database/%s/%s" %(projectDir[0].getPath().path(), 
                genomeName, self.directories[i])
            if newFile != directory + "/%s.%s" %(genomeName, self.fileExtensions[i]):
                for fileToRemove in QDir(directory).entryList(["*"], QDir.Files):
                    QDir(directory).remove(fileToRemove)
                QFile.copy(newFile, directory + "/%s.%s" %(genomeName, self.fileExtensions[i]))
                project[0].setAllstepsGenome(genomeName, False)
                self.genomeModified.emit(genomeName)


def checkProjectCache(projectPath):#checked
        projectCacheFile = QFile("%s/Cache/project.cache" %(projectPath))
        if projectCacheFile.open(QIODevice.ReadOnly | QIODevice.Text):
            projectCacheIn = QTextStream(projectCacheFile)
            toReturn = []
            while not projectCacheIn.atEnd():
                line = projectCacheIn.readLine().strip().split("\t")
                if "Project path:" in line and projectPath.split("/")[-1] == line[-1].split("/")[-1]:
                    continue
                elif "Genomes:" in line:
                    tmp = []
                    if "-" in line:
                        continue
                    else:
                        for genome in line[-1].split(","):
                            tmp.append(genome)
                        toReturn.append(tmp)
                elif "GenomeName Loucs:" in line:
                    toReturn.append(json.loads(line[-1]))
                elif "Annotator step1:" in line:
                    toReturn.append(json.loads(line[-1]))
                elif "Annotator step2:" in line:
                    toReturn.append(json.loads(line[-1]))
                elif "RNAtor step1:" in line:
                    toReturn.append(json.loads(line[-1]))
                elif "RNAtor step2:" in line:
                    toReturn.append(json.loads(line[-1]))
                else:
                    return ()
            return tuple(toReturn)
        else:
            return ()

