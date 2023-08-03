#!/bin/bash

sudo apt install python3 python3-pip build-essential python3-dev
pip install -U scikit-learn
pip install -r requirements.txt

sudo apt-get install npm
cd frontend/url-detector
npm i
cd .. && cd ..

## TEXT PROCESSING ##

# head -5000 URLs.csv > test.csv
# fgrep -c phishing URLs.csv

# Concat the datasets in a temporary file (excludes header from second file)
# awk '(NR == 1) || (FNR > 1)' kaggle/kaggle.csv phishtank/phishtank.csv > tmp.csv

# Remove duplicate rows without sorting in a final file and removes the temporary one
# awk '{if (!($0 in x)) {print $0; x[$0]=1} }' tmp.csv > merged.csv && rm tmp.csv
