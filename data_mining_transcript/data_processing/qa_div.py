# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 17:06:37 2019

@author: Luofeng
"""
'''
Step 1: Delete page seperator "<div class="p_count"></div>"
Step 1.1: Delete empty lines.
Step 2: Delete empty tag "<...></...>"
Step 2.1: Drop the title.
Step 3: Entity recognition
    <p class=\"p p[0-9]?[0-9]\"><strong>(.*?)</strong></p>
        or has id
    <p class=\"p p[0-9]?[0-9]\"><strong><span class=\"[answer|question]\"> (.*?)</span></strong></p>
    
        Content recognition
    </strong></p>\n<p class=\"p p[0-9]?[0-9]\">(.?)<p class=\"p p[0-9]?[0-9]\"><strong>
    
    #TODO
    Note that these two steps should NOT be run separately. The "correct" method is to run
    these two regex recursively.  Or use "re.split" function (more simple and fast).
    #TODO
Step 4: Determine the essense as Q or A
    if sentense has id:
        just use the id part.
        #TODO
        Note that in some file such as 4257356, the first entity is not marked while others
        are marked! so we should identify each entity!
        #TODO
    else:
        refer to raw data's list of analyst and manager and try to determine the essense.

'''
import pandas as pd
import os
import re
from settings import *

class logfile:
    def __init__(self):
        self.error_type = []
        self.error_id = []

    def push(self, errorid, errortype):
        self.error_type.append(errortype)
        self.error_id.append(errorid)

    def out(self, filename):
        l = pd.DataFrame([self.error_id, self.error_type]).transpose()
        l.to_csv(filename, encoding="utf-8")


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


def delete_n(wordlist):
    temp = []
    for i in wordlist:
        if i != "\n" and i != "" and i != " ":
            temp.append(i)
    return temp


def intersect(l1, l2):
    for i in l1:
        if i in l2:
            return False
    for j in l2:
        if j in l2:
            return False
    return True


def charactor(l1, l2):
    pat = re.compile("[a-zA-Z]+")
    t1 = []
    t2 = []
    for i in l1:
        try:
            t1.append(re.findall(pat, i)[0])
        except:
            continue
    for j in l2:
        try:
            t2.append(re.findall(pat, j)[0])
        except:
            continue
    return t1, t2


def collect_essense(ind, mode):
    with open("../" + str(ind) + ".txt", "r", encoding="utf-8") as f:

        content = f.read()

        f.close()

    strong_c = re.compile("</strong>(.*?)<strong>", re.DOTALL | re.M)
    if mode == "e":
        _item = re.compile("<p class=\"p p1\">(.*?)</p>", re.DOTALL | re.M)  # TODO: newly formed
    elif mode == "h":
        _item = re.compile("<p class=\"p p1\">(\S*\s*\S*).*?</p>", re.DOTALL | re.M)  # TODO: newly formed
    t1, t2 = re.findall(_item, delete_n(re.findall(strong_c, content))[0]), re.findall(_item, delete_n(
        re.findall(strong_c, content))[1])
    t1 = [re.sub("[a-zA-Z]*\.", "", t1[i]) for i in range(len(t1))]
    t2 = [re.sub("[a-zA-Z]*\.", "", t2[i]) for i in range(len(t2))]
    return t1, t2


def delete_em(l):
    temp = []
    for i in l:
        if i != "":
            temp.append(i)
    return temp


def determine_entity(entity, executive_list, analyst_list):
    '''
    Step 2 and 3 in "entity_rec"
    '''
    '''
    TODO:
    two-section name matching!!!
    '''
    executive_list.extend(["resident", "hief"])  # president, chief...
    analyst_list.extend(["nonymous", "nalyst", "identif"])  # unidentified, analyst, anonymous...
    for ii in executive_list:
        try:  # to avoid utf-8 character
            if re.findall(ii, entity) != []:  # find executive match
                return "A"
        except:
            continue
    for jj in analyst_list:
        try:  # same reason
            if re.findall(jj, entity) != []:  # find analyst
                return "Q"
        except:
            continue
    return "O"  # unidentified (many situation4, maybe operator)


def drop_tags(wordlist):
    '''
    Drop existing tags
    '''
    temp = []
    for i in wordlist:
        if len(re.findall("span", i)) > 0:
            temp.append(i)
            continue
        t = re.sub("<[^<>]*>", "", i)
        if t != "":
            temp.append(t)
    return temp


def entity_rec(nameid, entity_list, content_list):
    '''
    classify the content (corresponding to an entity) as Q or A
    there are several situations:
        Q and A are in class: <span class=\"answer\"> Anderson </span>  No1
        The entity is "Operator" or sth like that, or in the list of Analysts or Executives No2
        Anonymous/ unidentified/ unknown analyst No3
        Q and A are explicitly listed:  Q - Anderson (Q and A in upper case following special character or space) No4
    '''
    ans_pattern = re.compile("<span class=\"answer\">")
    qus_pattern = re.compile("<span class=\"question\">")
    #    operator_pattern = re.compile("perat")
    qus_temp = ""
    ans_temp = ""
    qlist = []
    alist = []
    executive_list = []
    analyst_list = []
    indindlist = []
    indind = 0
    for i in range(len(entity_list)):
        if len(re.findall(qus_pattern, entity_list[i])) == 1:  # explicitly in class modifier, No1
            if ans_temp != "":  # a new question
                if qus_temp != "":
                    indindlist.append(indind)
                    indind += 1
                    qlist.append(qus_temp)
                    alist.append(ans_temp)
                    qus_temp = ""
                ans_temp = ""
            qus_temp += content_list[i]
        elif len(re.findall(ans_pattern, entity_list[i])) == 1:  # explicitly in class modifier
            ans_temp += content_list[i]
        else:  # no explicit class modifier, No2
            if executive_list == []:  # the calculation is previously done, so do not repeat "collect_essense"!
                executive_list, analyst_list = collect_essense(nameid, "e")
                if intersect(executive_list, analyst_list) == True:
                    executive_list, analyst_list = collect_essense(nameid, "h")
                if executive_list == [] or analyst_list == []:  # no explicit findings of participant
                    executive_list = []
                    analyst_list = []
                #                    return False, False, False  # Omit the situation of "<strong>Q</strong>"  #TODO: add this situation in the list.
                executive_list, analyst_list = charactor(executive_list, analyst_list)
            entity_essense_2 = determine_entity(entity_list[i], executive_list, analyst_list)
            if entity_essense_2 == "Q":
                if ans_temp != "":  # a new question
                    if qus_temp != "":
                        indindlist.append(indind)
                        indind += 1
                        qlist.append(qus_temp)
                        alist.append(ans_temp)
                        qus_temp = ""
                    ans_temp = ""
                qus_temp += content_list[i]
            elif entity_essense_2 == "A":
                ans_temp += content_list[i]
            else:  # Operator or No 4
                if len(re.findall("Q", entity_list[i])) > 0:
                    if ans_temp != "":  # a new question
                        if qus_temp != "":
                            indindlist.append(indind)
                            indind += 1
                            qlist.append(qus_temp)
                            alist.append(ans_temp)
                            qus_temp = ""
                        ans_temp = ""
                    qus_temp += content_list[i]
                    continue
                elif len(re.findall("A", entity_list[i])) > 0:
                    ans_temp += content_list[i]
    if ans_temp != "" and qus_temp != "":
        qlist.append(qus_temp)
        alist.append(ans_temp)
        indindlist.append(indind)
    return indindlist, qlist, alist


def divide_qa():
    _mainlist = pd.read_csv("../out_proc.tsv", sep="\t", encoding="utf-8")  # not out.csv!

    log = logfile()
    d = 0
    entity_pattern = re.compile("<p[^<>]*?>[^a-zA-Z<>]*<strong>(.*?)</strong>[^a-zA-Z<>]*</p>",
                                re.M | re.DOTALL)  # a paragraph beginning with strong-tag
    c_pattern = re.compile("</p>(.*)", re.DOTALL | re.M)
    for i in range(len(_mainlist["AlphaIndex"])):
        flag = 0
        name = str(_mainlist["AlphaIndex"][i]) + "_qa_part_v2" + ".csv"
        #        print(name)
        if os.path.exists(name) and not os.path.exists(
                "./qapair/" + str(_mainlist["AlphaIndex"][i]) + ".tsv"):  # rewrite-free mode
            #        if os.path.exists(name): #rewrite mode
            with open(name, "r", encoding="utf-8") as f:
                content = f.read()
                content += "\n<p class=\"p p99\"><strong>"
                flag = 1
                f.close()
            content = re.sub("<div class=\"p_count\"></div>", "", content)  # Step 1
            content = re.sub("<[^/][^>]*?>\s*?</[^>]*?>", "", content)  # Delete empty tags (in pair)
            content = re.sub("<[^<>/]*/>", "", content)  # Delete self-tags
            content = re.sub("\n", "", content)  # Step 1.1: delete "enter"
            content = re.sub("\t", "", content)  # Step 1.2: delete tab (which is the seperator of our output)
            content = re.sub("<[^/<>]*>[\n\t\r]*?</[^/<>]*>", "", content)  # Step 2
            content = re.findall(c_pattern, content)[0]  # Step 2.1
            '''
            Build essense-content pairs recursively.
            # Updated in 6.19 11:31: use re.spilt instead of recursive!
            '''
            entity_list = []
            content_list = []
            try:
                content_spt = re.split(entity_pattern, content)[1:]
                content_spt = drop_tags(content_spt)
            except:  # no q-a entity exists
                flag = 0
                log.push(_mainlist["AlphaIndex"][i], "Cannot split out")
                continue
            try:
                assert len(content_spt) % 2 == 0  # one entity corresponds to one content
            except:
                flag = 0
                log.push(_mainlist["AlphaIndex"][i], "Multiple entities or contents")
                continue
            '''
            Go for entity-content matching!
            '''
            for j in range(len(content_spt)):
                if j % 2 == 0:
                    entity_list.append(content_spt[j])
                else:
                    content_list.append(content_spt[j])
            '''
            Go for entity recognition!
            '''
            try:
                indind, q_list, a_list = entity_rec(_mainlist["AlphaIndex"][i], entity_list, content_list)
                assert len(q_list) == len(a_list) and a_list != False and q_list != False
            except:
                flag = 0
                log.push(_mainlist["AlphaIndex"][i], "QA mismatch or no entity declared")
                continue
            '''
            Outing...
            '''
            if len(q_list) == 0:  # no data:
                log.push(_mainlist["AlphaIndex"][i], "No match")
                flag = 0
                continue
            indl = [str(_mainlist["AlphaIndex"][i])] * len(q_list)
            if flag == 1:
                pd.DataFrame([indl, indind, q_list, a_list]).transpose().to_csv(
                    TRANS_SAVE_DIR + "qapair/" + str(_mainlist["AlphaIndex"][i]) + ".tsv", sep="\t", encoding="utf-8")
                d += len(indind)
                print("Success in " + str(_mainlist["AlphaIndex"][i]) + " !")
    print(str(d))
    log.out(TRANS_SAVE_DIR + "qapair/error.log")
