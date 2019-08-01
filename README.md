# TF
Reproduction of Textual Factors in 10-Ks and Earnings Call Transcripts.

## Textual Factors in 10-Ks.
Textual Factors in 10-Ks are constructed according to Bankers et al.[1].

### Data Feed.
Firm-year fundamentals are from Compustat and 10-Ks are from EDGAR, SEC.

### Descriptions.

getcorplist.py -- get corporate list from 10-K files.

pars.py -- read 10-Ks and parse the "Item 1" part.

indexcalculate.py -- calculate textual factors for 10-Ks.

indicatorsparse.py -- combine textual factors from individual files.


## Textual Factors in Earnings Call Transcripts.
Textual Factors in earnings call transcripts are constructed according to Gow et al.[2]. Instead of using CrowdFlower, I try to form an automatic way to extract Q-A pairs in earnings call transcripts.

### Data Feed.
Firm-year fundamentals are from Compustat and earnings call transcripts are parsed from www.seekingalpha.com.

### Descriptions.

data_feed/htmparser.py -- get htm files in seekingalpha's list of earnings call transcripts.

data_processing/get_list.py -- get the detailed list of transcripts.

data_processing/get_fisical.py -- get fisical year and quarter.

data_processing/download_trans.py -- download each file from seekingalpha.

data_processing/qa_sep_new.py -- seperate Q-A section for each transcript.

data_processing/qa_div.py -- divide Q-A pairs automatically.

statistics/gen_key.py --  create foreign key when joining tables from textual factors and fundamentals.

statistics/statistics.py -- calculate textual factors for each earnings call transcript.

statistics/synthesis.py -- left join fundamentals to textual factors.

## Reference.

[1] Banker et al., "A Textual Measure of Strategy".

[2] Gow et al., "Non-answers during Conference Calls".