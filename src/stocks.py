#!/usr/bin/env python

import time
import traceback
import sys
from collections.abc import Callable
from typing import Dict, List

import selenium
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from urls import URLS


EUR_TO_DKK = 7.44


def parse_decimal_comma_string(s: str) -> float:
    """Parse string with decimal comma to float"""
    s = s.replace(' ', '')
    s = s.replace(',', '.')
    if s == '-':
        return None
    return float(s)


def find_and_parse(driver: WebDriver, xpath: str, parse_fn: Callable = parse_decimal_comma_string) -> float:
    """Find xpath element on web page given by driver and parse it with parse_fn"""
    return parse_fn(driver.find_element_by_xpath(xpath).get_attribute('innerHTML'))


def get_stock_data(driver: WebDriver, url: str) -> Dict:
    """Return dict with data on stock from url using driver"""
    driver.get(url)

    header = driver.find_element_by_xpath('//*[@id="zbCenter"]/div/span/table[1]/tbody/tr/td[2]/a').get_attribute('innerHTML')
    symbol = header[header.index('(') + 1:header.index(')')]

    try:
        currency_price = driver.find_element_by_xpath('//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[13]/td[1]/div').get_attribute('innerHTML').strip()[13:13+3]
    except selenium.common.exceptions.NoSuchElementException:
        currency_price = driver.find_element_by_xpath('//*[@id="zbCenter"]/div/span/table[3]/tbody/tr/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[13]/td[1]/div').get_attribute('innerHTML').strip()[13:13+3]

    try:
        currency_financials = driver.find_element_by_xpath('//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[13]/td/div[2]').get_attribute('innerHTML').strip()[13:13+3]
    except selenium.common.exceptions.NoSuchElementException:
        currency_financials = currency_price

    stock = {
        'name': driver.find_element_by_xpath('//*[@id="zbCenter"]/div/span/table[1]/tbody/tr/td[2]/a/h1').get_attribute('innerHTML').replace('&amp;', '&'),
        'symbol': symbol,
        'url': url,
        'price': find_and_parse(driver, '//*[@id="zbjsfv_dr"]'),
        'currency_price': currency_price,
        'currency_financials': currency_financials,
        'years': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/b', int),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[3]/b', int),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[4]/b', int),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[5]/b', int),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[6]/b', int),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[7]/b', int),
        ],
        'capitalization': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[7]'),
        ],
        'ev': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td[7]'),
        ],
        'num_shares': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[10]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[10]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[10]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[10]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[10]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[10]/td[7]'),
        ],
        # Income
        'sales': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[7]'),
        ],
        'ebitda': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[3]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[3]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[3]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[3]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[3]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[3]/td[7]'),
        ],
        'ebit': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[4]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[4]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[4]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[4]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[4]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[4]/td[7]'),
        ],
        'earnings': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[7]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[7]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[7]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[7]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[7]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[7]/td[7]'),
        ],
        'eps': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[9]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[9]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[9]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[9]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[9]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[9]/td[7]'),
        ],
        'dividend': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[10]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[10]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[10]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[10]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[10]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr[10]/td[7]'),
        ],
        # Balance sheet
        'debt': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[2]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[2]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[2]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[2]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[2]/td[7]'),
        ],
        'cash': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[3]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[3]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[3]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[3]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[3]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[3]/td[7]'),
        ],
        'fcf': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[5]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[5]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[5]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[5]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[5]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[5]/td[7]'),
        ],
        'equity': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[7]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[7]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[7]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[7]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[7]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[7]/td[7]'),
        ],
        'assets': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[9]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[9]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[9]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[9]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[9]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[9]/td[7]'),
        ],
        'book_ps': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[10]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[10]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[10]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[10]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[10]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[10]/td[7]'),
        ],
        'capex': [
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[12]/td[2]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[12]/td[3]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[12]/td[4]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[12]/td[5]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[12]/td[6]'),
            find_and_parse(driver, '//*[@id="zbCenter"]/div/span/table[3]/tbody/tr[2]/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[12]/td[7]'),
        ],
    }

    return stock


def load_data(db, gui: bool) -> None:
    """Load stock data from URLs to database"""
    options = webdriver.ChromeOptions()
    if not gui:
        options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    for url in URLS:
        try:
            stock = get_stock_data(driver, url)
            print(stock['name'])
            db.stocks.insert_one(stock)
            time.sleep(1)
        except Exception:
            print(traceback.format_exc())
            print('failed at ' + url)

    driver.close()


def avg(xs, years):
    covid_year_index = years.index(2020)
    ys = [
        0.3*xs[0],
        0.5*xs[1],
        1.0*xs[2],
        1.1*xs[3],
        1.3*xs[4],
        1.5*xs[5],
    ]
    ys[covid_year_index] *= 0.5
    return sum(ys)/len(ys)


