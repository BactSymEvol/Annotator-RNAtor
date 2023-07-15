#!/bin/python3

from PyQt5.QtCore import QObject, QFile, QIODevice, QTextStream, QDir, QProcess, pyqtSignal

import pandas as pd

import sys

class RNAtor(QObject):

    def __init__(self):
        super().__init__(None)
        self.process = QProcess(self)


    #Signals
    rnatorStep1Error = pyqtSignal(tuple)
    rnatorStep1Done = pyqtSignal()
    rnatorStep2Error = pyqtSignal(tuple)
    rnatorStep2Done = pyqtSignal(tuple)
    rnatorStep3Error = pyqtSignal(tuple)
    rnatorStep3Done = pyqtSignal(tuple)
    progressSetValue = pyqtSignal(int)
    progressSetTextLabel = pyqtSignal(str)
    progressSetMin = pyqtSignal(int)
    progerssSetMax =  pyqtSignal(int)
    progressDialog = pyqtSignal()


    def makeGtfFiles(self, project, tickedGenomes):#checked1
        projectPath = project[0].getPath().path()
        project = project[0]
        for genome in tickedGenomes:
            if project.getAnnotatorStep2Info()[genome]:
                outputLine = ""
                toReadFile = QFile("%s/Database/%s/GFF/%s_ANO.gff" %(projectPath, genome, genome))
                if toReadFile.open(QIODevice.ReadOnly | QIODevice.Text):
                    toReadOut = QTextStream(toReadFile)
                    while not toReadOut.atEnd():
                        line = toReadOut.readLine()
                        if line.startswith("#"):
                            continue
                        elif line.startswith(">"):
                            break
                        else:
                            line = line.strip().split("\t")
                            if line[2] == "CDS" and "pseudo=" not in line[8]:
                                outputLine += "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" \
                                    %(line[0],line[1],line[2],line[3], line[4], line[5], line[6], line[7])
                                endLine = line[8].split(";")
                                locusTag = endLine[0].split("=")[1]
                                proteinID = ""
                                for repeat in [1, 2]:
                                    for info in endLine:
                                        if "protein_id" in info and repeat == 1:
                                            proteinID = info.split("=")[1]
                                        elif "note=" in info and repeat == 2:
                                            proteinID = info.split(" ")[0].split("=")[1]
                                outputLine += "\tgene_id \"%s\"; transcript_id \"%s\"; protein_id \"%s\"\n" \
                                    %(locusTag, locusTag, proteinID)
                            elif line[2] == "gene":
                                outputLine +=  "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" \
                                    %(line[0],line[1],line[2],line[3], line[4], line[5], line[6], line[7])
                                locusTag = line[8].split(";")[0].split("=")[1]
                                outputLine += "\tgene_id \"%s\"; transcript_id \"%s\"\n" %(locusTag, locusTag)

                if not QDir("%s/Database/%s/GTF"%(projectPath, genome)).exists():
                    QDir("%s/Database/%s" %(projectPath, genome)).mkdir("GTF")
                toWriteFile = QFile("%s/Database/%s/GTF/%s_ANO.gtf" %(projectPath, genome, genome))
                if toWriteFile.open(QIODevice.WriteOnly | QIODevice.Text):
                    toWriteIn = QTextStream(toWriteFile)
                    toWriteIn << outputLine
                    project.setRNAtorStep1Genome(genome, True)
                else:
                    self.rnatorStep1Error.emit(("GTF File Writing Error",
                        "Some errors were encountred during GTF file writing."))
                    return
            else:
                self.rnatorStep1Error.emit(("Missing step", 
                    "Some steps were missed for %s. Please perform the steps before." %(genome)))
                return
        self.rnatorStep1Done.emit()


    def rnatorProcess(self, project, genomesInformation, threads):#checked1
        self.progressDialog.emit()
        project = project[0]
        projectPath = project.getPath().path()
        self.progressSetMin.emit(0)
        self.progerssSetMax.emit(len(genomesInformation))

        if not project.getPath().exists("BWA"):
            project.getPath().mkdir("BWA")
        if not project.getPath().exists("Counts"):
            project.getPath().mkdir("Counts")

        rnaS1NotPerformedGenomes = []
        for i, (genome, genomeInformation) in enumerate(genomesInformation.items()):
            self.progressSetValue.emit(i)
            if project.getRNAtorStep1Info()[genome]:
                self.progressSetTextLabel.emit("%s : Genome indexation..." %(genome))
                print(genomeInformation[2])
                self.process.start("bash",
                    ["-c", "bwa index %s" %(genomeInformation[2])])
                self.process.waitForFinished(-1)
                if self.process.exitStatus() == 1:
                    self.rnatorStep2Error.emit("RNAtor Error : BWA", "Some errors occured during genome indexation.")
                    continue

                self.progressSetTextLabel.emit("%s : file SAM creation..." %(genome))
                self.process.start("bash",
                    ["-c", "bwa mem -t %s %s %s %s > %s/BWA/%s.sam" \
                    %(threads, genomeInformation[2], genomeInformation[0], 
                        genomeInformation[1], projectPath, genome)])
                self.process.waitForFinished(-1)
                if self.process.exitStatus() == 1:
                    self.rnatorStep2Error.emit("RNAtor Error : BWA", "Some errors occured during genome SAM file creation.")
                    continue
                
                self.progressSetTextLabel.emit("%s : FeaturesCounts process..." %(genome))
                self.process.start("bash",
                    ["-c", "featureCounts -T %s -t CDS -g transcript_id -a %s -o %s/Counts/counts_%s.txt %s/BWA/%s.sam > "\
                        "%s/Counts/featoutput_%s.txt 2>&1" \
                        %(threads, genomeInformation[3], projectPath, genome, 
                            projectPath, genome, projectPath, genome)])
                self.process.waitForFinished(-1)
                if self.process.exitStatus() == 1:
                    self.rnatorStep2Error.emit(("RNAtor Error : FeatureCounts", "Some errors occured during FeatureCounts process."))
                else:
                    project.setRNAtorStep2Genome(genome, True)
            else:
                rnaS1NotPerformedGenomes.append(genome)
        
        countedGenomesPathsToFiles = []
        for key in project.getRNAtorStep2Info().keys():
            for i, (genome, genomeInformation) in enumerate(genomesInformation.items()):
                if genome in key:
                    countedGenomesPathsToFiles.append("%s/Counts/counts_%s.txt" %(projectPath, key))
        mainfile = countedGenomesPathsToFiles[0]
        print(mainfile)
        fileList = countedGenomesPathsToFiles[1:]
        print(fileList)
        df1= pd.read_csv(mainfile, sep='\t', lineterminator='\n', comment='#')
        df1 = df1.iloc[:, [0,6]]
        print(df1)
        df1.rename(columns = {list(df1)[1]: mainfile.split('/')[-1]}, inplace = True)
        for filename in fileList:
            df2 = pd.read_csv(filename, sep='\t', lineterminator='\n', comment='#')
            df2 = df2.iloc[:, [0,6]]
            print(df2)
            df2.rename(columns = {list(df2)[1]: filename.split('/')[-1]}, inplace = True)
            df1 = df1.merge(df2, on="Geneid", how='outer').sort_values(by=['Geneid'])
            print(df1)
        df1 = df1.fillna(0)
        df = df1.to_csv('%s/CountComparisonOutput.csv' %(projectPath), index=False)

        self.progressSetTextLabel.emit("Done")
        self.progressSetValue.emit(len(genomesInformation))
        self.rnatorStep2Done.emit(tuple(rnaS1NotPerformedGenomes))

        
    def rnatorProcesslong(self, project, genomesInfo, threads):#checked1
        self.progressDialog.emit()
        project = project[0]
        projectPath = project.getPath().path()
        self.progressSetMin.emit(0)
        self.progerssSetMax.emit(len(genomesInfo))

        if not project.getPath().exists("BWA"):
            project.getPath().mkdir("BWA")
        if not project.getPath().exists("Counts"):
            project.getPath().mkdir("Counts")

        rnaStep1NotPerformedGenomes = []
        for i, (genome, genomesInfo) in enumerate(genomesInfo.items()):
            self.progressSetValue.emit(i)
            if project.getRNAtorStep1Info()[genome]:
                self.progressSetTextLabel.emit("%s : Genome indexation..." %(genome))
                self.process.start("bash",
                    ["-c", "bwa index %s" %(genomesInfo[1])])
                self.process.waitForFinished(-1)
                if self.process.exitStatus() == 1:
                    self.rnatorStep3Error.emit("RNAtor Error : BWA", "Some errors occured during genome indexation.")
                    continue

                self.progressSetTextLabel.emit("%s : file SAM creation..." %(genome))
                self.process.start("bash",
                    ["-c", "bwa mem -x ont2d -t %s %s %s > %s/BWA/%s.sam" \
                    %(threads, genomesInfo[1], genomesInfo[0], 
                         projectPath, genome)])
                self.process.waitForFinished(-1)
                if self.process.exitStatus() == 1:
                    self.rnatorStep3Error.emit("RNAtor Error : BWA", "Some errors occured during genome SAM file creation.")
                    continue
                
                self.progressSetTextLabel.emit("%s : FeaturesCounts process..." %(genome))
                self.process.start("bash",
                    ["-c", "featureCounts -T %s -t CDS -g transcript_id -a %s -o %s/Counts/counts_%s.txt %s/BWA/%s.sam > "\
                        "%s/Counts/featoutput_%s.txt 2>&1" \
                        %(threads, genomesInfo[2], projectPath, genome, 
                            projectPath, genome, projectPath, genome)])
                self.process.waitForFinished(-1)
                if self.process.exitStatus() == 1:
                    self.rnatorStep3Error.emit(("RNAtor Error : FeatureCounts", "Some errors occured during FeatureCounts process."))
                else:
                    project.setRNAtorStep3Genome(genome, True)
            else:
                rnaStep1NotPerformedGenomes.append(genome)
        
        countedGenomesPathsToFiles = []
        for key in project.getRNAtorStep3Info().keys():
            countedGenomesPathsToFiles.append("%s/Counts/counts_%s.txt" %(projectPath, key))
        mainfile = countedGenomesPathsToFiles[0]
        fileList = countedGenomesPathsToFiles[1:]
        df1= pd.read_csv(mainfile, sep='\t', lineterminator='\n', comment='#')
        df1 = df1.iloc[:, [0,6]]
        df1.rename(columns = {list(df1)[1]: mainfile.split('/')[-1]}, inplace = True)
        for filename in fileList:
            df2 = pd.read_csv(filename, sep='\t', lineterminator='\n', comment='#')
            df2 = df2.iloc[:, [0,6]]
            df2.rename(columns = {list(df2)[1]: filename.split('/')[-1]}, inplace = True)
            df1 = df1.merge(df2, on="Geneid", how='outer').sort_values(by=['Geneid'])
        df1 = df1.fillna(0)
        df = df1.to_csv('%s/CountComparisonOutput.csv' %(projectPath), index=False)

        self.progressSetTextLabel.emit("Done")
        self.progressSetValue.emit(len(genomesInfo))
        self.rnatorStep3Done.emit(tuple(rnaStep1NotPerformedGenomes))