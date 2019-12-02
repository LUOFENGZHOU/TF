# -*- coding: utf-8 -*-
"""
Created on Sat May  4 18:10:39 2019

@author: zlf
"""

import requests
from bs4 import BeautifulSoup
import time
from settings import *
from user_agent import generate_user_agent


def trans_collect_list():
    time0 = time.time()
    url_art = 'https://seekingalpha.com/earnings/earnings-call-transcripts/'  # + number
    # headers = header_change()
    i = 0
    while i < 6000:
        print(i)
        try:
            h = generate_user_agent()  # next(headers)
            page = requests.get(url_art + str(i), headers={'User-Agent': h})
            page_bs = BeautifulSoup(page.text, "lxml")
            links = page_bs.findAll('ul', id='analysis-list-container')[0]
            with open(TRANS_READ_DIR + "html/htm_" + str(i) + ".htm", "w", encoding="utf-8") as f:
                f.write(str(links))
            print("Success " + str(i) + " !")
            i += 1
            time.sleep(1)
            avgtime = (time0 - time.time()) / (i + 1) * 6000 / 3600
            print(str(avgtime) + " hours left.", end="\r")
        except:
            print("Waiting ... ")
            time.sleep(1)