def process_data(db) -> None:
    """Process data in database, i.e., convert currencies, calculate properties and weighted properties"""
    for s in sorted(db.stocks.find(), key=lambda s: s['name']):
        print(f"{s['currency_price']}  {s['name']}")
        try:
            if 2021 in s['years']:
                year_index = s['years'].index(2021)
            else:
                year_index = s['years'].index(2020)

            if s['currency_price'] == 'GBP':
                s['real_price'] = s['price']/100
            else:
                s['real_price'] = s['price']

            if s['equity'][-1] is None and s['equity'][-2] is not None:
                print(f"No equity for {s['years'][-1]}, using that for {s['years'][-2]}")
                s['equity'][-1] = s['equity'][-2]

            if s['book_ps'][-1] is None and s['book_ps'][-2] is not None:
                print(f"No book per share for {s['years'][-1]}, using that for {s['years'][-2]}")
                s['book_ps'][-1] = s['book_ps'][-2]

            if any(ns is None for ns in s['num_shares']):
                print(f"No number of shares, using the most recent")
                most_recent_num_shares = next((ns for ns in reversed(s['num_shares']) if ns is not None), None)
                s['num_shares'] = [most_recent_num_shares if ns is None else ns for ns in s['num_shares']]

            if any(bps is None for bps in s['book_ps']):
                i = s['book_ps'].index(None)
                s['book_ps'][i] = (s['book_ps'][i-1] + s['book_ps'][i+1])/2
                print(f"No book per share found for {s['years'][i]}, using average of {s['years'][i-1]} and {s['years'][i+1]}")

            s['roe'] = [
                100*s['earnings'][i]/s['equity'][i] if s['equity'][i] else 0
                for i in range(len(s['years']))
            ]
            s['roa'] = [
                100*s['earnings'][i]/s['assets'][i] if s['assets'][i] else 0
                for i in range(len(s['years']))
            ]

            s['avg_roe'] = avg(s['roe'], s['years'])
            s['avg_roa'] = avg(s['roa'], s['years'])
            s['yield'] = 100*s['dividend'][year_index]/s['real_price'] if s['dividend'][year_index] else 0
            s['last_year'] = s['years'][-1]
            s['earnings_ev'] = avg([
                s['earnings'][i]/s['ev'][year_index] if s['earnings'][i] else 0
                for i in range(len(s['years']))
            ], years=s['years'])
            s['fcf_ev'] = avg([
                s['fcf'][i]/s['ev'][year_index] if s['fcf'][i] else 0
                for i in range(len(s['years']))
            ], years=s['years'])

            s['avg_roce'] = avg([
                100*(s['earnings'][i] if s['earnings'][i] else 0)/((s['equity'][i] if s['equity'][i] else -s['book_ps'][i]*s['num_shares'][year_index]/1000) + (s['debt'][i] if s['debt'][i] else 0))
                for i in range(len(s['years']))
            ], years=s['years']) + s['avg_roa']
            try:
                s['b_p'] = (s['equity'][year_index] if s['equity'][year_index] else s['equity'][year_index - 1])/s['capitalization'][year_index]
            except Exception:
                s['b_p'] = 0
            s['valuation'] = 2*s['earnings_ev'] + s['fcf_ev']
            s['filter_assets'] = [a for a in s['assets'] if a is not None]
            if s['filter_assets']:
                s['invest'] = ((s['filter_assets'][-1]/s['filter_assets'][0])**(1/len(s['filter_assets'])) - 1)*100
            else:
                print('No assets found')
                # db.stocks.update({symbol: "TCM"}, {$set: {assets: [844, 911, 929, null, null, null]}})
                s['invest'] = 100

            db.stocks.remove({'name': s['name']})
            db.stocks.insert_one(s)
        except Exception:
            print(traceback.format_exc())


def rank(stocks, s, key, descending=True):
    return [x[key] for x in sorted(stocks, key=lambda s: s[key], reverse=descending)].index(s[key]) + 1


def rank_data(db):
    stocks = [s for s in db.stocks.find({'invest': {'$exists': 1}})]
    median_invest = sorted([s['invest'] for s in stocks])[len(stocks)//2]

    for s in stocks:
        s['rank_bp'] = rank(stocks, s, 'b_p')
        s['rank_valuation'] = rank(stocks, s, 'valuation')
        s['rank_invest'] = 0 if s['invest'] < median_invest else len(stocks)//2
        s['rank_roc'] = rank(stocks, s, 'avg_roce')
        s['score'] = 2*s['rank_valuation'] + s['rank_roc'] + s['rank_bp']//2 + s['rank_invest']//2
        db.stocks.remove({'name': s['name']})
        db.stocks.insert_one(s)
    print("Median invest: %d" % median_invest)


if __name__ == '__main__':
    # Parse command line args
    gui = 'gui' in sys.argv
    clear = 'clear' in sys.argv
    load = 'load' in sys.argv
    process = 'process' in sys.argv

    db = pymongo.MongoClient().stocksdb

    if clear:
        db.stocks.remove({})
    if load:
        load_data(db, gui)
    if process:
        process_data(db)
        rank_data(db)
