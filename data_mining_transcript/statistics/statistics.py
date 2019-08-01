# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pymysql
import datetime
NULL_THRES = 0.2
record_filename = r"out_proc_sort.tsv"
qa_pair_dir = r"E:/0523会计数据版本/0610分步处理数据/0610原始数据/v2/qapair/"

def get_next_corp(df, t_next):
    corp_now = df["Ticker"][t_next]
    i = t_next
    while df["Ticker"][i+1] == corp_now:
        i += 1
    return corp_now, df[t_next:i+1], i+1

class LogFile:
    def __init__(self):
        self.logs_corp = []
    def push(self, corp):
        self.logs_corp.append(corp)
        print("Error : " + corp)
    def out(self):
        return pd.DataFrame(self.logs_corp).T.to_csv("errorv2.log")
# read file
#def tfill(df):
#    fyear = list(df["Fyear"])
#    fquart = list(df["Fquarter"])
#    t_len = len(fyear)
#    null_list = []
#    for _ in range(t_len):
#        if fyear[_] == "ERROR" or fquart[_] == "ERROR":
#            null_list.append(0)
#        else:
#            null_list.append(1)
#        nlen = len(null_list) / t_len
#    if nlen > t_len * NULL_THRES:
#        print("Too many null items")
#        return False, df
#    rate_list = []
#    for i in range(len(fquart)):
#        if i == "ERROR":
#            continue
#        rate_list.append([(j - i + int(fquart[i][1]) -1) % 4 + 1 for j in range(len(fquart))])
#    for_times = len(rate_list)
#    rating = 

def get_trade_time(tic, db_ip="localhost" , db_username="root" , db_password="zaqxswcd", db_name="new_schema1"):
    '''
    Get the record in database.
    '''
    db = pymysql.connect(db_ip, db_username, db_password, db_name )
    cursor = db.cursor()
    cursor.execute("USE new_schema")
    cursor.execute("SELECT gvkey, fyear, tic, datadate FROM ggg WHERE tic = \"" + tic + "\"")
    ind_list = cursor.fetchall()
    db.close()
    return pd.DataFrame(np.array([np.array(_) for _ in ind_list]))








def find_near(li, val):
    '''
    return index of li.
    '''
    if (li[0] - val).days > 0 and (li[0] - val).days < 360:
        return 0
    for i in range(1, len(li)):
        if 0 < (li[i] - val).days and  (li[i] - val).days < 360 and (val-li[i-1]).days > 0:
            return i
        elif (val-li[i-1]).days < 0:
            return i - 1
    return False

logs = LogFile()
df = pd.read_csv(record_filename, encoding = "utf-8", sep = "\t")

def is_distinct(ls):
    past = ls[0]
    for i in ls:
        if i != past:
            return False
    return True

# segmentation
t_next = 0
init = True
fyear_append = []
gvkey_append = []
Num_append = []
for i in range(len(df)-1):
#for i in [0]:
    try:
        t_ticker, t_sep_list, t_next = get_next_corp(df, t_next) # seperate by company
    except:
        continue
    gvkeylist = get_trade_time(t_ticker)

    if len(gvkeylist) == 0:
        print("ticker not found: " + t_ticker)
        logs.push(t_ticker)
        continue
    if not is_distinct(gvkeylist[0]):
        print("changing ticker: " + t_ticker)
        logs.push(t_ticker)
        continue
    if not is_distinct([_.month for _ in gvkeylist[3]]):
        print("changing month: " + t_ticker)
        logs.push(t_ticker)
        continue



    if gvkeylist[1][0] == gvkeylist[3][0].year:
        rel = 0
    else:
        rel = -1
    month_t = gvkeylist[3][0].month
    truemonth_t = (month_t + 3) % 12
    if month_t > truemonth_t:
        year_t = 1
    else:
        year_t = 0
    yearlist_t = [_ for _ in range(gvkeylist[3].min().year + year_t, gvkeylist[3].max().year + year_t + 1)]
    if truemonth_t == 12:
        datelist_t = [datetime.date(_,12,31) for _ in yearlist_t]
    else:
        datelist_t = [datetime.date(_,truemonth_t+1,1) - datetime.timedelta(1) for _ in yearlist_t]
    # change time format
    tplist = []
    for d in t_sep_list["Adatetime"]:
        tplist.append(datetime.date(int(str(d)[0:4]), int(str(d)[4:6]), int(str(d)[6:8])))

    for cs in range(len(tplist)):
        ddd = find_near(datelist_t, tplist[cs])
        if ddd != False:
            gvkey_append.append(gvkeylist[0][0])
            fyear_append.append(datelist_t[ddd].year + rel - year_t)
            Num_append.append(np.array(t_sep_list["Num"])[cs])
    print("Over!")
#    t_sep_list = tfill(t_sep_list)
#    ylist, fnamelist, 
#pd.DataFrame([fyear_append, gvkey_append, Num_append]).T.to_csv("outputmerge.csv", encoding = "utf-8")
#logs.out()