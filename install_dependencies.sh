#!/bin/bash

sudo apt install python3 python3-pip build-essential python3-dev
pip install -U scikit-learn
pip install -r requirements.txt

## Text processing ##

# head -5000 URLs.csv > test.csv
# fgrep -c benign URLs.csv
# fgrep -c defacement URLs.csv
# fgrep -c phishing URLs.csv
# fgrep -c malware URLs.csv
