#!/bin/python3

from ast import IsNot
from curses.ascii import isdigit
from fileinput import filename
from PyQt5.QtCore import QObject, QFile, QIODevice, QTextStream, QDir, QProcess, pyqtSignal
import subprocess, os, fnmatch
import pandas as pd
import csv


class homolog(QObject):

    def __init__(self):
        super().__init__(None)
        self.process = QProcess(self)
    
    annotatorStep2Done = pyqtSignal()#checked1

    def getProteinHomolog(self, project, tickedGenomes, threads, get_method, get_Lt, get_similarity):

        
        project = project[0]
        projectPath = project.getPath().path()
        folder = "protein_files"
        tmp = os.path.join(projectPath, folder)
        if not os.path.exists(tmp):
            os.mkdir(tmp) 
        else:
            deleteFolder = 'rm -r "%s"' % (tmp)
            commandRun = subprocess.call(deleteFolder, shell=True)
            os.mkdir(tmp)
            
            for genomes in tickedGenomes:
                for root, dirnames, filenames in os.walk(projectPath):
                    for faa in fnmatch.filter(filenames,'*.faa'):
                        if genomes in faa:
                            protfile = os.path.join(projectPath, "Database", genomes, 'FAA', faa)
                            if "converted" in protfile:
                                cmd = 'cp "%s" "%s"' % (protfile, tmp)
                                status = subprocess.call(cmd, shell=True)
                            
        myDir = os.path.join(os.getcwd(), "protein_files_homologues")
      
        if os.path.isdir(myDir):
            deleteFolder = 'rm -r "%s"' % (myDir)
            commandRun = subprocess.call(deleteFolder, shell=True)
       
        #gethomologpath = input("Enter absolute path of GetHomologues: ")
        gethomologpath = input("Enter absolute path for GET_HOMOLOGOUS: ")
        
        if get_method == "BDBH":
            result = subprocess.run(["perl", gethomologpath, "-d", tmp, "-n", threads, "-S", get_similarity])
        elif get_method == "OMCL":
            result = subprocess.run(["perl", gethomologpath, "-d", tmp, "-t", "0", "-M", "-n", threads, "-S", get_similarity])
        elif get_method == "COG":
            result = subprocess.run(["perl", gethomologpath, "-d", tmp, "-t", "0", "-G", "-n", threads])

        

        # This is the directory of getHomolog result folder
        #myDir = "/home/mac/Documents/Garima/Neisseriacinerea_dmd_f0_0taxa_algOMCL_e0_S55_"
        
        for files in os.listdir(myDir):
            if "taxa" in files and "cluster" not in files:
                myDir = os.path.join(myDir, files)
        # Path to the getHomolog input folder
        #mypath = "/home/mac/Documents/Garima/Phylogeny/protein"
        mypath = tmp
        
        #Dictionary to store the genome locus tag as keys and file name as values
        locusVsGenomeFileDict = {}
        #genomeFileNameVsLocusTag = {}
        genomeFileNames = []
        
        for name in os.listdir(mypath):
            tmp = os.path.join(mypath, name)
            f2 = open(tmp, "r")
            line = f2.readline().rstrip()
            if line.startswith(">"):
                locus = line[1: line.rfind("_")] 
                #locus = line.split(">")[1]
                locusVsGenomeFileDict[locus] = name
                #genomeFileNameVsLocusTag[name] = []
                genomeFileNames.append(name)
        


        #open csv file to write 
        tsvFilePath = os.path.join(projectPath, "geneAssociation.tsv")
        fileCSV = open(tsvFilePath, "w")
        writer = csv.writer(fileCSV, delimiter='\t')
        writer.writerow(["ID"] + genomeFileNames)
        unifiedLocusTagSuffix = 1
        for proteinFile in os.listdir(myDir):
            genomeFileNameVsLocusTag = {}
            for genomeFileName in genomeFileNames:
                genomeFileNameVsLocusTag[genomeFileName] = []
            maxRowCount = 0

            unifiedLocusTag = get_Lt + "_" + str(float(unifiedLocusTagSuffix))
            unifiedLocusTagSuffix = unifiedLocusTagSuffix + 1

            tmpProt = os.path.join(myDir, proteinFile)
            f = open(tmpProt, "r")
            #f = open("/home/mac/Documents/Garima/Annotator-test/protein_files_homologues/Afili_f0_0taxa_algOMCL_e0_/4_JOMKLAGE_00004.faa", "r")
            lines = f.readlines()
            for line in lines:
                if line.startswith(">"):
                    locusTag = line.split(" ")[0]
                    locusTag = locusTag.split(">")[1]
                   # locus = locusTag.split("_")[0]
                    locus = locusTag[0:locusTag.rfind("_")]
                    if locus in locusVsGenomeFileDict:
                        genomeFile = locusVsGenomeFileDict[locus]
                        genomeFileNameVsLocusTag[genomeFile].append(locusTag)
                        length = len(genomeFileNameVsLocusTag[genomeFile])
                        if length > maxRowCount:
                            maxRowCount = length
                            
            for row in range(0, maxRowCount):
                statusList = ["-"] * len(genomeFileNames)  
                index = 0
                for fileName in genomeFileNames:
                    if len(genomeFileNameVsLocusTag[fileName]) != 0:
                        listLocusTags = genomeFileNameVsLocusTag[fileName]
                        if len(listLocusTags) > row:
                            statusList[index] = listLocusTags[row]
                          #  genomeFileNameVsLocusTag[fileName] = "-"
                    index = index + 1

                if maxRowCount > 1:
                    writer.writerow([unifiedLocusTag + "_" + str(row + 1)] + statusList)
                else:
                    writer.writerow([unifiedLocusTag] + statusList)
            
            
            
          
        from lib.models.annotator import Annotator
        theClass = Annotator()
        theClass.makeNewGffFile(project, tickedGenomes)
        self.annotatorStep2Done.emit()    

        



       



        '''
        genome_list = []
        protein_list = []
        with open("genome_list.txt", "w") as g:

            for file in os.listdir(mypath):
                path_content = file.split('.')
                file_name = path_content[0].split('/')[-1]
                genome_list.append(file_name)
            


        for protein_file in os.listdir(myDir):
            protein_content = protein_file.split('.')
            protein_name = protein_content[0].split('/')[-1]
            n = protein_name.split('_', 1)[-1]
            protein_list.append(n)

        myDict = {}

        
        with open("my.csv", "w") as f:
            writer = csv.writer(f)
            
            writer.writerow(["ID"] + genome_list)
            for x in protein_list:
                writer.writerow([x])

                
                
            
            
        f.close()
            
       

        with open("genomeTagList.txt", "w") as f1:
            # We take the name of the file (genome name) and the genome tag
            for name in os.listdir(mypath):
                tmp = os.path.join(mypath, name)
                print(name)
                f2 = open(tmp, "r")
                line = f2.readline().rstrip()
                if line.startswith(">"):
                    line = name + " " + line.split("_")[0] 
                f1.write(line + "\n")
                f2.close()
        
        def makeLocusList(fileName):   # Ok
            """
            Take the result of makeGenomeNamesAndLocusList and 
            create a locus list for genomes
            """
            
            """
            Take the result of makeGenomeNamesAndLocusList and 
            create a locus list for genomes
            """
            #myDir = "/home/mac/Documents/Garima/Neisseriacinerea_dmd_f0_0taxa_algOMCL_e0_S55_/"
            #os.chdir(myDir)
            genomeLocusList = []
            with open(fileName, "r") as f1: 
                while 1:
                    line = f1.readline().rstrip() 
                    if line == "":
                        break
                    line = line.split(">")[1]
                    genomeLocusList.append(line)
            
            return genomeLocusList 

        def makeProteinList():   # Ok
            proteinLocusList = []
            for each_file in os.listdir(myDir):
                protein_content = each_file.split('.')
                protein_name = protein_content[0].split('/')[-1]
                n = protein_name.split('_', 1)[-1]
                proteinLocusList.append(n)
            return proteinLocusList

        newDict = {}
        genomeTagDict = {}
        proteinTagList = makeProteinList()
        print(proteinTagList)
        genomeTagList = makeLocusList("genomeTagList.txt")
        print(genomeTagList)
        for genomeTag in genomeTagList:
            newDict[genomeTag] = []
        #myDir = "/home/mac/Documents/Garima/Neisseriacinerea_dmd_f0_0taxa_algOMCL_e0_S55_"
        #os.chdir(myDir)
        
        for genomeTag in genomeTagList:
            genomeTagDict[genomeTag] = [] 
            
        for genokey in genomeTagDict.keys():   
            for file in os.listdir("/home/mac/Documents/Garima/Neisseriacinerea_dmd_f0_0taxa_algOMCL_e0_S55_/"):
                if file.endswith(".faa"):
                    proteinkey = file.split(".")[0]
                    if os.path.exists(file):
                        with open(file, "r") as f1:
                            while 1:
                                line = f1.readline().rstrip()
                                if line == "":
                                    break
                                if line.startswith(">ID:X:"):
                                    myValue = (line.split("|")[0]).split(":")[2]
                                    if genokey in myValue:
                                        genomeTagDict[genokey].append(myValue)
                                    
                                if line.startswith(">") and "ID:X:" not in line:
                                    myValue = (line.split("|")[0]).split(":")[1]
                                    if genokey in myValue:
                                        genomeTagDict[genokey].append(myValue)
                                        
        for proteinTag in proteinTagList:
            for file in os.listdir("/home/mac/Documents/Garima/Neisseriacinerea_dmd_f0_0taxa_algOMCL_e0_S55_/"):
                if file.endswith(".faa"):
                    name = file.split(".")[0]
                    if name == proteinTag:
                        if os.path.exists(file):
                            with open(file, "r") as f1:
                                while 1:
                                    line = f1.readline().rstrip()
                                    if line == "":
                                        break
                                    for key, value in genomeTagDict.items():
                                        if line.startswith(">ID") and key in line:
                                            for i in range(len(value)):
                                                myValue = value[i]
                                                if myValue in line:
                                                    newDict[key].append(myValue)
        print(newDict)
        df = pd.DataFrame(newDict, columns = genomeTagList, index = proteinTagList)
        df.to_csv("getHomologAssociation_test.tsv", sep="\t")                         
    print("finished")
   '''     
