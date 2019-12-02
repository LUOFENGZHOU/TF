# -*- coding: utf-8 -*-
"""
This file contains all the global variables needed in the parsing process.
"""
import os

# Data feed of 10-Ks
STRATEGY_READ_DIR = "./data_feed_10k/"


# Saving directory of strategy from 10-Ks
STRATEGY_SAVE_DIR = "./data_10k/"

# Data feed of earnings call transcripts
TRANS_READ_DIR = "./data_feed_trans/"

# Saving directory of nonanswers from transcripts.
TRANS_SAVE_DIR = "./data_trans/"

if __name__ == "__main__":
    print("Resolving data feed for strategy...")
    # TODO: DOWNLOAD RAW DATA FROM INTERNET AUTOMATICALLY
    print("Resolving saving directory for strategy...")
    if not os.path.exists(STRATEGY_SAVE_DIR):
        print("Strategy path not exist, create a new directory...", end="")
        os.mkdir(STRATEGY_SAVE_DIR)
    print("Done!")

