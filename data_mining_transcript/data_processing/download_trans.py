# -*- coding: utf-8 -*-
"""
Created on Thu May 23 21:49:08 2019

@author: Luofeng
"""

import pandas as pd

import requests

from user_agent import generate_user_agent

from multiprocessing import Process

import time

from bs4 import BeautifulSoup

import os

import numpy as np
from settings import *


def download_trans():
    aa = time.time()
    mainlist = pd.read_csv(TRANS_READ_DIR + "trans_list_proc.csv", encoding="utf-8")

    for i in range(len(mainlist["AlphaIndex"])):

        if not os.path.exists(str(mainlist["AlphaIndex"][i]) + ".txt"):
            print(str(mainlist["AlphaIndex"][i]))
            h = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
                "Cookie": "machine_cookie=3304320221604; __gads=ID=f8f9adc8384ae385:T=1556960855:S=ALNI_MZpYUGI69X-eFqyPKgH41Rdjdu7sQ; __utma=150447540.948520752.1556960856.1557654227.1557657917.10; __utmz=150447540.1556960866.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pxvid=1e770625-6e4c-11e9-a19d-0242ac12000d; __utmb=150447540.16.10.1557657917; __utmt=1; __utmc=150447540; _px=IuAl5gK94RT2J1ZY+jFtFi16PxLD+bSQC8HSg2PorYwukYGgA8Mly+pPe9LucpydE3FSeR6Ie4/ZhqVvXB6k3A==:1000:V7G2VJHIzAyTpQutyxTrs3gRNG1LlvJgZiwrOwvvPXEDrclwQMXAfX56a9TbTmpqrD0LGgubxgQCTYLQdf6ezfwjNES0L4eFFwE/BT0PHoa7XcT3fNrLp9g/EQWiF6aCYH+qlcemhiPsMCO4Lw8OFxbon25y8efP6Nsi4ThFlTAXP5j/KkBuMa//zVqEVzMFr/8Q/WE39zQLwfLRLpGJO8rRLVSQgQ4QnekOyXarKiY0Kso+06EXzOc0Y1UmyygRzRncS07dRifplpwFQ+E3Cw==; _px2=eyJ1IjoiNzA5YTQ1NzAtNzRiMi0xMWU5LWE3MGUtMmQ5N2YxYzI5MjM3IiwidiI6IjFlNzcwNjI1LTZlNGMtMTFlOS1hMTlkLTAyNDJhYzEyMDAwZCIsInQiOjE1NTc2NjUwNjA2MzAsImgiOiI2NmMxZDc3MTA1NTA4OGI4NWY4OWZhNzBlYTEyMGM4MDIwZTg2MzVlMWYxZWZkZDRjOGNjNzMyZGZlOTg4NDIwIn0=; h_px=1; _pxff_tm=1; _pxde=6be8c21762dc318c152bf482fbd822e995b46ecbe732eeb33117f57b61503b18:eyJ0aW1lc3RhbXAiOjE1NTc2NjQ1NjA2MzB9; _igt=650d39d6-b352-4137-aee3-1f32207f5c67; _ig=fd713b51-7da8-4770-b1bf-189a07b360fb"}
            try:
                page_art = requests.get(mainlist["Link"][i], headers=h, timeout=60)

                if page_art.status_code == 403:
                    h = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/' +

                                       str(np.random.randint(1, high=9)) +

                                       str(np.random.randint(1, high=9)) +

                                       str(np.random.randint(1, high=9)) +

                                       '.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                page_art = requests.get(mainlist["Link"][i], headers=h, timeout=60)

                if page_art.status_code == 200:

                    page_bs_art = BeautifulSoup(page_art.text, "lxml")
                    #                page_art.close()

                    text = page_bs_art.findAll('article')[0]

                    with open(TRANS_SAVE_DIR + str(mainlist["AlphaIndex"][i]) + '.txt', "w", encoding="utf-8") as f:

                        f.write(str(text))

                    print("Sucess of " + str(i) + "!")

                    print(str((time.time() - aa) * (len(mainlist) - i + 1) / 3600))

                #                time.sleep(1)
                else:
                    print(str(page_art.status_code) + " " + str(mainlist["Num"][i]))
                    h = generate_user_agent()  # next(headers)
            #                page_art.close()
            #                time.sleep(1)

            except:
                h = generate_user_agent()  # next(headers)

                print("Waiting ...")

    #            time.sleep(1)
    #            page_art.close()
