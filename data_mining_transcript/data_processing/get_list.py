# -*- coding: utf-8 -*-
"""
Created on Mon May  6 02:27:09 2019

@author: zlf

"""

import glob
import pandas as pd
import time
import re
from natsort import natsorted
from settings import *


def trans_proc_list():
    url_site = 'https://seekingalpha.com/'
    filelist = natsorted(glob.glob(TRANS_READ_DIR + "/html/*.htm"))
    ticklist = []
    linklist = []
    indlist = []
    sourcelist = []
    timelist = []
    fullnamelist = []
    shortnamelist = []

    lll = 0

    for file in filelist:
        try:
            with open(file, "r", encoding="utf-8") as f:
                aa = f.read()
            bb = re.compile("<a class=\"dashboard-article-link\"(.*?)</a>", re.S)
            cc = re.compile("<div.*?</div>", re.S)
            cd = re.compile("\n\s*(.*?)\n\n")
            dd = re.compile("href=\"(.*?)\"", re.S)
            ee = re.compile(">(.*)", re.S)
            cont = cc.findall(aa)
            name = bb.findall(aa)
            gg = re.compile("/(.*?)-")
            ti = re.compile("title=\"(.*?)\"", re.S)
            kk = re.compile(r'<a.*?>(.*?)</a?', re.DOTALL | re.UNICODE)
            for i in range(len(cont)):
                title = kk.findall(cont[i])
                tick = title[0]
                source = title[1]
                time = cd.findall(cont[i])
                ind = gg.findall(name[i])[0]
                link = url_site + dd.findall(name[i])[0][1:]
                fullname = ee.findall(name[i])[0]
                shortname = ti.findall(cont[i])
                ticklist.append(tick)
                sourcelist.append(source)
                timelist.append(time[0])
                linklist.append(link)
                fullnamelist.append(fullname)
                try:
                    shortnamelist.append(shortname[0])
                except:
                    shortnamelist.append("")
                indlist.append(ind[8:])
            print(str(lll) + " is over!")
            lll += 1
        except:
            continue
    l = pd.DataFrame()
    l["FileName"] = fullnamelist
    l["AlphaIndex"] = indlist
    l["Link"] = linklist
    l["CompanyName"] = shortnamelist
    l["Source"] = sourcelist
    l["Ticker"] = ticklist
    l["DateTime"] = timelist
    l.index.name = "Num"
    l.to_csv(TRANS_READ_DIR + "trans_list.tsv", encoding="utf-8", sep="\t")
