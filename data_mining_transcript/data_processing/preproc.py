# -*- coding: utf-8 -*-
"""
Created on Mon May  6 02:27:09 2019

@author: zlf
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May  4 18:20:28 2019

@author: zlf
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May  4 18:10:39 2019

@author: zlf
"""

import numpy as np

import glob

#import requests

import pandas as pd

from bs4 import BeautifulSoup

import time

import re

from user_agent import generate_user_agent

from natsort import natsorted



#def header_change():
#
#    header1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/' +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             '.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
#
#    header2 = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/' +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             '.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}
#
#    header3 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/' +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             '.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
#
#    header4 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/' +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             '.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
#
#    header5 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/' +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             str(np.random.randint(1, high=9)) +
#
#                             '.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
#
#    headers = [header1, header2, header3, header4, header5]
#
#    while True:
#
#        for h in headers:
#
#            yield h


time0 = time.time()

url_art = 'https://seekingalpha.com/earnings/earnings-call-transcripts/'  # + number

url_site = 'https://seekingalpha.com/'



folder = '../'



# headers = header_change()

#i = 1440
#
#i0 = i
filelist = natsorted(glob.glob("*.htm"))
ticklist = []
linklist = []
indlist = []
sourcelist = []
timelist = []
fullnamelist = []
shortnamelist = []

lll = 0

for file in filelist:
    

    
    try:
        with open(file, "r", encoding = "utf-8") as f:
        
            aa = f.read()
    
        bb = re.compile("<a class=\"dashboard-article-link\"(.*?)</a>", re.S)
        
        cc = re.compile("<div.*?</div>", re.S)
        
        cd = re.compile("\n\s*(.*?)\n\n")
        
        dd = re.compile("href=\"(.*?)\"", re.S)
        
        ee = re.compile(">(.*)", re.S)
        
        cont = cc.findall(aa)
        
        name = bb.findall(aa)
        
        gg = re.compile("/(.*?)-")
        
        ti = re.compile("title=\"(.*?)\"", re.S)
        
        kk = re.compile(r'<a.*?>(.*?)</a?', re.DOTALL|re.UNICODE)
    
#        assert len(cont) == 30
#        
#        assert len(name) == 30
        
        for i in range(len(cont)):
            
            title = kk.findall(cont[i])
            
            tick = title[0]
            
            source = title[1]
            
            time = cd.findall(cont[i])
            
            ind = gg.findall(name[i])[0]
            
            link = url_site + dd.findall(name[i])[0][1:]
            
            fullname = ee.findall(name[i])[0]
            
            shortname = ti.findall(cont[i])
            
            ticklist.append(tick)
            
            sourcelist.append(source)
            
            timelist.append(time[0])
            
            linklist.append(link)
            
            fullnamelist.append(fullname)
            
            try:
                
                shortnamelist.append(shortname[0])
                
            except:
                
                shortnamelist.append("")
            
            indlist.append(ind[8:])
            
        print(str(lll) +" is over!")
        
        lll += 1
            
        
        


#while i < 6000:
#
#    print(i)
#
#    try:
#
#        h = generate_user_agent() #next(headers)
#
#        page = requests.get(url_art + str(i), headers={'User-Agent': h})
#
#        page_bs = BeautifulSoup(page.text, "lxml")
#
#        links = page_bs.findAll('ul', id='analysis-list-container')[0]
#        
#        with open("htm_" + str(i) + ".htm", "w", encoding = "utf-8") as f:
#            
#            f.write(str(links))
#        
#        print("Sucess " + str(i) + " !")
#        
#        i += 1
#        
#        time.sleep(1)
#        
#        avgtime = -(time0 - time.time()) / (i - i0) * (6000 - i) / 3600
#        
#        print(str(avgtime) + " hours left.")
##        print(page_bs)
#
#
#        links = links.findAll('h3')
#
#        arts = []
#
#        for a in links:
#
#            arts.append(a.findAll('a')[0]['href'])
#
#        for x in range(0, len(arts)):
#
#            h = generate_user_agent() #next(headers)
#
#            page_art = requests.get(url_site + arts[x], headers={'User-Agent': h})
#
#            try:
#
#                if page_art.status_code == 200:
#
#                    page_bs_art = BeautifulSoup(page_art.text, "lxml")
#
#                    text = page_bs_art.findAll('article')[0]
#
#
#
#                    with open(folder + "data/parsing/" + str(i) + '_num_' + str(x) + '.txt', "w") as f:
#
#                        f.write(str(text))
#
#
#
#                    print(str(i) + '_num_' + str(x) + '.txt')
#
#
#
#                else:
#
#                    h = generate_user_agent() #next(headers)
#
#                    time.sleep(15)
#
#                    page_art = requests.get(url_site + arts[x], headers={'User-Agent': h})
#
#                    page_bs_art = BeautifulSoup(page_art.text, "lxml")
#
#                    text = page_bs_art.findAll('article')[0]
#
#
#
#                    with open(folder + "data/parsing/" + str(i) + '_num_' + str(x) + '.txt', "w") as f:
#
#                        f.write(str(text))
#
#
#
#                    print(str(i) + '_num_' + str(x) + '.txt')
#
#
#
#            except:
#
#                h = generate_user_agent() #next(headers)
#
#                time.sleep(50)
#
#                with open(folder + "data/errors.txt", "a") as f:
#
#                    f.write(url_site + arts[x])



    except:
        
        continue
l = pd.DataFrame([fullnamelist, indlist, linklist, shortnamelist, sourcelist, ticklist, timelist]).transpose()

l.to_csv("out.csv", encoding = "utf-8")
#        with open(folder + "data/big_errors.txt", "a") as f:
#
#            f.write(url_site + str(i))