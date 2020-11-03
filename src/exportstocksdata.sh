rm ../data/*
mongoexport --db stocksdb -c stocks --jsonArray --pretty -o ../data/data.json
echo 'const DATA = ' > tmp.js
cat tmp.js ../data/data.json > ../data/data.js
rm tmp.js

