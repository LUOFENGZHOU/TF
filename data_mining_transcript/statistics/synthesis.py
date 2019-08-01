# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
#import re
#import glob
#import time
import os

able_list = pd.read_csv("read_all.tsv", sep = "\t", encoding = "utf-8")
append_num = able_list["AlphaIndex"]
save_dir = "./save_stat/"

# begin main loop
list1 = np.array([])
list2 = np.array([])
list3 = np.array([])
for i in range(len(append_num)):
#for i in [0]:
    print(str(i))
    num_temp = append_num[i]
    if os.path.exists(save_dir + str(num_temp) + "_proc.tsv"):
        read_temp = pd.read_csv(save_dir + str(num_temp) + "_proc.tsv", encoding = "utf-8", sep = "\t")
        list1 = np.append(list1, 1 if np.sum(read_temp["2"]) > 0 else 0)
        list2 = np.append(list2, 1 if np.sum(read_temp["3"]) > 0 else 0)
        list3 = np.append(list3, 1 if np.sum(read_temp["4"]) > 0 else 0)
    else: # no q-a pair file: 1,2,3 = 0
        list1 = np.append(list1, 0)
        list2 = np.append(list2, 0)
        list3 = np.append(list3, 0)
        print("zzz")
able_list["text1"] = list1
able_list["text2"] = list2
able_list["text3"] = list3
able_list.to_csv("real_all_modified.tsv", sep = "\t", encoding = "utf-8")         