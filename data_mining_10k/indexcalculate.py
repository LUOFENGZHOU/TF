# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 16:00:06 2019

@author: zlf
"""
import glob
import numpy as np
import pandas as pd
import re
from settings import *


def strategy_cal():
    prefix = "\W"
    DStrategicpositioning = ["differenti", "unique", "superior", "premium", "high[a-z]*\s*margin",
                             "high[a-z]*\s*price", "high[a-z]*\s*end", "inelasticity"]
    DProductinnovation = ["new[a-z]*\s*product", "innovat", "creativ", "research and development",
                          "R&D", "techni", "technolog", "patent", "quality", "reliab", "durable"]
    DCustomerintimacy = ["marketing", "advertis", "brand", "reputation", "trademark", "customer[a-z]*\s*service",
                         "consumer[a-z]*\s*service", "customer[a-z]*\s*need", "sales\s*support",
                         "post.purchase\s*service",
                         "customer\s*preference", "c\s*preference", "loyalty", "customiz", "personaliz", "responsive"]
    DHumanresources = ["talent", "train", "skill", "intellectual[a-z]*\s*propert", "human\s*capital"]
    CStrategicpositioning = ["cost\s*leader", "low[a-z]*\s*pric", "low[a-z]*\s*cost", "cost\s*advantage",
                             "aggressive\s*pric"]
    CCostcontrol = ["control[a-z]*\s*cost", "control[a-z]*\s*expense", "control[a-z]*\s*overhead",
                    "minimiz[a-z]*\s*cost",
                    "minimiz[a-z]*\s*expense", "minimiz[a-z]*\s*overhead", "reduc[a-z]*\s*cost",
                    "reduc[a-z]*\s*expense",
                    "reduc[a-z]*\s*overhead", "sav[a-z]*\s*cost", "improv[a-z]*\s*cost", "cut[a-z]*\s*cost",
                    "cut[a-z]*\s*expense", "cut[a-z]*\s*overhead", "decrease[a-z]*\s*cost", "decrease[a-z]*\s*expense",
                    "decrease[a-z]*\s*overhead", "monitor[a-z]*\s*cost", "monitor[a-z]*\s*expense",
                    "monitor[a-z]*\s*overhead"]
    COperationefficiency = ["efficien", "high[a-z]*\s*yield", "process[a-z]*\s*improvement",
                            "asset[a-z]*\s*utilization",
                            "capacity[a-z]*\s*utilization"]
    CEconomiesofscale = ["scope", "scale", "breath", "broad", "mass", "high[a-z]*\s*volume", "large[a-z]*\s*volume"]
    DList = [DStrategicpositioning, DProductinnovation, DCustomerintimacy, DHumanresources]
    CList = [CStrategicpositioning, CCostcontrol, COperationefficiency, CEconomiesofscale]
    DInd = np.zeros(4)
    CInd = np.zeros(4)
    filelist = glob.glob(STRATEGY_SAVE_DIR + "*wordlist.csv")

    for file in filelist:
        log = {"Name": [], "Year": [], "CIK": [], "Date": [], "MainPart": [], "DS": [], "DP": [], "DC": [], "DH": [],
               "CS": [], "CC": [], "CO": [], "CE": []}
        readfile = pd.read_csv(file, sep="\x02")
        year = file[0:4]
        enumerator2 = 0
        enumerator3 = 0
        log["Name"].extend(readfile["FileName"])
        for i in range(len(readfile["FileName"])):
            enumerator2 += 1
            if enumerator2 == 1000:
                print(str(enumerator2 + enumerator3 * 1000) + " times have passed.")
                enumerator2 = 0
                enumerator3 += 1
            rawdata = readfile["MainPart"][i]
            filename = readfile["FileName"][i]
            log["Year"].append(year)
            pattern = re.compile("data_([0-9]*)_", re.S | re.I)
            log["CIK"].append(re.findall(pattern, filename)[0])
            log["MainPart"].append(rawdata)
            log["Date"].append(filename[0:8])
            dtemp = np.zeros(4)
            ctemp = np.zeros(4)
            enumerator = 0
            for k in DList:
                tempt = 0
                for w in k:
                    pattern = re.compile(prefix + w, re.S | re.I)
                    count = re.findall(pattern, rawdata)
                    tempt += len(count)
                dtemp[enumerator] = tempt
                enumerator += 1
            enumerator = 0
            for k in CList:
                tempt = 0
                for w in k:
                    pattern = re.compile(prefix + w, re.S | re.I)
                    count = re.findall(pattern, rawdata)
                    tempt += len(count)
                ctemp[enumerator] = tempt
                enumerator += 1
            log["DS"].append(dtemp[0])
            log["DP"].append(dtemp[1])
            log["DC"].append(dtemp[2])
            log["DH"].append(dtemp[3])
            log["CS"].append(ctemp[0])
            log["CC"].append(ctemp[1])
            log["CO"].append(ctemp[2])
            log["CE"].append(ctemp[3])
        print("Year " + str(year) + " is over!")
        output = pd.DataFrame(log)
        output.to_csv(STRATEGY_SAVE_DIR + str(year) + "_processed.csv")
