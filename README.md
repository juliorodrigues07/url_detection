[![Python 3.10.12](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3106/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/2.3.x/)
[![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252)](https://colab.research.google.com/?utm_source=scs-index)

[![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)](https://vuejs.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
# URL Detector

Malicious URL Detector built utilizing several data mining, machine learning and data science concepts, techniques and algorithms.

# Requirements

All the project dependencies are listed is this section (languages, libraries, package managers, frameworks, ...), as well as the instructions to install each of of them.

## To install all dependencies

    ./install_dependencies.sh

## Languages and package managers

- [Python3](https://python.org) and [pip](https://pip.pypa.io/en/stable/installation/) package manager:

      sudo apt install python3 python3-pip build-essential python3-dev

- Node.JS package manager - [npm](https://docs.npmjs.com/) (**Optional**):

      sudo apt-get install npm
      
## Data Mining

- [scikit-learn](https://scikit-learn.org/stable/index.html) library:

      pip install -U scikit-learn
      
- [xgboost](https://xgboost.readthedocs.io/en/stable/) library:
 
      pip install xgboost

- [mlxtend](https://rasbt.github.io/mlxtend/) library:
 
      pip install mlxtend

- [imbalanced-learn](https://imbalanced-learn.org/stable/) library:
 
      pip install imbalanced-learn
       
- [pandas](https://pandas.pydata.org/) library:

      pip install pandas

## Data Visualization
       
- [Matplotlib](https://matplotlib.org/) library:
 
      pip install matplotlib
       
- [seaborn](https://seaborn.pydata.org/) library:
 
      pip install seaborn
      
- [joblib](https://joblib.readthedocs.io/en/latest/index.html) library:
 
      pip install joblib
      
- [numpy](https://numpy.org/) library:

      pip install numpy
      
## Web Scraping (Optional)
      
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library:
 
      pip install beautifulsoup4
      
- [mechanize](https://mechanize.readthedocs.io/en/latest/) library:
 
      pip install mechanize
      
- [Random User Agents](https://github.com/Luqman-Ud-Din/random_user_agent) library:
 
      pip install random_user_agent
      
- [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/introduction.html) library:
 
      pip install pycryptodomex

## GUI (Graphical User Interface - Optional)

- [Vue.js](https://vuejs.org/) framework:

      npm install -g @vue/cli

### Inside _url-detector_ directory

- [Bootstrap](https://vuejs.org/) framework:

      npm install bootstrap@4.6.0 --save

- [axios](https://axios-http.com/ptbr/docs/intro) library:

      npm i axios

- [Font Awesome](https://fontawesome.com/) tool kit:

      npm i --save @fortawesome/free-solid-svg-icons && npm i --save @fortawesome/vue-fontawesome@latest-2

- To install all GUI dependencies:

      npm i

# Execution

All the instructions for exploring the project functionalities are listed in this section, as well as the commands to execute each application.

## Data Mining

    python3 main.py
    
## Web Scraping
      
    python3 phishing_scraper.py

## Application

### CLI (Command Line Interface Mode)

- Inside _src_ directory, execute the command using the following template: `python3 predict.py cli <url> <algorithm>`.
- Example with a phishing URL:

      python3 predict.py cli https://bujhanginamfb.github.io/taelasos/update-recovry/ XGB

### GUI (Graphical User Interface Mode)

- Open two terminal instances and execute the following commands in each one of them, respectively.
- Terminal 1 - Back-end (inside _src_ directory):

      python3 predict.py server

- Terminal 2 - Front-end (inside _url-detector_ directory):

      npm run serve

- You should receive two _URLs_ as outputs (`http://localhost:<port number>`). To visualize it, just open any of them in a browser of your choice. The front-end server (GUI) should be running at:

      http://localhost:8080

- Finally, feel free to test the model with your own URLs! :champagne:

### Main Screen

![Main Screen](/docs/screen.png)

# Outro

Due to model training with the [Kaggle](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset) dataset, the model reliability can suffer a lot depending on the user's inputted URL format. Most of the URLs present in the Kaggle dataset doesn't have its communication protocol specified (HTTP, HTTPS, ...), which could introduce large bias on the results and models trained, making the classifications quite unstable.
    
