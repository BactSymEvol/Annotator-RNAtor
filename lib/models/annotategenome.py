#!/bin/python3

from PyQt5.QtCore import QObject, QFile, QIODevice, QTextStream, QDir, QProcess, pyqtSignal
import subprocess, os, fnmatch


class AnnotateGenome(QObject):

    def __init__(self):
        super().__init__(None)
        self.process = QProcess(self)
        self.directories = ("FFN", "FNA", "FAA", "GFF", "FeatureTable")
        self.fileExtensions = ("ffn", "fna", "faa", "gff", "txt")
        self.realExtensions = ("_cds_from_genomic.fna", "_genomic.fna", "_protein.faa", 
            "_genomic.gff", "_feature_table.txt")
        
    #Signals
    addGenomeDone = pyqtSignal(str)#checked1
    annotateStepDone = pyqtSignal(tuple)#checked1

    def annotategen(self, project, tickedGenomes, threads, genomeFolderPath):
        varProject = project
        project = project[0]
        projectPath = project.getPath().path()
        os.chdir(genomeFolderPath)
        #file = os.path.join(genomeFolderPath, file)
        #command = ["sed", "-i", '"s/^>.*/>${file%%.*}/"', '"$file"']
        #for file in os.list(genomeFolderPath):
         #   output  = subprocess.call(['sed', '-i', 's/^>.*/>${file%%.*}/', '$file'])
        processes = []
        prokkapath = input("Enter absolute path of prokka: ")
        genomeAnnotation = os.path.join(projectPath, "Annotation")
        genomeInformation = {}
        for genome in tickedGenomes:
            genomeFilePath = []
            genomeFilePath = os.path.join(genomeFolderPath, genome + '.' + 'fna')
            outputPath = os.path.join(genomeAnnotation, genome)
            result = subprocess.Popen([prokkapath, "--outdir", outputPath, "--prefix", genome, "--cpus", threads, "--force", genomeFilePath])
            processes.append(result)
        for p in processes:
            p.wait()
        self.annotateStepDone.emit((project,))    

    
    

                        
                        
           
