from Cryptodome.Random import random
from bs4 import BeautifulSoup
from mechanize import Browser
from time import sleep
from math import ceil
from os import chdir
from os import getcwd
import constants as const


def initialize_browser(url):

    browser = Browser()
    browser.set_handle_robots(False)

    # Requests as a distinct user-agent each time to avoid IP blocks
    browser.addheaders = [('User-agent', const.USER_AGENT_ROTATOR.get_random_user_agent())]
    browser.open(url)

    return browser


def phish_scrapper():

    page_number = 0
    # n_requests = ceil(const.N_URLS / const.PER_PAGE)
    n_requests = 10

    with open(f'{getcwd()}/datasets/phishtank.csv', 'w') as file:
        file.write('url,type\n')

        while page_number < n_requests:

            # Gets the page html
            browser = initialize_browser(f'{const.MAIN_URL}page={page_number}&{const.QUERY}')
            response = browser.response().read()
            soup = BeautifulSoup(response, 'lxml')

            # Obtains all the phishing urls info in the table
            trs = soup.find_all('tr')
            for tr in trs:

                # Filters by each url info (id, url, who reported, valid status, online status)
                i = 0
                tds = tr.find_all('td')
                for td in tds:

                    # Discards info about when it was added, getting only the url text
                    if i == 1:
                        raw_text = td.get_text().split('added on ')[0]
                        # phishing_url = raw_text[0].replace('[email protected]', '')
                        file.write(f'{raw_text},phishing\n')
                        break

                    i += 1

            # Monitoring scraping progress, killing browser instances between each request
            browser.close()
            progress = (page_number / n_requests) * 100.0
            page_number += 1

            print(f'{round(progress, 2)}% concluded...')

            # Time interval randomly defined for spacing at each request and avoid IP blocks
            timing = random.randint(2, 5)
            sleep(timing)


if __name__ == '__main__':
    chdir('../..')
    phish_scrapper()
