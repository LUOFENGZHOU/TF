# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
import glob
import time
import os

NULL_THRES = 0.2
record_filename = r"out_proc_sort.tsv"
qa_pair_dir = r"E:/0523会计数据版本/0610分步处理数据/0610原始数据/v2/qapair/"
save_dir = "./save_stat/"
filelist = glob.glob(qa_pair_dir + "*.tsv")

# define dictionaries

DISC_VERB_NO_NOUN = r"(be\b\s?([\w’,&@#$%_\-\(\)\[\]]+\s){0,1}specific|announce|announced|announcing|answer|answered|answering|breakdown|breakout|break out|breaking out|broken out|break that out|break it out|break those out|breaking that out|breaking it out|breaking those out|broken that out|broken it out|broken those out|comment|commented|commenting|disclose|disclosed|disclosing|discuss|discussed|discussing|divulge|divulged|divulging|elaborate|elaborated|elaborating|estimate|estimated|estimating|forecast|forecasted|forecasting|guide|guided|guiding|predict|predicted|predicting|report|reported|reporting|reveal|revealed|revealing|speculate|speculated|speculating|say about|say anything|say more|say any more|say much more|say too much|said about|said anything|said more|said any more|said much more|said too much|talk about|talked about)"

WORD_CHAR = r"[a-zA-z]"
    
DISC_VERB_NOUN=r"(address|addressed|addressing|explain|explanation|get into|get|getting|give|given|giving|go into|going into|got into|gotten into|mention|mentioned|mentioning|on record|present|presented|presenting|provide|provided|providing|quantified|quantify|quantifying|release|released|releasing|speak|speaking|specified|specify|specifying|spoke|supplied|supply|supplying|talk|talked|talking|tell|told|update|updated|updating)"

DEFERRAL=r"(difficult|impossible|infeasible|hard|decline|refuse|refrain|unable|never|all I can|all we can|all I will|all we will|about all)"

DISC_NOUN= r"(too much|much more|account|accounts|acquisition|acquisitions|activity|activities|amount|amounts|analysis|answer|answers|anything|asset|assets|backlog|backlogs|balance|balances|breakdown|budget|budgets|capital|cash|change|changes|comparison|comparisons|component|components|condition|conditions|content|contract|contracts|cost|costs|coverage|credit|data|deal|deals|debt|demand|demands|detail|details|development|developments|direction|directions|distribution|dollar|dollars|earnings|equity|equities|estimate|estimates|expansion|expansions|expectation|expectations|expense|expenses|exposure|fact|facts|factor|factors|fee|fees|figure|figures|financing|forecast|forecasts|funding|growth|guidance|income|incomes|information|interest|inventory|inventories|investment|investments|liquidity|loan|loans|loss|losses|magnitude|magnitudes|management|margin|margins|marketing|metric|metrics|model|models|money|name|names|needs|news|number|numbers|operations|option|options|order|orders|partner|partners|percent|percentage|percentages|performance|plan|plans|point|points|policy|policies|portfolio|portfolios|price|prices|pricing|profit|profits|profitability|progress|project|projects|projection|projections|quality|quantification|quantity|quantities|range|ranges|rate|rates|ratio|ratios|reason|reasons|reserve|reserves|result|results|revenue|revenues|risk|risks|sale|sales|savings|share|shares|size|sizes|specific|specifics|specifically|spending|statement|statements|statistic|statistics|strategy|supplier|suppliers|supply|supplies|target|targets|tax|taxes|term|terms|transaction|transactions|trend|trends|value|values|volume|volumes)"
   

# define regex

