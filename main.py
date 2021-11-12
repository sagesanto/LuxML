from typing import Any
import json
from json import JSONEncoder
import numpy as np
import pandas as pd
import scipy
import matplotlib
import base64
import math, sys
import subprocess
import shlex
import pygame
from scipy.optimize import minimize, rosen, rosen_der

summaryFrame = pd.DataFrame()
batchNumber = 0


def readJson(dump):
    enc = json.loads(dump)
    dataArray = enc
    # print("data array in LuxML:", dataArray)
    return dataArray


def readFromFile(filename):
    with open(filename, 'r') as f:
        last_line = f.readlines()[-1]
    return last_line


def getResults():
    encResults = readFromFile("C:/LuxAI/rexai/scores.txt")
    score = readJson(encResults)
    return score


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def encodeJson(inputLists):
    # nparray = {"array":nparray}
    # print(type(inputLists))
    # print(inputLists.dtype)
    # print(inputLists.shape)
    return json.dumps(inputLists, cls=NumpyArrayEncoder)


# [str(nparray.dtype), nparray.to_list(), nparray.shape]


def writeToFile(filename, string):
    with open(filename, 'a') as f:
        f.write(string + '\n')


def overwriteFile(filename, string):
    with open(filename, 'w') as f:
        f.write(string)


def writeInstructions(inputLists):
    inputString = encodeJson(inputLists)
    print("inputString from write:", inputString)
    writeToFile("C:/LuxAI/rexai/instructions.txt", inputString)


def runGame(inputLists):
    global batchNumber
    global summaryFrame
    batchNumber += 1
    writeInstructions(inputLists)
    command = "C:/Users/Student/AppData/Roaming/npm/lux-ai-2021.cmd C:/LuxAI/simple/main.py C:/LuxAI/rexAI/main.py --maxtime 3000 --out replay.json"
    args = shlex.split(command)
    score = 0
    gamesPerBatch = 20
    for i in range(gamesPerBatch):
        proc = subprocess.Popen(args)
        while proc.returncode is None:
            proc.poll()
        score = score - getResults()
    summaryFrame = summaryFrame.append(
        {"batch": batchNumber, "averageScore": score / gamesPerBatch, "parameters": inputLists}, ignore_index=True)

    overwriteFile("C:/Users/Student/PycharmProjects/LuxML/summary.csv", str(summaryFrame.to_csv()))
    print(summaryFrame)
    return -1 * (score / gamesPerBatch)


array = np.array([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]], dtype="int64")


def con(x):
    return max[x - int(x)] == 0


cons = ({'type': 'eq', 'fun': lambda x: max([x[i] - int(x[i]) for i in range(len(x))])})
res = scipy.optimize.minimize(runGame, array, method="COBYLA", options = {"rhobeg" : 5})
output = str(
    "result:" + res.x + "success:" + res.success + "message:" + res.message + "iterations:" + res.nit + "lastScore:" +
    getResults())
writeToFile("C:/LuxAI/rexai/scores.txt", output)
print(output)
