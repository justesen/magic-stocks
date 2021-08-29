# Stocks #
Rates stocks based on metrics inspired by Joel Greenblatt's *The Little Book that Beats the Market* and factors loosely based on Fama-French Five Factor Model.

Scrapes data from https://marketscreener.com/.

## Running ##
From `src/` folder:
* Update data with `./stocks.py clear load`
* Process data with `./stocks.py process`
* Update JSON files used by frontend with `./exportstocksdata.sh`
* Or do it all in one go with `./stocks.py clear load process && ./exportstocksdata.sh`

Open `web/index.html` in a browser to view.

## Dependencies ##
* selenium
* pymongo
