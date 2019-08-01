import glob
import re
import pandas as pd
years=range(1995,2018)
for year in years:
    txtlist=glob.glob(str(year)+"*.txt")
    wordlist={"FileName":[],"MainPart":[]}
    errorlist=[]
    enu=0
    enu2=0
    pattern1=re.compile("Item[s]*\s*1[\.|\s|:].*?Item[s]*\s*2[\.|\s|:]",re.S|re.I)
    pattern2=re.compile("Item[s]*\s*1[\.|\s|:].*?Item[s]*\s*1B[\.|\s|:]",re.S|re.I)
    for k in txtlist:
        enu+=1
        if enu==100:
            print("File process: "+str(100*enu2+enu)+".")
            enu=0
            enu2+=1
        tempfile=open(k)
        readfile=tempfile.read()
        mainpart=re.findall(pattern1,readfile)
        mainpartstar=re.findall(pattern2,readfile)
        try:
            mainpartstar=mainpartstar[-1]
            mainpart=mainpartstar
        except:
            try:
                mainpart=mainpart[-1]
            except:
                mainpart=[]
        if len(mainpart)<2:
            print("Error occurs: "+k)
            errorlist.append(k)
        else:
            wordlist["FileName"].append(k)  
            wordlist["MainPart"].append(mainpart)
    output=pd.DataFrame(wordlist)
    output.to_csv(str(year)+"wordlist.csv",sep="\x02")
    errorfile=pd.DataFrame(errorlist)
    errorfile.to_csv(str(year)+"errorlist.csv")
        
        