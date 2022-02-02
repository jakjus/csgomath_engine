import argparse
from components.scraper import Scraper
from components.extractor import Extractor

parser = argparse.ArgumentParser(description='Define script options.')
parser.add_argument("-s", "--scrape", help="Only scrape.",
                    action="store_true", default=True)
parser.add_argument("-e", "--extract", help="Only extract.",
                    action="store_true", default=True)
parser.add_argument("-d", "--debug", help="Debug mode.",
                    action="store_true")
args = parser.parse_args()


def main():
    if args.scrape:
        scraper = Scraper()
        scraper.get_csgo_items()
        scraper.save_to_pickle('steam_market_items')
    if args.extract:
        extractor = Extractor(pickle_name='steam_market_items')
        extractor.extract_full()
        cases = extractor.cases
    if args.debug:
        print(cases)

if __name__ == "__main__":
    main()
