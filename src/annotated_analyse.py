import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math

def getStallingCounts(dateipfad):
    df = pd.read_csv(dateipfad)
    stallingCount = 0
    for _, row in df.iterrows():
        if (df.loc[row, 'stalling'] == "1"):
            stallingCount = stallingCount + 1
    return stallingCount
def getStalllingRequests(dateipfad):
    df = pd.read_csv(dateipfad)
    stalllingRequests = [];
    for _, row in df.iterrows():
        if (df.loc[row, 'stalling'] == "1"):
            stalllingRequests.append(df.loc[row, 'requestStart'])

    return stalllingRequests

def getStallingDuration(dateipfad):
    df = pd.read_csv(dateipfad)
    stallingTime = 0
    for _, row in df.iterrows():
        if (df.loc[row, 'stalling'] == "1"):
            stallingTime = stallingTime + df.loc[row, 'duration']
    return stallingTime

def getDuration(dateipfad):
    df = pd.read_csv(dateipfad)
    duration = 0
    for _, row in df.iterrows():
        duration = duration + df.loc[row, 'duration']
    return duration


def getQuality(dateipfad, resquestStart):
    df = pd.read_csv(dateipfad)
    for _, row in df.iterrows():
        if (df.loc[row, 'resquestStart'] == resquestStart):
            return df.loc[row, 'quality']
    return 0

def getQualityAverage(dateipfad):
    df = pd.read_csv(dateipfad)
    qualitysum = 0
    for _, row in df.iterrows():
        qualitysum = qualitysum + df.loc[row, 'quality']

    return qualitysum/len(df)

def getQualityChangeCount(dateipfad):
    df = pd.read_csv(dateipfad)
    qualityChangeCount = 0
    for _, row in df.iterrows():
        if (df.loc[row, 'qc'] == "1"):
            qualityChangeCount = qualityChangeCount + 1

    return qualityChangeCount

def getQualityChanges(dateipfad):
    df = pd.read_csv(dateipfad)
    qualityChanges = []
    for _, row in df.iterrows():
        if (df.loc[row, 'qc'] == "1"):
            qualityChanges.append(df.loc[row, 'requestStart'])

    return qualityChanges