# Refuse non-answers
#TYPE=REFUSE
# {Disclosure Verb}..."no"...{Disclosure Noun}
refuse1 = re.compile(r"(?i)\b" + DISC_VERB_NOUN + r"\b\s?(" + WORD_CHAR + r"+\s){0,2}no\b\s?(" + WORD_CHAR + r"+\s){0,2}" + DISC_NOUN + r"\b")
# {Disclosure Verb}..."no"
refuse2 = re.compile(r"(?i)\b" + DISC_VERB_NO_NOUN + r"\b\s?(" + WORD_CHAR + r"+\s){0,2}no\b")
# {Negation}...{Disclosure Verb}
refuse3 = re.compile(r"(?i)(n(’|‘)t|\bnot|cannot|without)\b\s?(" + WORD_CHAR + r"+\s){0,8}" + DISC_VERB_NO_NOUN + r"\b")
# {Negation}...{Disclosure Verb}...{Disclosure Noun}
refuse4 = re.compile(r"(?i)(n(’|‘)t|\bnot|cannot|without)\b\s?(" + WORD_CHAR + r"+\s){0,8}" + DISC_VERB_NOUN + r"\b\s?(" + WORD_CHAR + r"+\s){0,8}" + DISC_NOUN + r"\b")
# {Deferral}...{Disclosure Verb}
refuse5 = re.compile(r"(?i)\b" + DEFERRAL + r"\b\s?(" + WORD_CHAR + r"+\s){0,8}" + DISC_VERB_NO_NOUN + r"\b")
refuse6 = re.compile(r"(?i)\b" + DEFERRAL + r"\b\s?(" + WORD_CHAR + r"+\s){0,8}" + DISC_VERB_NOUN + r"\b\s?(" + WORD_CHAR + r"+\s){0,8}" + DISC_NOUN + r"\b")

# Unable non-answers
#TYPE=UNABLE
unable1 = re.compile(r"(?i)\b(I|we)\b\s?(" + WORD_CHAR + r"+\s){0,2}((do(n(’|‘)t| not))|(can(’t|not| not)))\b\s?(" + WORD_CHAR + r"+\s){0,2}(know|recall|remember)\b")
unable2 = re.compile(r"(?i)\b(I|we) have no idea\b")
unable3 = re.compile(r"(?i)\b(I|we) do(n(’|‘)t| not)\b\s?(" + WORD_CHAR + r"+\s){0,2}(have (the|it|that|this|those))\b")
unable4 = re.compile(r"(?i)(n(’|‘)t|\bnot|cannot|without)\b\s?(" + WORD_CHAR + r"+\s){0,8}(share|sharing|shared)\b\s?(" + WORD_CHAR + r"+\s){0,8}(with)\b")

# After-call non-answers
#TYPE=AFTERCALL
aftercall = re.compile(r"(?i)\b(off-line|offline|after the call|after call|another (time|day))\b")
begin_time = time.time()
counter = 0
for i in filelist:
    name = i[44:-4]
    if os.path.exists(save_dir + name + "_proc.tsv"):
        continue
    print(name + " " + str(counter))
    try:
        data = pd.read_csv(open(i, encoding = "utf-8"), sep = "\t", encoding = "utf-8")
    except:
        continue
    qlist = data["2"]
    alist = data["3"]
    data["4"] = data["1"]
    for j in range(len(alist)):
        counter += 1
        r1 = len(re.findall(refuse1, alist[j]))
        r2 = len(re.findall(refuse2, alist[j]))
        r3 = len(re.findall(refuse3, alist[j]))
        r4 = len(re.findall(refuse4, alist[j]))
        r5 = len(re.findall(refuse5, alist[j]))
        r6 = len(re.findall(refuse6, alist[j]))
        r = r1 + r2 + r3 + r4 + r5 + r6
        u1 = len(re.findall(unable1, alist[j]))
        u2 = len(re.findall(unable2, alist[j]))
        u3 = len(re.findall(unable3, alist[j]))
        u4 = len(re.findall(unable4, alist[j]))
        u = u1 + u2 + u3 + u4
        a = len(re.findall(aftercall, alist[j]))
        data["2"][j] = r
        data["3"][j] = u
        data["4"][j] = a
        midtime = time.time()
        print("Speed : " + str(counter / (midtime - begin_time )), end = "\r")
    data.to_csv(save_dir + name + "_proc.tsv", encoding = "utf-8", sep = "\t")
    print("Speed : " + str(counter / (midtime - begin_time )))
print("Over: " + str(counter))
