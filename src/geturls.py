#!/usr/bin/env python

import traceback
import sys

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from urls import URLS


SEARCH_PAGE_URL = 'https://www.marketscreener.com/search/?mots='


def get_url(driver: WebDriver, symbol: str) -> str:
    driver.get(SEARCH_PAGE_URL + symbol)

    try:
        market = driver.find_element_by_xpath('//*[@id="ALNI0"]/tbody/tr[2]/td[7]').get_attribute('innerHTML').replace('&nbsp;', ' ')
        ms_name = driver.find_element_by_xpath('//*[@id="ALNI0"]/tbody/tr[2]/td[3]/a').get_attribute('innerHTML')
        print(name, market)
        if (market == 'London Stock Exchange'):
            ms_name = driver.find_element_by_xpath('//*[@id="ALNI0"]/tbody/tr[2]/td[3]/a').get_attribute('innerHTML')
            ms_url = driver.find_element_by_xpath('//*[@id="ALNI0"]/tbody/tr[2]/td[3]/a').get_attribute('href') + 'financials/'
            return ms_name, ms_url
    except selenium.common.exceptions.NoSuchElementException:
        print(traceback.format_exc())
        return None, None

    return None, None


if __name__ == '__main__':
    # Parse command line args
    gui = 'gui' in sys.argv

    options = webdriver.ChromeOptions()
    if not gui:
        options.add_argument('headless')

    urls = []
    missed = []

    with open('info.txt') as f:
        for line in f:
            driver = webdriver.Chrome(chrome_options=options)
            name, symbol, sector = line.strip().split('\t')
            ms_name, ms_url = get_url(driver, symbol)
            driver.close()

            if ms_url:
                print(ms_url, ms_name)
                if (ms_url, ms_name) not in urls:
                    urls.append((ms_url, ms_name))
                else:
                    print(ms_name + " added twice to NAMES")
            else:
                print('couldn\'t find %s' % name)
                missed.append(name)

    for url, name in urls:
        if url not in URLS:
            print("'%s'" % url)

    for url, name in urls:
        if url in URLS:
            print("already had '%s'" % name)

    print('Could not find:')
    for name in missed:
        print(name)
