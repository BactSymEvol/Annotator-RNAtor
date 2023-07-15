#!/bin/python3

from PyQt5.QtCore import QDir, QFile, QIODevice, QTextStream, QFileInfo
from lib.models.project import Project
import json

def writeCache(project):
    projectCacheFile = QFile("%s/Cache/project.cache" %(project.getPath().path()))
    if projectCacheFile.open(QIODevice.WriteOnly | QIODevice.Text):
        projectCacheOut = QTextStream(projectCacheFile)
        projectCacheOut << "Project path:\t%s\n" %(project.getPath().path())
        projectCacheOut << "Genomes:\t"
        tmp = ""
        for genome in project.getGenomes():
            tmp += genome + ","
        if tmp:
            projectCacheOut << "%s\n" %(tmp[:-1])
        else:
            projectCacheOut << "-\n"
        projectCacheOut << "Annotator step1:\t" + json.dumps(project.getAnnotatorStep1Info()) + "\n"
        projectCacheOut << "Annotator step2:\t" + json.dumps(project.getAnnotatorStep2Info()) + "\n"
        projectCacheOut << "RNAtor step1:\t" + json.dumps(project.getRNAtorStep1Info()) + "\n"
        projectCacheOut << "RNAtor step2:\t" + json.dumps(project.getRNAtorStep2Info()) + "\n"
        


def checkProjectCache(projectPath):
    if QFileInfo.exists("%s/Cache/project.cache" %(projectPath)):
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
                elif "Annotator step1:" in line:
                    toReturn.append(json.loads(line[-1]))
                elif "Annotator step2:" in line:
                    toReturn.append(json.loads(line[-1]))
                elif "RNAtor step1:" in line:
                    toReturn.append(json.loads(line[-1]))
                elif "RNAtor step2:" in line:
                    toReturn.append(json.loads(line[-1]))
                else:
                    return
            return tuple(toReturn)
        else:
            return
    else:
        return


        

