from typing import Any
import json
import numpy as np
import pandas as pd
import sklearn
import matplotlib
import base64
import math, sys
import subprocess
import shlex
import pygame

def readJson(dump):
    enc = json.loads(dump)
    dataType = np.dtype(enc[0])
    dataArray = np.frombuffer(base64.decodestring(enc[1]), dataType)
    if len(enc) > 2:
        dataArray.reshape(enc[2])
    return dataArray


def readFromFile(filename):
    with open(filename, 'r') as f:
        last_line = f.readlines()[-1]
    return last_line


def getResults():
    encResults = readFromFile("C:/LuxAI/rexai/gameDataAndResults.txt")
    score = readJson(encResults)
    return score


def encodeJson(inputLists):
    nparray = np.array([inputLists[0],inputLists[1],inputLists[2],inputLists[3]],dtype=object)
    return json.dumps([str(nparray.dtype), base64.b64encode(nparray), nparray.shape])

def writeToFile(filename, string):
    with open(filename, 'a') as f:
        f.write(string)


def writeInstructions(inputLists):
    inputString = encodeJson(inputLists)
    print(inputString)
    writeToFile("gameDataAndResults.txt", inputString)

def runGame(inputLists):
    writeInstructions(inputLists)
    command = "C:/Users/Student/AppData/Roaming/npm/lux-ai-2021.cmd C:/LuxAI/simple/main.py C:/LuxAI/rexAI/main.py --out replay.json"
    args = shlex.split(command)
    print(args)
    proc = subprocess.Popen(args)
    while proc.returncode is None:
        proc.poll()
    return getResults()


score = runGame([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
print(score)