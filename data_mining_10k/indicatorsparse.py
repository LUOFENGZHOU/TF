import glob
import pandas as pd
import re
filelist=glob.glob("*.csv")
log={"Year":[],"CIK":[],"Date":[],"DS":[],"DP":[],"DC":[],"DH":[],"CS":[],"CC":[],"CO":[],"CE":[]}
keys=log.keys()
pattern=re.compile("([a-z|']*)",re.S|re.I)
log={"Year":[],"CIK":[],"Date":[],"DS":[],"DP":[],"DC":[],"DH":[],"CS":[],"CC":[],"CO":[],"CE":[],"Length":[]}
for l in filelist:
    readfile=pd.read_csv(l)
    for k in keys:
        log[k].extend(readfile[k])
    for b in range(len(readfile["CIK"])):
        listtemp=re.findall(pattern,readfile["MainPart"][b])
        countt=0
        for a in listtemp:
            if len(a)>0:
                countt+=1
        log["Length"].append(countt)
    print(l+" is completed!")
output=pd.DataFrame(log)
output.to_csv("out.csv",sep=',')