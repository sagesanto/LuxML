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
    dataArray = enc
    print("data array in LuxML:",dataArray)
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
    nparray = np.array([inputLists], dtype=object)
    print("encode:",base64.b64encode(nparray).decode('utf-8'))
    return json.dumps([str(nparray.dtype), nparray.tolist(), nparray.shape])


def writeToFile(filename, string):
    with open(filename, 'a') as f:
        f.write(string+ '\n')


def writeInstructions(inputLists):
    inputString = encodeJson(inputLists)
    print(inputString)
    writeToFile("C:/LuxAI/rexai/gameDataAndResults.txt", inputString)


def runGame(inputLists):
    writeInstructions(inputLists)
    command = "C:/Users/Student/AppData/Roaming/npm/lux-ai-2021.cmd C:/LuxAI/simple/main.py C:/LuxAI/rexAI/main.py --maxtime 3000 --out replay.json"
    args = shlex.split(command)
    print(args)
    proc = subprocess.Popen(args)
    while proc.returncode is None:
        proc.poll()
    return getResults()


score = runGame([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
print("score:",score)
