# -*- coding: utf-8 -*-

"""
This project aims at extracting some textual factors from existing and widely-used documents, 10-Ks and Earnings call
transcripts. Main functions are contained in different folders of this project. This file performs as a coordinator
to show the process of each step. Users can choose to adjust basic settings in this file to perform parsing the text.

Global variables in this project should be set in "settings.py"
"""
from settings import *
from data_mining_10k.pars import strategy_parse
from data_mining_10k.indexcalculate import strategy_cal
from data_mining_10k.indicatorsparse import strategy_combine
from data_mining_transcript.data_feed.htmparser import trans_collect_list
from data_mining_transcript.data_processing.get_list import trans_proc_list
from data_mining_transcript.data_processing.get_fisical import trans_proc_list2
from data_mining_transcript.data_processing.download_trans import download_trans
from data_mining_transcript.data_processing.qa_div import divide_qa
from data_mining_transcript.data_processing.qa_sep_new import trans_qa_sep

if __name__ == "__main__":
    # 1. corporates' strategy described in 10-Ks.
    # 1.1 Download the Stage-One Parsed 10-Ks from Google Drive

    # 1.2 Parse the "Item 1" part
    strategy_parse()
    # 1.3 Calculate textual factors for 10-Ks
    strategy_cal()
    # 1.4 Combine them together
    strategy_combine()

    # 2. non-answers in earnings call
    # 2.1 Collect html list of earnings call transcript
    trans_collect_list()
    trans_proc_list()
    trans_proc_list2()

    # 2.2 Download transcripts and process the q-a section
    download_trans()
    trans_qa_sep()
    divide_qa()