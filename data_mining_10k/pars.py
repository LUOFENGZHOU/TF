import glob
import re
import pandas as pd
from settings import *


def strategy_parse():
    years = range(1995, 2018)
    for year in years:
        txt_list = glob.glob(STRATEGY_READ_DIR + str(year) + "*.txt")
        word_list = {"FileName": [], "MainPart": []}
        error_list = []
        enu = 0
        enu2 = 0
        pattern1 = re.compile("Item[s]*\s*1[\.|\s|:].*?Item[s]*\s*2[\.|\s|:]", re.S | re.I)
        pattern2 = re.compile("Item[s]*\s*1[\.|\s|:].*?Item[s]*\s*1B[\.|\s|:]", re.S | re.I)
        for k in txt_list:
            enu += 1
            if enu == 100:
                print("File process: " + str(100 * enu2 + enu) + ".")
                enu = 0
                enu2 += 1
            temp_file = open(k)
            readfile = temp_file.read()
            main_part = re.findall(pattern1, readfile)
            main_part_star = re.findall(pattern2, readfile)
            try:
                main_part_star = main_part_star[-1]
                main_part = main_part_star
            except IndexError:
                try:
                    main_part = main_part[-1]
                except IndexError:
                    main_part = []
            if len(main_part) < 2:
                print("Error occurs: " + k)
                error_list.append(k)
            else:
                word_list["FileName"].append(k)
                word_list["MainPart"].append(main_part)
        output = pd.DataFrame(word_list)
        output.to_csv(STRATEGY_SAVE_DIR + str(year) + "wordlist.csv", sep="\x02")
        error_file = pd.DataFrame(error_list)
        error_file.to_csv(STRATEGY_SAVE_DIR + str(year) + "errorlist.csv")


if __name__ == "__main__":
    strategy_parse()
