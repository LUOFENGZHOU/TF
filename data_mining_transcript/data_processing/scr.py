# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:52:58 2019

@author: Luofeng
"""
import pandas as pd

import numpy as np

import os
import time
import re
from multiprocessing import Process
def delete_n(wordlist):
    temp = []
    for i in wordlist:
        if i != "\n" and i != "" and i != " ":
            temp.append(i)
    return temp

def delete_space(wordlist):
    temp = []
    for string in wordlist:
        try:
            if string[-1] == " ":
                string = string[:-1]
            if string[0] == " ":
                string = string[1:]
            temp.append(string)
        except:
            continue
    return temp
if __name__=='__main__':

    _mainlist = pd.read_csv("out.csv", encoding = "utf-8")
    
    _secpattern = re.compile("<strong>.*?Answer.*?</strong></p>(.*)</p>",re.DOTALL|re.M)
    
    _strong_c = re.compile("</strong><(.*?)><strong>",re.DOTALL|re.M)
    strong_c = re.compile("</strong>(.*?)<strong>",re.DOTALL|re.M)


    _strong_e = re.compile("><strong>(.*?)</strong><",re.DOTALL|re.M)
        
    _item = re.compile("<p class=\"p p1\">([a-zA-Z]*\.? *[a-zA-Z]*\.? *[a-zA-Z]*\.? *[a-zA-Z]* *[a-zA-Z]*? *[a-zA-Z]*).*?</p>",re.DOTALL|re.M)
    _figure = re.compile(">?([a-zA-Z]*\.? *[a-zA-Z]*\.? *[a-zA-Z]*\.? *[a-zA-Z]* *[a-zA-Z]*? *[a-zA-Z]*).*?<?")

    _cc = re.compile(">(.*?)<", re.DOTALL|re.M)
    _class = re.compile("span class=\"(.*?)\">", re.DOTALL|re.M)
    for i in range(len(_mainlist["AlphaIndex"])):
        
        t0 = time.time()

        print("Start "+str(i))

        _filename = str(_mainlist["AlphaIndex"][i]) + ".txt"
        
        if os.path.exists(_filename) == True: #file exists 
        
            f = open(_filename, "r", encoding = "utf-8")
            
            content = f.read()
            
            f.close()
            try:
                name = str(_mainlist["AlphaIndex"][i]) + "_proc" + ".csv"
                if os.path.exists(name) == False:
                    _execute = delete_n(re.findall(strong_c, content))[0]
                    
                    _analyst = delete_n(re.findall(strong_c, content))[1]
        
                    _execute_list = delete_space(re.findall(_item, _execute))
                    
                    _analyst_list = delete_space(re.findall(_item, _analyst))
                    
                    _qa_section = re.findall(_secpattern, content)[0]
                    
                    main_entity = re.findall(_strong_e, _qa_section)[:-1]
                    
                    main_content = re.findall(_strong_c, _qa_section)
                    
        #            assert len(main_entity) == len(main_content)

                    essense_list = []
                    entity_list = []
                    content_list = []
                    for j in range(len(main_entity)):
                        
                        essense = re.findall(_class, main_entity[j])
                        
                        if essense != []:
                            essense_list.append(essense[0])
                            
                            entity_list.append(re.findall(_cc, main_entity[j])[0])
                            
                            content_list.append(delete_n(re.findall(_cc, main_content[j]))[0])
                        else:
                            try:
                                if len(re.findall(_cc, main_entity[j])) > 0:
                                    
                                    if delete_space(re.findall(_figure, re.findall(_cc, main_entity[j])[0]))[0] in _execute_list:
                                        essense = ["answer"]
                                    elif delete_space(re.findall(_figure, re.findall(_cc, main_entity[j])[0]))[0] in _analyst_list:
                                        essense = ["question"]
                                else:
                                    if delete_space(re.findall(_figure, main_entity[j]))[0] in _execute_list:
                                        essense = ["answer"]
                                    elif delete_space(re.findall(_figure, main_entity[j]))[0] in _analyst_list:
                                        essense = ["question"] 
                                if essense != []:
                                    essense_list.append(essense[0])
                                    if re.findall(_cc, main_entity[j]) == []:
                                        entity_list.append(main_entity[j])
                                    else:
                                        entity_list.append(re.findall(_cc, main_entity[j])[0])
                                    if len(re.findall(_cc, main_content[j])) < 2:
                                        content_list.append(main_content[j])
                                    else:
                                        content_list.append(delete_n(re.findall(_cc, main_content[j]))[0])
                                else:
                                    if len(re.findall("Q\s*[-|—]", main_entity[j])) > 0:
                                        essense = ["question"]
                                    elif  len(re.findall("A\s*[-|—]", main_entity[j])) > 0:
                                        essense = ["answer"]
                                    if essense != []:
                                        essense_list.append(essense[0])
                                        if re.findall(_cc, main_entity[j]) == []:
                                            entity_list.append(main_entity[j])
                                        else:
                                            entity_list.append(re.findall(_cc, main_entity[j])[0])
                                        if len(re.findall(_cc, main_content[j])) < 2:
                                            content_list.append(main_content[j])
                                        else:
                                            content_list.append(delete_n(re.findall(_cc, main_content[j]))[0])
                            except:
                                continue
                    if len(content_list) > 0:
                        l = pd.DataFrame([essense_list, entity_list, content_list]).transpose()
                        l.to_csv(name, encoding = "utf-8")
                        print(name)
                        print(str((time.time() - t0) ))

                    else:
                        print("Fail! "+name)
                        print(str((time.time() - t0) ))
                else:
                    print("End "+ str(i))
            except:
                print("Fail! "+name)
                print(str((time.time() - t0) ))

                continue