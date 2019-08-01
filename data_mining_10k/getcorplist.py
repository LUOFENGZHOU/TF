# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 10:45:40 2019

@author: zlf
"""
import glob
import re
import pandas as pd
import os
if __name__ == "__main__":
    years=range(2005,2018)#Define processing year
    pattern=re.compile("data_([0-9]*)_",re.S|re.I)
    for year in years:
        enu=0#I/O variable: lowest counter
        enu2=0#I/O variable: higher rank of counter
        txtlist=[]
        for root,dirs,files in os.walk(glob.glob("*")[0], onerror=None, followlinks=False): 
            try:
                if files[0][0:4]==str(year):
                    for i in range(len(files)):
                        files[i]="\\"+dirs+"\\"+files[i]
                    txtlist.extend(files)
            except:
                continue
        txtlist=glob.glob(str(year)+"*.txt")#Get all files in that year
        corplist={"FileName":[],"Date":[],"Year":[],"CIK":[]}#Create log dictionary for needed data collection
        errorlist=[]#Create error list
#        uncertainlist=[]#Create uncertain list
        errorflag=0
        for k in txtlist:
            corplist["FileName"].append(k)
            corplist["Date"].append(k[0:8])
            corplist["Year"].append(k[0:4])
            corplist["CIK"].append(re.findall(pattern,k)[0])
        output=pd.DataFrame(corplist)
        output.to_csv("corplist"+str(year)+".csv")
#        uncertainfile=pd.DataFrame(uncertainlist)
#        uncertainfile.to_csv(str(year)+"uncertainlist.csv")
        print("Year "+str(year)+" is over!")
