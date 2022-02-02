## CS:GO Math Engine (Scraper + Extractor)

Backend application for [Counter-Strike: Global Offensive Market](https://steamcommunity.com/market/search?appid=730).

Consists of two main components:
- **CS:GO Math Scraper** is a tool to **scrape** CS:GO market data from *Valve's website*.

- **CS:GO Math Extractor** is a tool to **extract** cases from all items and **calculate** expected value of each case.

## Motivation
*Valve* does not officially offer API for market, hence scraping techniques are used. 

By using extractor, end users may know what is the percentage return on each type of case, by comparing `case + key price` to `expected value`. Additionally, they can compare across other cases and decide which case is most worthwhile to buy.

> Example presentation is available at [csgomath.com](https://csgomath.com) (to be rebuilt)

## Installation
Install necessary dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run scraper + extractor:
```
python main.py
```

Additional flags:
- `--scrape, -s` Only scrape.
- `--extract, -e` Only extract.
- `--debug, -d` Debug mode.

*Note: In the current version, extracted data is not processed any further, therefore **you need a `--debug` flag** to see any output after finish.*

## Further Description
**Expected value** is an arithmetic mean of a large number of independent realization of random variable, which in this case is opening a case or a more specific random variable, like obtaining some version of one weapon. *(Expected value may be also called **estimated value** in parts of code.)*

If calculated **expected value** of a `Wooden Case` is 1.23$, it means, that if `100 Wooden Case`'s are opened, the opener gets items worth 

```
100 * 1.23$ = 123$
```

If calculated **expected value** of a `Dragonbreath M4A1` is 8.92$, it means, that if `100 Dragonbreath M4A1` are looted, the opener gets `Dragonbreath M4A1` worth 
```
100 * 8.92$ = 892$
```
(in many versions: more or less used, StatTrak or not).


#### Scraper:
1. Send `GET` request to market URL with `appid=<CS:GO game id>` as parameter.
2. Loop over market pages with sleep period to avoid 
3. Append items from each page to instance's variable

#### Extractor:
1. Find `cases` in `all items`.
2. Read through `case description` and parse all items, that may be in the case.
3. Find each item from `description` and calculate `one item estimated value`
    - *(Calculating `item value` depends on the item type. It is based on odds provided by Valve. StatTrak/Usage odds are included.)*
    - Use `sale price` instead of `sell price`. 
>**Sale** price is the price that the item was lately sold for; **sell** price is the current lowest sell offer. It is an important distinction especially in very rare items: If only one piece of `Superhuman Gloves` is on sale for 1000000$ - `sell_price` is 1000000$ (inaccurate). Two weeks ago, though, someone has bought `Superhuman Gloves` for just 80$ - `sale_price` is 80$ (accurate).
4. Add `total` field in each of the element in case description
5. Add `total` field and `timestamp` in each whole case.
5. Altered list is available in scraper's instance variable `cases`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](./LICENSE)
