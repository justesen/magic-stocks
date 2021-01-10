#!/usr/bin/env python

import time
import traceback
import sys
from collections.abc import Callable
from typing import Dict, List, Tuple

import selenium
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from names import NAMES
from urls import URLS


SEARCH_PAGE_URL = 'https://www.morningstar.dk/dk/funds/SecuritySearchResults.aspx?type=STOCK&search='


def get_url(driver: WebDriver, name: str) -> str:
    driver.get(SEARCH_PAGE_URL + name)

    try:
        driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]').click()
        time.sleep(2)
        driver.get(SEARCH_PAGE_URL + name)
    except selenium.common.exceptions.NoSuchElementException:
        pass

    for tr in range(2, 10):
        try:
            ticker = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_stockTable"]/tbody/tr[%d]/td[2]/span' % tr).get_attribute('innerHTML')
            if ticker.split(':')[0] in ['NYSE', 'NASDAQ']:
                ms_name = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_stockTable"]/tbody/tr[%d]/td[1]/a' % tr).get_attribute('innerHTML')
                ms_url = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_stockTable"]/tbody/tr[%d]/td[1]/a' % tr).get_attribute('href')
                return ms_name, ms_url
        except selenium.common.exceptions.NoSuchElementException:
            print("error: couldn't find '%s'" % name)
            return None, None

    return None, None


def normalize(name: str) -> str:
    name = name.replace('.', ' ')
    name = ''.join([c.lower() for c in name
                    if c.isalnum() or c == ' '])
    terms = [t for t in name.split()
             if t not in ['the', 'co', 'corp', 'class', 'corporation', 'limited', 'ltd', 'company', 'group'] and not t.startswith('inc')]
    return ' '.join(terms)


if __name__ == '__main__':
    # Parse command line args
    gui = 'gui' in sys.argv

    options = webdriver.ChromeOptions()
    if not gui:
        options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    urls = []
    missed = []

    for name in NAMES:
        norm_name = normalize(name)
        ms_name, ms_url = get_url(driver, norm_name)

        if ms_url:
            print(ms_url, ms_name)
            if (ms_url, ms_name) not in urls:
                urls.append((ms_url, ms_name))
            else:
                print(ms_name + " added twice to NAMES")
        else:
            missed.append(name)

    for url, name in urls:
        if url not in URLS:
            print("'%s',  # %s" % (url, name))

    for url, name in urls:
        if url in URLS:
            print("already had '%s'" % name)

    print('Could not find:')
    for name in missed:
        print(name)
