# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:25:51 2019

@author: Luofeng
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:52:58 2019

@author: Luofeng

New version: modified on Jun. 18:
    changes _secpattern to match non-tag indicators.
"""
import pandas as pd
import os
import re

class logfile:
    def __init__(self):
        self.error_type = []
        self.error_id = []
    def push(self,errorid, errortype):
        self.error_type.append(errortype)
        self.error_id.append(errorid)
    def out(self, filename):
        l = pd.DataFrame([self.error_id, self.error_type]).transpose()
        l.to_csv(filename, encoding = "utf-8")

if __name__=='__main__':

    _mainlist = pd.read_csv("out_proc.tsv", sep = "\t", encoding = "utf-8")
    
    _secpattern = re.compile("<strong>[^<>]*?Answer[^<>]*?<br/></strong></p>.*</p>",re.DOTALL|re.M|re.I)
#    _secpattern = re.compile("<strong>[^<>]*?Answer[^<>]*?</strong></p>.*</p>",re.DOTALL|re.M|re.I)
#   run the second line first and then try the first line for complementation.    
    log = logfile()
    for i in range(len(_mainlist["AlphaIndex"])):

        filename = str(_mainlist["AlphaIndex"][i]) + ".txt"
        
        if os.path.exists(filename) == True: #file exists 
            name = "./v2/" + str(_mainlist["AlphaIndex"][i]) + "_qa_part_v2" + ".csv"
            if os.path.exists(name) == False:

                f = open(filename, "r", encoding = "utf-8")
                
                content = f.read()
                
                f.close()
                qa_section = re.findall(_secpattern, content)
                if len(qa_section) == 1:
                    with open(name, "w", encoding = "utf-8") as dd:
                        dd.write(qa_section[0])
                        print(name)
                elif len(qa_section) == 0:
                    log.push(_mainlist["AlphaIndex"][i],"No Q-A Section")
                else:
                    log.push(_mainlist["AlphaIndex"][i],"Multiple Findings")
    log.out("error_v2.log")


                
            
