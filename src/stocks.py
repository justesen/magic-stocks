#!/usr/bin/env python

import time
import traceback
import sys

import selenium
import pymongo
from selenium import webdriver


EUR_TO_DKK = 7.44


URLS = [
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5RL',  # A. P. Moller Maersk A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5RN',  # Ambu
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5RB',  # Bavarian Nordic A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5K1',  # Carlsberg A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000OO3C',  # Chr. Hansen Holding A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5K4',  # Coloplast A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5KA',  # Danske Bank A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5LK',  # Demant AS
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5Q9',  # DSV Panalpina AS
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5RO',  # FLSmidth & Co. A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5QU',  # Genmab A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5KG',  # GN Store Nord A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P00012E78',  # ISS A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5KR',  # Jyske Bank A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5Q7',  # Lundbeck A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5BQ',  # Novo Nordisk A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5QX',  # Novozymes A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000Q1VF',  # Pandora A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5L9',  # Rockwool International A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5QC',  # Royal UNIBREW A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5QV',  # SimCorp A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5RI',  # Tryg A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5Q5',  # Vestas Wind Systems A/S
    # 'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0001846T',  # Ørsted A/S

    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5LL',  # Alk-Abello A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5PI',  # Alm Brand AS
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5K5',  # DFDS A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0001H6JR',  # Drilling Company of 1972
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5RA',  # Jeudan A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5PB',  # Copenhagen Airports A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0001DFE0',  # Netcompany Group AS
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A6IU',  # Nordea Bank Abp
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5L8',  # Ringkjøbing Landbobank A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P00017EFW',  # Scandinavian Tobacco Group A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5JU',  # Schouw & Co A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5PV',  # Spar Nord Bank A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5R6',  # Sydbank A/S

    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5PC',  # Brødrene Hartmann A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5PK',  # Dampskibsselskabet NORDEN A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000Z26I',  # Matas A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0001BQUO',  # Nilfisk Holding A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5KX',  # NKT A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5QW',  # RTX A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5QR',  # Solar A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5KP',  # SP Group A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0001C9AZ',  # TCM Group A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5LG',  # Topdanmark A/S
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A5QN',  # UIE PLC

    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000053I',  # The Travelers Company Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0001H3ZI',  # Dow Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000005UI',  # Walgreens Boot Alliance Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000014I',  # Caterpillar Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000002H5',  # Goldman Sachs Group Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000000I',  # 3M Co
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000000CU',  # American Express Co
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000005NO',  # Raytheon Technologies Corp
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000002RH',  # IBM Corp
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000003X1',  # Nike Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000003IJ',  # McDonald's Corp
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000000TU',  # Boeing Co
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000019Y',  # Cisco Systems Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P00000185',  # Chevron Corp
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000CHAD',  # Pfizer Ltd
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000003KE',  # Merck & Co Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000005QY',  # Verizon Communications Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000001BW',  # Coca-Cola Co
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000005UJ',  # The Walt Disney Co
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000002OY',  # The Home Depot Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P00000220',  # Exxon Mobil Corp
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000005NU',  # UnitedHealth Group Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000002X8',  # Intel Corp
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000004GV',  # Procter & Gamble Co
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000005UH',  # Walmart Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000032S',  # Johnson & Johnson
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000031C',  # JPMorgan Chase & Co
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000CPCP',  # Visa Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000000GY',  # Apple Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000003MH',  # Microsoft Corp
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000000B7',  # Amazon.com Inc

    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000002DT',  # General Mills Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000002HD',  # Alphabet Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P00000031',  # AT&T Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000001HZ',  # Ingredion Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000XPGW',  # AbbVie Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000005K5',  # Tyson Foods Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P00008WF2',  # B&G Foods Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000004B0',  # PepsiCo Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000001CL',  # Colgate-Palmolive Co
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000000RD',  # Berkshire Hathaway Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000002DN',  # General Dynamics Corp
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000001GL',  # Consolidated Edison Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P00016CR2',  # The Kraft Heinz Co
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000000AV',  # Altria Group Inc
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P000001BD',  # Clorox Co

    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A6N7',  # Note AB
    'https://www.morningstar.dk/dk/stockquicktake/default.aspx?id=0P0000A6GI',  # Hennes & Mauritz AB
]


def parse_decimal_comma_string(s):
    s = s.replace('.', '')
    s = s.replace(',', '.')
    if s == '-':
        return None
    return float(s)


def parse_market_cap(s):
    if not s.endswith('Mia.'):
        print('parse_market_cap failure: %s does not end with "Mia."' % (s))
    return parse_decimal_comma_string(s[:-len('Mia.')])*1000


def find_and_parse(driver, xpath, parse_fn=parse_decimal_comma_string):
    return parse_fn(driver.find_element_by_xpath(xpath).get_attribute('innerHTML'))


def get_stock_data(driver, url):
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


def load_data(db, gui):
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


def weighted_avg(s, key, growth=False, growth_discount=0.5):
    seq = s[key]
    n = len(seq)
    denom = sum(range(1, n+1))
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

    return sum([e*(i+1)/denom for i, e in enumerate(seq)])


def calc_fcf(s):
    if all((x is None for x in s['fcf'])):
        return s['fcf']

    return [0 if x is None else x for x in s['fcf']]



def calc_debt(s):
    if all((x is None for x in s['long_term_liabilities'])) and all((x is None for x in s['short_term_liabilities'])):
        print('using liabilites')
        return [l - c for l, c in zip(s['liabilities'], s['cash'])]

    return [(0 if lt is None else lt) + (0 if olt is None else olt)
            for st, ost, lt, olt in zip(s['short_term_debt'], s['other_short_term_debt'], s['long_term_debt'], s['other_long_term_debt'])]


def calc_ebit(s):
    if None not in s['ebit']:
        ebit = s['ebit']
    elif None not in s['ebt']:
        ebit = s['ebt']
        print('using ebt')
    else:
        print('using earnings')
        ebit = s['earnings']

    return ebit


def process_data(db):
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

        s['ev'] = s['market_cap'] + s['debt'][-1] #- s['cash'][-1]
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


def rank(stocks, s, key):
    return [x[key] for x in sorted(stocks, key=lambda s: s[key], reverse=True)].index(s[key]) + 1


def rank_data(db):
    stocks = [s for s in db.stocks.find()]

    for s in db.stocks.find():
        s['rank_valuation'] = rank(stocks, s, 'valuation')
        s['rank_roc'] = rank(stocks, s, 'weighted_roce')
        s['score'] = s['rank_valuation'] + s['rank_roc']
        db.stocks.remove({'name': s['name']})
        db.stocks.insert_one(s)


if __name__ == '__main__':
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
