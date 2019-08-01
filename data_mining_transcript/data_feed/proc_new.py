# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:35:04 2019

@author: Luofeng

Input:
    out_new.tsv (sep = "\t"): it is a manually modified version of "out.csv" from script "preproc.py".
    
Output:
    out_proc.csv, recording fisical year and month and announcement datetime.
    out_proc.tsv
    out_proc.xlsx
"""

import pandas as pd
import re


def delete_space(string):
    """
    Delete Space from the two sides.
    """
    try:
        while string[0] == " ":
            assert len(string) > 1
            string = string[1:]
        while string[-1] == " ":
            assert len(string) > 1
            string = string[:-1]
        return string
    except: # Null string input exception (insubscriptable exception)
        return ""
def delete_nulllist(lol):
    '''
    Delete null list in a lol (list of list).
    '''
    for i in lol:
        if i != []:
            return i[0]
    return "NOT FOUND"
yearlist = [_ for _ in range(2000, 2020)] # Full year
mainlist = pd.read_csv("out_new.tsv", sep = "\t", encoding = "utf-8")
year_pattern = re.compile("20[0-9][0-9]")
quarter_pattern = re.compile("Q[1-4]")
date_pattern = re.compile(" *?[0-9]*?[0-9],")
fylist = [] #
fqlist = [] #
ancylist = []
ancmlist = []
ancdlist = []
anctlist = [] #
mlist = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
for i in range(len(mainlist["Num"])):
    flag = 0
    fy = re.findall(year_pattern, mainlist["FileName"][i])
    fq = re.findall(quarter_pattern, mainlist["FileName"][i])
    if len(fy) == 1:
        fylist.append(fy[0])
    else:
        fylist.append("ERROR")
    if len(fq) == 1:
        fqlist.append(fq[0])
    else:
        fqlist.append("ERROR")
    anctlist.append(delete_space(mainlist["DateTime"][i][-8:]))
    ancy = re.findall(year_pattern, mainlist["DateTime"][i])
    ancm = delete_nulllist([re.findall(j, mainlist["DateTime"][i]) for j in mlist])
    ancd = delete_space(re.findall(date_pattern, mainlist["DateTime"][i])[0][:-1])
    if len(ancy) == 1:
        ancylist.append(ancy[0])
    else:
        ancylist.append("2019")
    ancmlist.append(ancm)
    ancdlist.append(ancd)
    print(str(i)+" is over!")
l = pd.DataFrame([fylist, fqlist, ancylist, ancmlist, ancdlist, anctlist]).transpose()
l.to_csv("out_proc.csv", encoding = "utf-8")
    
    