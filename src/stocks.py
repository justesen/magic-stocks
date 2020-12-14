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
    s = s.replace('.', '')
    s = s.replace(',', '.')
    if s == '-':
        return None
    return float(s)


def parse_market_cap(s: str) -> float:
    """Parse string with market cap in Danish ("mia.") to float (mio.)"""
    if not s.endswith('Mia.'):
        raise Exception('parse_market_cap failure: %s does not end with "Mia."' % (s))
    return parse_decimal_comma_string(s[:-len('Mia.')])*1000


def find_and_parse(driver: WebDriver, xpath: str, parse_fn: Callable = parse_decimal_comma_string) -> float:
    """Find xpath element on web page given by driver and parse it with parse_fn"""
    return parse_fn(driver.find_element_by_xpath(xpath).get_attribute('innerHTML'))


def get_stock_data(driver: WebDriver, url: str) -> Dict:
    """Return dict with data on stock from url using driver"""
    driver.get(url)

    try:
        driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]').click()
    except selenium.common.exceptions.NoSuchElementException:
        pass

    stock = {
        'name': driver.find_element_by_class_name('securityName').get_attribute('innerHTML')[:-3].replace('&amp;', '&'),
        'symbol': driver.find_element_by_class_name('securitySymbol').get_attribute('innerHTML'),
        'url': url,
        'debt_to_equity': find_and_parse(driver, '//*[@id="KeyStatsDebtEquity"]/td'),
        'market_cap_raw': find_and_parse(driver, '//*[@id="Col0MCap"]', parse_market_cap),
        'price': find_and_parse(driver, '//*[@id="Col0Price"]'),
        'p_e': find_and_parse(driver, '//*[@id="Col0PE"]'),
        'p_b': find_and_parse(driver, '//*[@id="KeyStatsPriceBookRatio"]/td'),
        'financials_currency': driver.find_element_by_xpath('//*[@id="OverviewFinancialsDisclaimer"]/p').get_attribute('innerHTML').strip()[-4:-1],
        'fcf': [
            find_and_parse(driver, '//*[@id="OverviewFinancials"]/table/tbody[3]/tr[4]/td[1]'),
            find_and_parse(driver, '//*[@id="OverviewFinancials"]/table/tbody[3]/tr[4]/td[2]'),
            find_and_parse(driver, '//*[@id="OverviewFinancials"]/table/tbody[3]/tr[4]/td[3]'),
        ]
    }

    driver.find_element_by_xpath('//*[@id="LnkPage10"]').click()
    stock['revenue'] = [
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[1]/tr[1]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[1]/tr[1]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[1]/tr[1]/td[5]'),
    ]
    stock['ebit'] = [
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[2]/tr[8]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[2]/tr[8]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[2]/tr[8]/td[5]'),
    ]
    stock['ebt'] = [
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[3]/tr[2]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[3]/tr[2]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[3]/tr[2]/td[5]'),
    ]
    stock['earnings'] = [
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[3]/tr[5]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[3]/tr[5]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsIncomeStatement"]/table/tbody[3]/tr[5]/td[5]'),
    ]

    driver.find_element_by_xpath('//*[@id="LnkPage10Viewbs"]').click()
    stock['cash'] = [
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[1]/tr[6]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[1]/tr[6]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[1]/tr[6]/td[5]'),
    ]
    stock['short_term_debt'] = [
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[6]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[6]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[6]/td[5]'),
    ]
    stock['other_short_term_debt'] = [
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[7]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[7]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[7]/td[5]'),
    ]
    stock['short_term_liabilities'] = [
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[8]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[8]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[8]/td[5]'),
    ]
    stock['long_term_debt'] = [
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[11]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[11]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[11]/td[5]'),
    ]
    stock['other_long_term_debt'] = [
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[12]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[12]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[12]/td[5]'),
    ]
    stock['long_term_liabilities'] = [
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[13]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[13]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[13]/td[5]'),
    ]
    stock['liabilities'] = [
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[14]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[14]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[14]/td[5]'),
    ]
    stock['equity'] = [
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[21]/td[3]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[21]/td[4]'),
        find_and_parse(driver, '//*[@id="FinancialsBalanceSheet"]/table/tbody[2]/tr[21]/td[5]'),
    ]

    driver.find_element_by_xpath('//*[@id="LnkPage11"]').click()
    stock['roa'] = [
        find_and_parse(driver, '//*[@id="KeyRatiosProfitability"]/table/tbody/tr[3]/td[3]'),
        find_and_parse(driver, '//*[@id="KeyRatiosProfitability"]/table/tbody/tr[3]/td[4]'),
        find_and_parse(driver, '//*[@id="KeyRatiosProfitability"]/table/tbody/tr[3]/td[5]'),
    ]
    stock['roe'] = [
        find_and_parse(driver, '//*[@id="KeyRatiosProfitability"]/table/tbody/tr[5]/td[3]'),
        find_and_parse(driver, '//*[@id="KeyRatiosProfitability"]/table/tbody/tr[5]/td[4]'),
        find_and_parse(driver, '//*[@id="KeyRatiosProfitability"]/table/tbody/tr[5]/td[5]'),
    ]

    return stock


