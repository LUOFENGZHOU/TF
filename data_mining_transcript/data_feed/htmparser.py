# -*- coding: utf-8 -*-
"""
Created on Sat May  4 18:10:39 2019

@author: zlf
"""

import numpy as np



import requests

from bs4 import BeautifulSoup

import time



from user_agent import generate_user_agent



def header_change():

    header1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/' +

                             str(np.random.randint(1, high=9)) +

                             str(np.random.randint(1, high=9)) +

                             str(np.random.randint(1, high=9)) +

                             '.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

    header2 = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/' +

                             str(np.random.randint(1, high=9)) +

                             str(np.random.randint(1, high=9)) +

                             str(np.random.randint(1, high=9)) +

                             '.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}

    header3 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/' +

                             str(np.random.randint(1, high=9)) +

                             str(np.random.randint(1, high=9)) +

                             str(np.random.randint(1, high=9)) +

                             '.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

    header4 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/' +

                             str(np.random.randint(1, high=9)) +

                             str(np.random.randint(1, high=9)) +

                             str(np.random.randint(1, high=9)) +

                             '.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}

    header5 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/' +

                             str(np.random.randint(1, high=9)) +

                             str(np.random.randint(1, high=9)) +

                             str(np.random.randint(1, high=9)) +

                             '.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    headers = [header1, header2, header3, header4, header5]

    while True:

        for h in headers:

            yield h


time0 = time.time()

url_art = 'https://seekingalpha.com/earnings/earnings-call-transcripts/'  # + number

url_site = 'https://seekingalpha.com/'



folder = '../'


# headers = header_change()

i = 0

while i < 6000:

    print(i)

    try:

        h = generate_user_agent() #next(headers)

        page = requests.get(url_art + str(i), headers={'User-Agent': h})

        page_bs = BeautifulSoup(page.text, "lxml")

        links = page_bs.findAll('ul', id='analysis-list-container')[0]
        
        with open("htm_" + str(i) + ".htm", "w", encoding = "utf-8") as f:
            
            f.write(str(links))
        
        print("Sucess " + str(i) + " !")
        
        i += 1
        
        time.sleep(1)
        
        avgtime = (time0 - time.time()) / (i + 1) * 6000 / 3600
        
        print(str(avgtime) + " hours left.", end = "\r")


    except:
        
        print("Waiting ... ")
        
        time.sleep(1)
