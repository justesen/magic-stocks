# Stocks #
Rates stocks based on valuation and ROC metrics inspired by Joel Greenblatt's *The Little Book that Beats the Market*.

Scrapes data from https://morningstar.dk/.

## Running ##
From `src/folder`:
* Update data with `./stocks.py clear load`
* Process data with `./stocks.py process`
* Update JSON files used by frontend with `./exportstocksdata.sh`
* Or do it all in one go with `./stocks.py clear load process && ./exportstocksdata.sh`

Open `web/index.html` in a browser to view.
