from sklearn.preprocessing import LabelEncoder
from urllib.parse import urlparse
import re


def discretize_values(column, key):

    encoding = LabelEncoder()

    # Discretize column values (bening, phishing, malware, ...) => [0, 1, 2, ...]
    encoding.fit(column[key])
    column[key] = encoding.transform(column[key].copy())

    return column


def url_protocol(url):
    
    protocol = urlparse(url).scheme

    # Identifying which protocol each site uses to construct a new feature
    match = str(protocol)
    if match == 'https':
        return 'HTTPS'
    elif match == 'http':
        return 'HTTP'
    else:
        return 'Not Specified'
    
    
def find_anomalies(url):

    domain = str(urlparse(url).hostname)
    pattern = re.search(domain, url)

    if pattern:
        return 1
    else:
        return 0
    