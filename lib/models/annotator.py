#!/bin/python3

from PyQt5.QtCore import QObject, QDir, QFile, QIODevice, QTextStream, QProcess, pyqtSignal

class Annotator(QObject):

    def __init__(self):
        super().__init__(None)
        self.process = QProcess(self)
        self.dbtypeDict = {"Blastn":"nucl", "Blastp":"prot"}
        self.dbDirectDict = {"Blastn":"DBn", "Blastp":"DBp"}
        self.cdsDict = {"Blastn":"FFN", "Blastp":"FAA"}
        self.resultDirecDict = {"Blastn":"BNresults", "Blastp":"BPresults"}


    #Signals
    annotatorStep1Error = pyqtSignal(tuple)#checked1
    annotatorStep1Done = pyqtSignal(tuple)#checked1
    annotatorStep2Error = pyqtSignal(tuple)#checked1
    blastInformations = pyqtSignal(dict, dict, tuple)#checked1
    annotatorStep2Done = pyqtSignal()#checked1


    def annotatorStep1(self, blast, genomes, threads, projectTuple):#checked1
        import itertools
        from math import comb

        project = projectTuple[0]
        projectPath = project.getPath().path()
        for genome in genomes:
            if not project.getGenomesNameLocus()[genome]:
                genomeLocusDict = self.convertFiles(genome, projectPath)
                project.setGenomeNameLocus(genome, genomeLocusDict)
            if not QDir("%s/BLASTresults/%s" %(projectPath, self.dbDirectDict[blast])).entryList(["%s.*" %(genome)], QDir.Files):
                if not self.makeblastdb(genome, blast, projectPath):
                    self.annotatorStep1Error.emit(("Blast Database Error", "An error occured during blast database creation. \
                        For more information check the log file."))

        toWriteFile = QFile("%s/locus.txt" %(projectPath))
        if toWriteFile.open(QIODevice.WriteOnly | QIODevice.Text):
            toWriteOut = QTextStream(toWriteFile)
            for genomeName, locus in project.getGenomesNameLocus().items():
                toWriteOut << genomeName + "\t" + locus + "\n"
                

        noBlastedGenomes = []
        for genome1, genome2 in itertools.combinations(genomes, 2):
            if not project.getAnnotatorStep1Info()[blast][genome1]:
                noBlastedGenomes.append(genome1)
                if not project.getAnnotatorStep1Info()[blast][genome2]:
                    noBlastedGenomes.append(genome2)
                if not self.blastPlus(blast, genome1, genome2, threads, projectPath):
                    self.annotatorStep1Error.emit(("Blast error", "Error was occured during %s-%s blast."
                        %(genome1, genome2)))
                    return
                continue
            elif not project.getAnnotatorStep1Info()[blast][genome2]:
                noBlastedGenomes.append(genome2)
                if not self.blastPlus(blast, genome1, genome2, threads, projectPath):
                    self.annotatorStep1Error.emit(("Blast error", "Error was occured during %s-%s blast."
                        %(genome1, genome2)))
                    return
        for genome in noBlastedGenomes:
            project.setAnnotatorStep1Genome(blast, genome, True)

        self.concatBlastResult(blast, genomes, projectPath)
        self.annotatorStep1Done.emit((project,))


    def annotatorStep2(self, project, userChoices):#checked1
        if userChoices[1] == "_No_":
            if userChoices[2] in project[0].getGenomesNameLocus().values():
                self.annotatorStep2Error.emit(("Unified locus tag already exists",
                    "Unified locus tag entred is one of locus tag genomes of the database."))
            else:
                self.makeGeneAssociationFile(project[0], 
                    project[0].getPath().path(), userChoices[-1], 
                        userChoices[2], userChoices[3])
        else:
            self.makeGeneAssociationFileRefGenome(project[0], 
                project[0].getPath().path(), userChoices[-1], 
                    userChoices[1], userChoices[2], userChoices[3])
        self.makeNewGffFile(project[0], userChoices[0])
        self.annotatorStep2Done.emit()
        

    def annotatorS2BlastInformations(self, project, tickedGenomes):#checked1
        tickedGenomesBlast = {"Blastn" : True, "Blastp" : True}
        noBlastedGenomes = []
        for genome in tickedGenomes:
            if not project[0].getAnnotatorStep1Info()["Blastn"][genome]:
                tickedGenomesBlast["Blastn"] = False
                noBlastedGenomes.append(genome)
            if not project[0].getAnnotatorStep1Info()["Blastp"][genome]:
                tickedGenomesBlast["Blastp"] = False
            elif genome in noBlastedGenomes:
                    noBlastedGenomes.remove(genome)
        
        if tickedGenomesBlast["Blastn"] == False and tickedGenomesBlast["Blastp"] == False:
            self.annotatorStep2Error.emit(("Blast not performed", 
                "Some genomes have been not blasted. "\
                    "The following genomes must be blasted before performing this step:\n"\
                        "%s." %(", ".join(noBlastedGenomes))))
        else:
            self.blastInformations.emit(project[0].getGenomesNameLocus(), 
                tickedGenomesBlast, tickedGenomes)


    def convertFiles(self, genome, projectDir):#checked1
        locusTag = ""
        
        accessProtLocTag = {}
        featureTableFile = QFile("%s/Database/%s/FeatureTable/%s.txt" %(projectDir, genome, genome))
        if featureTableFile.open(QIODevice.ReadOnly | QIODevice.Text):
            featureTableIn = QTextStream(featureTableFile)
            while not featureTableIn.atEnd():
                line = featureTableIn.readLine().strip()
                if line.startswith("#"):
                    continue
                else:
                    
                    line = line.split("\t")
                    if line[0] == "CDS":
                        if "without_" not in line[1]:
                            productAccession = line[10]
                            locusTag = line[16]
                            if "_" in locusTag:
                                accessProtLocTag[productAccession] = locusTag
                            else:
                                self.annotatorStep1Error.emit(("Locus tag format incompatibility", 
                                    "Locus tag format is not supported by the tool. Please choose an other one."))
                                return
        pathsList = ("Database/%s/FFN" %(genome), "Database/%s/FAA" %(genome))
        extensions = (".ffn", ".faa")

        for i, path in enumerate(pathsList):
            toWriteFile = QFile("%s/%s/%s_converted%s" %(projectDir, path, genome, extensions[i]))
            if toWriteFile.open(QIODevice.WriteOnly | QIODevice.Text):
                toReadFile = QFile("%s/%s/%s%s" %(projectDir, path, genome, extensions[i]))
                if toReadFile.open(QIODevice.ReadOnly | QIODevice.Text):
                    toWriteOut = QTextStream(toWriteFile)
                    toReadOut = QTextStream(toReadFile)
                    while not toReadOut.atEnd():
                        line = toReadOut.readLine().strip()
                        if not line.startswith(">"):
                            toWriteOut << line + "\n"
                        elif line.startswith(">lcl"):
                            line = line.split(" ")
                            if "gene=" not in line[1]:
                                locTag = line[1].split("locus_tag=")[-1][:-1]
                            else:
                                locTag = line[2].split("locus_tag=")[-1][:-1]
                            toWriteOut << ">%s\n" %(locTag)
                        else:
                            accessProt = line.split(" ")[0][1:]
                            toWriteOut << ">%s\n" %(accessProtLocTag[accessProt])
        return locusTag.split("_")[0]


    def makeblastdb(self, genome, blastType, projectDir):#checked1
        if not QDir("%s/BLASTresults/%s" %(projectDir, self.dbDirectDict[blastType])).exists():
            QDir("%s/BLASTresults" %(projectDir)).mkpath(self.dbDirectDict[blastType])
        self.process.start("bash", 
            ["-c", "makeblastdb -in %s/Database/%s/%s/%s_converted.%s -out %s/BLASTresults/%s/%s -dbtype %s > %s/BLASTresults/%s/LOG.txt 2>&1"
                %(projectDir, genome, self.cdsDict[blastType], genome, self.cdsDict[blastType].lower(),
                    projectDir, self.dbDirectDict[blastType], genome, 
                    self.dbtypeDict[blastType], 
                    projectDir, self.dbDirectDict[blastType])])
        self.process.waitForFinished(-1)
        if self.process.exitStatus() == 0:
            return True
        else:
            return False
            

    def blastPlus(self, blastType, genome1, genome2, threads, projectDir):#checked1
        blastn = ["-c", "cat %s/Database/%s/%s/%s_converted.%s | "\
                "parallel --no-notice -j %s -k --block 5k --recstart '>' --pipe "\
                "'blastn -query - -db %s/BLASTresults/%s/%s -dust no -max_target_seqs 1 -max_hsps 1 -evalue 1e-10 "\
                "-outfmt \"6 qseqid sseqid bitscore score evalue nident qlen pident positive ppos\" "\
                ">> %s/BLASTresults/%s/%s-%s.%s'"
                    %(projectDir, genome1, self.cdsDict[blastType], genome1, self.cdsDict[blastType].lower(),
                        threads,
                        projectDir, self.dbDirectDict[blastType], genome2,
                        projectDir, self.resultDirecDict[blastType], genome1, genome2, self.resultDirecDict[blastType])]
        
        blastp = ["-c", "cat %s/Database/%s/%s/%s_converted.%s | "\
                "parallel --no-notice -j %s -k --block 5k --recstart '>' --pipe "\
                "'blastp -query - -db %s/BLASTresults/%s/%s -seg no -max_target_seqs 1 -max_hsps 1 -evalue 1e-10 "\
                "-outfmt \"6 qseqid sseqid bitscore score evalue nident qlen pident positive ppos\" "\
                ">> %s/BLASTresults/%s/%s-%s.%s'"
                    %(projectDir, genome1, self.cdsDict[blastType], genome1, self.cdsDict[blastType].lower(),
                        threads,
                        projectDir, self.dbDirectDict[blastType], genome2,
                        projectDir, self.resultDirecDict[blastType], genome1, genome2, self.resultDirecDict[blastType])]
        print(blastType)
        if blastType == "Blastn":
            print(blastn)
            if not QDir(projectDir).exists("BLASTresults/BNresults"):
                QDir(projectDir).mkpath("BLASTresults/BNresults")
            self.process.start("bash", blastn)  
        else:
            if not QDir(projectDir).exists("BLASTresults/BPresults"):
                QDir(projectDir).mkpath("BLASTresults/BPresults")
            self.process.start("bash", blastp)
        self.process.waitForFinished(-1)
        if self.process.exitStatus() == 0:
            return True
        else:
            return False


    def concatBlastResult(self, blastType, genomesList, projectDir):#checked1
        toWriteFile = QFile("%s/BLASTresults/%s/concat.txt" %(projectDir, self.resultDirecDict[blastType]))
        if toWriteFile.open(QIODevice.WriteOnly | QIODevice.Text):
            toWriteOut = QTextStream(toWriteFile)
            for blastResult in QDir("%s/BLASTresults/%s" %(projectDir, self.resultDirecDict[blastType])).entryList(
                ["*.%s" %(self.resultDirecDict[blastType])], QDir.Files):
                    toReadFile = QFile("%s/BLASTresults/%s/%s" %(projectDir, self.resultDirecDict[blastType], blastResult))
                    if toReadFile.open(QIODevice.ReadOnly | QIODevice.Text):
                        toReadOut = QTextStream(toReadFile)
                        print(toReadOut)
                        toWriteOut << toReadOut.readAll()

                    
    def makeGeneAssociationFile(self, project, projectPath, desiredBlast, unifieduserChoices, threshold):#checked1
        import networkx as nx

        graph = nx.Graph()
        toReadFile = QFile("%s/BLASTresults/%s/concat.txt" %(projectPath, self.resultDirecDict[desiredBlast]))
        if toReadFile.open(QIODevice.ReadOnly | QIODevice.Text):
            toReadOut = QTextStream(toReadFile)
            while not toReadOut.atEnd():
                line = toReadOut.readLine().strip().split("\t")
                if float(line[-1]) >= threshold:
                    graph.add_edge(line[0], line[1])
            nx.write_gexf(graph, "%s/graph.gexf" %(projectPath), encoding="utf-8", prettyprint=True, version="1.1draft")

        locusTuple = tuple(project.getGenomesNameLocus().values())
        components = nx.connected_components(graph)
        toWriteFile = QFile("%s/geneAssociation.tsv" %(projectPath))
        if toWriteFile.open(QIODevice.WriteOnly | QIODevice.Text):
            output = ""
            toWriteIn = QTextStream(toWriteFile)
            for newLocus, network in enumerate(components):
                networkTagList = []
                copies = 0
                output += "%s_%d\t" %(unifieduserChoices, newLocus)
                for locus in locusTuple:
                    presentLocus = []
                    duplicatedGenes = []
                    for homologue in network:
                        if locus in homologue:
                            tag = homologue.split("_")[0]
                            if tag not in networkTagList and not duplicatedGenes:
                                networkTagList.append(tag)
                                presentLocus.append(homologue)
                            else:
                                duplicatedGenes.append(homologue)
                                if presentLocus:
                                    for geneToRemove in presentLocus:
                                        if tag in geneToRemove:
                                            presentLocus.remove(geneToRemove)
                                            copies += 1
                                            toWriteIn << "%s_%d.%d\t%s\n" %(unifieduserChoices, newLocus, copies, geneToRemove)
                                            break
                                copies += 1
                                toWriteIn << "%s_%d.%d\t%s\n" %(unifieduserChoices, newLocus, copies, homologue)
                    if len(duplicatedGenes) > 0:
                        for gene in duplicatedGenes:
                            output += gene + ","
                        output = output[:-1] + "\t"
                    elif presentLocus:
                        output += presentLocus[0] + "\t"
                    else:
                        output += "-\t"
                output += "\n"
            toWriteIn << output


    def makeGeneAssociationFileRefGenome(self, project, projectPath, desiredBlast, refLocus, unifieduserChoices, threshold):#checked1
        import networkx as nx

        locusSpecieDict = tuple(project.getGenomesNameLocus().values())

        graph = nx.Graph()
        toReadFile = QFile("%s/BLASTresults/%s/concat.txt" %(projectPath, self.resultDirecDict[desiredBlast]))
        if toReadFile.open(QIODevice.ReadOnly | QIODevice.Text):
            toReadOut = QTextStream(toReadFile)
            while not toReadOut.atEnd():
                line = toReadOut.readLine().strip().split("\t")
                if float(line[-1]) >= threshold:
                    graph.add_edge(line[0], line[1])
            nx.write_gexf(graph, "%s/graph.gexf" %(projectPath), encoding="utf-8", prettyprint=True, version="1.1draft")
        
        components = nx.connected_components(graph)
        toWriteFile = QFile("%s/geneAssociation.tsv" %(projectPath))
        if toWriteFile.open(QIODevice.WriteOnly | QIODevice.Text):
            toWriteIn = QTextStream(toWriteFile)
            i = 1
            choosenLocus = refLocus.split(" - ")[-1]
            for network in components:
                ourLocusTagList = []
                locusLTDict = {}
                for homologue in network:
                    if choosenLocus in homologue:
                        ourLocusTagList.append(homologue)
                    else:
                        locus = homologue.split("_")[0]
                        if locus in locusLTDict:
                            locusLTDict[locus].append(homologue)
                        else:
                            locusLTDict[locus] = [homologue,]
                outputLine = ""
                if len(ourLocusTagList) == 0:
                    outputLine += "%s_%s%d\t" %(unifieduserChoices, ("0"*(5-len(str(i)))), i)
                    i += 1
                else:
                    for ourLocusTag in ourLocusTagList:
                        outputLine += ourLocusTag + ","
                    outputLine = outputLine[:-1] + "\t"
                for locus in locusSpecieDict:
                    if locus in locusLTDict:
                        for locusTag in locusLTDict[locus]:
                            outputLine += locusTag + ","
                        outputLine = outputLine[:-1] + "\t"
                    elif locus != choosenLocus:
                        outputLine += "-\t"
                toWriteIn << outputLine.strip() + "\n"


    def makeNewGffFile(self, project, tickedGenomes):#checked1
        print(project)
        def replaceParser(featureTableLine, accessionLocusDict):
            accessionLocusDict[featureTableline.strip().split("\t")[10]] = featureTableline.strip().split("\t")[16]

        geneAssociationDict = {}
        toReadFile = QFile("%s/geneAssociation.tsv" %(project.getPath().path()))
        if toReadFile.open(QIODevice.ReadOnly | QIODevice.Text):
            toReadOut = QTextStream(toReadFile)
            while not toReadOut.atEnd():
                line = toReadOut.readLine().strip().split("\t")
                for locusTag in line[1:]:
                    if locusTag != "-" and locusTag != "":
                        geneAssociationDict[locusTag] = line[0]

        for genome in tickedGenomes:
            accessionLocusDict = {}
            toReadFile = QFile("%s/Datbase/%s/FeatureTable/%s.txt" %(project.getPath().path(), genome, genome))
            if toReadFile.open(QIODevice.ReadOnly | QIODevice.Text):
                toReadOut = QTextStream(toReadFile)
                line = toReadOut.readLine()
                if not line.startswith("#"):
                    replaceParser(line, accessionLocusDict)
                while not toReadOut.atEnd():
                    replaceParser(toReadOut.readLine().strip(), accessionLocusDict)
           

            toWriteFile = QFile("%s/Database/%s/GFF/%s_ANO.gff" %(project.getPath().path(), genome, genome))
            if toWriteFile.open(QIODevice.WriteOnly | QIODevice.Text):
                toReadFile = QFile("%s/Database/%s/GFF/%s.gff" %(project.getPath().path(), genome, genome))
                if toReadFile.open(QIODevice.ReadOnly | QIODevice.Text):
                    toReadOut = QTextStream(toReadFile)
                    toWriteIn = QTextStream(toWriteFile)
                    while not toReadOut.atEnd():
                        line = toReadOut.readLine()
                        
                        if ("ID=" in line) and ("Parent=" not in line):
                            fragmentedBigLine = line.strip().split("\t")
                            fragmentedLastElem = fragmentedBigLine[-1].split(";")
                            genomeId = fragmentedLastElem[0].split("ID=")[-1]
                            if "-" in genomeId:
                                genomeId = genomeId.split("-")[-1]
                            if genomeId in accessionLocusDict and accessionLocusDict[genomeId] in geneAssociationDict:
                                fragmentedLastElem[0] = "ID=" + geneAssociationDict[accessionLocusDict[genomeId]]
                            elif genomeId in geneAssociationDict:
                                fragmentedLastElem[0] = "ID=" + geneAssociationDict[genomeId]
                            else:
                                toWriteIn << line + "\n"
                                continue
                            fragmentedBigLine[-1] = ";".join(fragmentedLastElem)
                            toWriteIn << "\t".join(fragmentedBigLine) + "\n"
                        elif ("ID=" in line) and ("Parent=" in line) and ("CDS" in line):
                            fragmentedBigLine = line.strip().split("\t")
                            fragmentedLastElem = fragmentedBigLine[-1].split(";")
                            genomeId = fragmentedLastElem[1].split("Parent=")[-1]
                            print(genomeId)
                            if "-" in genomeId:
                                genomeId = genomeId.split("-")[-1]
                            if genomeId in accessionLocusDict and accessionLocusDict[genomeId] in geneAssociationDict:
                                fragmentedLastElem[0] = "ID=" + geneAssociationDict[accessionLocusDict[genomeId]]
                            elif genomeId in geneAssociationDict:
                                fragmentedLastElem[0] = "ID=" + geneAssociationDict[genomeId]
                            else:
                                toWriteIn << line + "\n"
                                continue
                            fragmentedBigLine[-1] = ";".join(fragmentedLastElem)
                            toWriteIn << "\t".join(fragmentedBigLine) + "\n"
                        elif line.startswith("#"):
                            toWriteIn << line + "\n"
                    project.setAnnotatorStep2Genome(genome, True)