def load_data(db, gui: bool) -> None:
    """Load stock data from URLs to database"""
    options = webdriver.ChromeOptions()
    if not gui:
        options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    for i, url in enumerate(URLS):
        try:
            stock = get_stock_data(driver, url)
            print(stock['name'])
            db.stocks.insert_one(stock)
            time.sleep(1)
        except Exception:
            print(traceback.format_exc())
            print('failed at ' + str(i))
            input()

    driver.close()


def weighted_avg(s: Dict, key: str, growth: bool = False, growth_discount: float = 0.5) -> float:
    """Return weighted average of three values in s[key]

    If growth is True and elements in s[key] are monotonically increasing or decreasing,
    apply the smallest (in |absolute| terms) growth factor between the pairs of values,
    but discount the growth by growth_discount (defaults to 50%).
    """
    seq = s[key]
    n = len(seq)
    denom = sum(range(1, n + 1))
    s['growth_' + key] = 0

    if growth and seq[0] < seq[1] < seq[2] and all([x > 0 for x in seq]):
        growth_factor = ((min(seq[2]/seq[1], seq[1]/seq[0]) - 1)*growth_discount + 1)
        growth = growth_factor*seq[2]
        s['growth_' + key] = growth_factor - 1
        return growth

    if growth and seq[0] > seq[1] > seq[2] and all([x > 0 for x in seq]):
        growth_factor = ((max(seq[2]/seq[1], seq[1]/seq[0]) - 1)*growth_discount + 1)
        growth = growth_factor*seq[2]
        s['growth_' + key] = growth_factor - 1
        return growth

    return sum([e*(i + 1)/denom for i, e in enumerate(seq)])


def calc_fcf(s: Dict) -> List:
    """If not all FCF values are missing (i.e. None), set remaing to 0"""
    if all((x is None for x in s['fcf'])):
        return s['fcf']

    return [0 if x is None else x for x in s['fcf']]


def calc_debt(s: Dict) -> List:
    """Return debt based on long/short term liabilites and cash"""
    if all((x is None for x in s['long_term_liabilities'])) and all((x is None for x in s['short_term_liabilities'])):
        print('using liabilites')
        return [lia - c for lia, c in zip(s['liabilities'], s['cash'])]

    return [(0 if lt is None else lt) + (0 if olt is None else olt)
            for st, ost, lt, olt in zip(s['short_term_debt'], s['other_short_term_debt'], s['long_term_debt'], s['other_long_term_debt'])]


def calc_ebit(s: Dict) -> List:
    """Calculate EBIT based on available data as either EBIT, EBT or earnings"""
    if None not in s['ebit']:
        ebit = s['ebit']
    elif None not in s['ebt']:
        ebit = s['ebt']
        print('using ebt')
    else:
        print('using earnings')
        ebit = s['earnings']

    return ebit


def process_data(db) -> None:
    """Process data in database, i.e., convert currencies, calculate properties and weighted properties"""
    for s in sorted(db.stocks.find(), key=lambda s: s['name']):
        print(s['name'])

        if s['financials_currency'] == 'EUR':
            print('euro conversion!')
            s['market_cap'] = s['market_cap_raw']/EUR_TO_DKK
        else:
            s['market_cap'] = s['market_cap_raw']

        s['my_cash'] = [0 if x is None else x for x in s['cash']]
        s['debt'] = calc_debt(s)
        s['my_ebit'] = calc_ebit(s)
        s['my_fcf'] = calc_fcf(s)
        s['roce'] = [100*s['earnings'][i]/((s['equity'][i] if s['equity'][i] > 0 else -s['equity'][i]) + s['debt'][i]) for i in range(len(s['my_ebit']))]

        s['ev'] = s['market_cap'] + s['debt'][-1]
        s['my_debt_to_equity'] = (s['debt'][-1])/s['equity'][-1]

        s['weighted_earnings'] = weighted_avg(s, 'earnings', True)
        s['weighted_ebit'] = weighted_avg(s, 'my_ebit', True)
        if None not in s['my_fcf']:
            s['weighted_fcf'] = weighted_avg(s, 'my_fcf', True)
        s['weighted_roe'] = weighted_avg(s, 'roe', True)
        s['weighted_roa'] = weighted_avg(s, 'roa', True)
        s['weighted_roce'] = weighted_avg(s, 'roce', True)

        s['earnings_ev'] = s['weighted_earnings']/s['ev']
        s['ebit_ev'] = s['weighted_ebit']/s['ev']

        if 'weighted_fcf' in s:
            s['fcf_ev'] = s['weighted_fcf']/s['ev']
            s['valuation'] = 100*(0.6*s['earnings_ev'] + 0.0*s['ebit_ev'] + 0.3*s['fcf_ev'] + 0.1*(1/s['p_e'] if s['p_e'] is not None else 0))
        else:
            print('no fcf')
            s['valuation'] = 100*(0.9*s['earnings_ev'] + 0.0*s['ebit_ev'] + 0.1*(1/s['p_e'] if s['p_e'] is not None else 0))

        db.stocks.remove({'name': s['name']})
        db.stocks.insert_one(s)
        print()


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
